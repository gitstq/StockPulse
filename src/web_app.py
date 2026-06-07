"""
StockPulse Web 应用模块
Web dashboard for StockPulse
"""

import json
from datetime import datetime
from typing import Dict, List

from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit

from .config import init_config
from .data_source import DataSourceManager
from .watchlist import WatchlistManager
from .analyzer import InsightGenerator


app = Flask(__name__)
app.config['SECRET_KEY'] = 'stockpulse-secret-key'
socketio = SocketIO(app, cors_allowed_origins="*")

# 初始化
data_source = None
watchlist_manager = None


def init_app():
    """初始化应用"""
    global data_source, watchlist_manager
    init_config()
    data_source = DataSourceManager()
    watchlist_manager = WatchlistManager()


@app.route('/')
def index():
    """主页"""
    return render_template('index.html')


@app.route('/api/quote/<symbol>')
def api_quote(symbol):
    """API: 获取股票报价"""
    quote = data_source.get_quote(symbol.upper())
    if quote:
        return jsonify(quote.to_dict())
    return jsonify({"error": "无法获取数据"}), 404


@app.route('/api/historical/<symbol>')
def api_historical(symbol):
    """API: 获取历史数据"""
    period = request.args.get('period', '1mo')
    historical = data_source.get_historical(symbol.upper(), period)
    return jsonify([h.to_dict() for h in historical])


@app.route('/api/market')
def api_market():
    """API: 获取市场概览"""
    overview = data_source.get_market_overview()
    return jsonify([o.to_dict() for o in overview])


@app.route('/api/watchlist')
def api_watchlist():
    """API: 获取自选股"""
    items = watchlist_manager.get_watchlist()
    result = []
    for item in items:
        quote = data_source.get_quote(item.symbol)
        item_dict = item.to_dict()
        if quote:
            item_dict['quote'] = quote.to_dict()
        result.append(item_dict)
    return jsonify(result)


@app.route('/api/watchlist', methods=['POST'])
def api_add_watchlist():
    """API: 添加自选股"""
    data = request.json
    symbol = data.get('symbol', '').upper()
    name = data.get('name', '')
    notes = data.get('notes', '')
    
    success = watchlist_manager.add_stock(symbol, name, notes)
    return jsonify({"success": success})


@app.route('/api/watchlist/<symbol>', methods=['DELETE'])
def api_remove_watchlist(symbol):
    """API: 移除自选股"""
    success = watchlist_manager.remove_stock(symbol.upper())
    return jsonify({"success": success})


@app.route('/api/insight/<symbol>')
def api_insight(symbol):
    """API: 获取股票分析"""
    quote = data_source.get_quote(symbol.upper())
    historical = data_source.get_historical(symbol.upper(), '3mo')
    
    if not quote:
        return jsonify({"error": "无法获取数据"}), 404
    
    insight = InsightGenerator.generate_insight(symbol.upper(), quote, historical)
    return jsonify(insight.to_dict())


@app.route('/api/search')
def api_search():
    """API: 搜索股票"""
    query = request.args.get('q', '')
    results = data_source.search_symbols(query)
    return jsonify(results)


@socketio.on('connect')
def handle_connect():
    """处理WebSocket连接"""
    emit('connected', {'data': 'Connected to StockPulse'})


@socketio.on('subscribe')
def handle_subscribe(data):
    """处理订阅请求"""
    symbol = data.get('symbol', '').upper()
    quote = data_source.get_quote(symbol)
    if quote:
        emit('quote_update', quote.to_dict())


def run_web_app(host='0.0.0.0', port=5000, debug=False):
    """运行Web应用"""
    init_app()
    socketio.run(app, host=host, port=port, debug=debug)


if __name__ == '__main__':
    run_web_app(debug=True)
