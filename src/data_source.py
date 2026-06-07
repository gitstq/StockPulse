"""
StockPulse 数据源模块
Data source adapters for StockPulse
"""

import requests
import json
import time
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Optional, List, Dict
from urllib.parse import urlencode

from .models import StockQuote, HistoricalData, MarketOverview
from .config import get_config


class DataSourceError(Exception):
    """数据源异常"""
    pass


class RateLimitError(DataSourceError):
    """速率限制异常"""
    pass


class BaseDataSource(ABC):
    """数据源基类"""
    
    def __init__(self, name: str, base_url: str, api_key: Optional[str] = None):
        self.name = name
        self.base_url = base_url
        self.api_key = api_key
        self.session = requests.Session()
        self._last_request_time = 0
        self._rate_limit_delay = 1.0  # 默认1秒间隔
    
    def _make_request(self, endpoint: str, params: Optional[Dict] = None, 
                      headers: Optional[Dict] = None) -> Dict:
        """发送HTTP请求"""
        # 速率限制
        elapsed = time.time() - self._last_request_time
        if elapsed < self._rate_limit_delay:
            time.sleep(self._rate_limit_delay - elapsed)
        
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            response = self.session.get(url, params=params, headers=headers, timeout=30)
            self._last_request_time = time.time()
            
            if response.status_code == 429:
                raise RateLimitError(f"速率限制: {self.name}")
            
            response.raise_for_status()
            
            # 尝试解析JSON
            try:
                return response.json()
            except json.JSONDecodeError:
                # 返回文本内容
                return {"text": response.text}
                
        except requests.exceptions.RequestException as e:
            raise DataSourceError(f"请求失败 [{self.name}]: {str(e)}")
    
    @abstractmethod
    def get_quote(self, symbol: str) -> Optional[StockQuote]:
        """获取股票报价"""
        pass
    
    @abstractmethod
    def get_historical(self, symbol: str, period: str = "1mo") -> List[HistoricalData]:
        """获取历史数据"""
        pass
    
    @abstractmethod
    def get_market_overview(self) -> List[MarketOverview]:
        """获取市场概览"""
        pass
    
    @abstractmethod
    def search_symbols(self, query: str) -> List[Dict]:
        """搜索股票代码"""
        pass


class YahooFinanceSource(BaseDataSource):
    """Yahoo Finance 数据源"""
    
    def __init__(self):
        super().__init__(
            name="yahoo",
            base_url="https://query1.finance.yahoo.com",
        )
        self._rate_limit_delay = 0.5
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
    
    def get_quote(self, symbol: str) -> Optional[StockQuote]:
        """获取股票报价"""
        try:
            endpoint = f"/v8/finance/chart/{symbol}"
            params = {
                "interval": "1d",
                "range": "1d",
                "includeAdjustedClose": "true"
            }
            
            data = self._make_request(endpoint, params)
            
            if "chart" not in data or "result" not in data["chart"] or not data["chart"]["result"]:
                return None
            
            result = data["chart"]["result"][0]
            meta = result.get("meta", {})
            
            # 获取最新价格
            timestamps = result.get("timestamp", [])
            closes = result.get("indicators", {}).get("quote", [{}])[0].get("close", [])
            volumes = result.get("indicators", {}).get("quote", [{}])[0].get("volume", [])
            
            if not closes or not timestamps:
                return None
            
            # 获取最新有效数据点
            latest_idx = -1
            for i in range(len(closes) - 1, -1, -1):
                if closes[i] is not None:
                    latest_idx = i
                    break
            
            if latest_idx < 0:
                return None
            
            current_price = closes[latest_idx]
            previous_close = meta.get("previousClose", meta.get("chartPreviousClose", current_price))
            
            change = current_price - previous_close
            change_percent = (change / previous_close * 100) if previous_close else 0
            
            # 获取当日高低
            highs = result.get("indicators", {}).get("quote", [{}])[0].get("high", [])
            lows = result.get("indicators", {}).get("quote", [{}])[0].get("low", [])
            opens = result.get("indicators", {}).get("quote", [{}])[0].get("open", [])
            
            day_high = max([h for h in highs if h is not None]) if highs else current_price
            day_low = min([l for l in lows if l is not None]) if lows else current_price
            day_open = opens[0] if opens and opens[0] is not None else previous_close
            day_volume = sum([v for v in volumes if v is not None]) if volumes else 0
            
            quote = StockQuote(
                symbol=symbol,
                name=meta.get("shortName", meta.get("longName", symbol)),
                price=round(current_price, 2),
                change=round(change, 2),
                change_percent=round(change_percent, 2),
                volume=int(day_volume),
                high=round(day_high, 2),
                low=round(day_low, 2),
                open=round(day_open, 2),
                previous_close=round(previous_close, 2),
                currency=meta.get("currency", "USD"),
                timestamp=datetime.now(),
            )
            
            return quote
            
        except Exception as e:
            print(f"⚠️  获取 {symbol} 报价失败: {e}")
            return None
    
    def get_historical(self, symbol: str, period: str = "1mo") -> List[HistoricalData]:
        """获取历史数据"""
        try:
            endpoint = f"/v8/finance/chart/{symbol}"
            
            # 转换period为interval和range
            interval = "1d"
            range_map = {
                "1d": "1d", "5d": "5d", "1mo": "1mo",
                "3mo": "3mo", "6mo": "6mo", "1y": "1y",
                "2y": "2y", "5y": "5y", "max": "max"
            }
            range_val = range_map.get(period, "1mo")
            
            params = {
                "interval": interval,
                "range": range_val,
                "includeAdjustedClose": "true"
            }
            
            data = self._make_request(endpoint, params)
            
            if "chart" not in data or "result" not in data["chart"] or not data["chart"]["result"]:
                return []
            
            result = data["chart"]["result"][0]
            timestamps = result.get("timestamp", [])
            quote_data = result.get("indicators", {}).get("quote", [{}])[0]
            adjclose_data = result.get("indicators", {}).get("adjclose", [{}])
            
            opens = quote_data.get("open", [])
            highs = quote_data.get("high", [])
            lows = quote_data.get("low", [])
            closes = quote_data.get("close", [])
            volumes = quote_data.get("volume", [])
            adj_closes = adjclose_data[0].get("adjclose", []) if adjclose_data else []
            
            historical = []
            for i in range(len(timestamps)):
                if closes[i] is None:
                    continue
                
                historical.append(HistoricalData(
                    date=datetime.fromtimestamp(timestamps[i]),
                    open=opens[i] if opens[i] is not None else closes[i],
                    high=highs[i] if highs[i] is not None else closes[i],
                    low=lows[i] if lows[i] is not None else closes[i],
                    close=closes[i],
                    volume=int(volumes[i]) if volumes[i] is not None else 0,
                    adj_close=adj_closes[i] if adj_closes and i < len(adj_closes) else None,
                ))
            
            return historical
            
        except Exception as e:
            print(f"⚠️  获取 {symbol} 历史数据失败: {e}")
            return []
    
    def get_market_overview(self) -> List[MarketOverview]:
        """获取市场概览"""
        indices = [
            ("^GSPC", "标普500"),
            ("^DJI", "道琼斯"),
            ("^IXIC", "纳斯达克"),
            ("^FTSE", "富时100"),
            ("^N225", "日经225"),
            ("000001.SS", "上证指数"),
            ("^HSI", "恒生指数"),
        ]
        
        overviews = []
        for symbol, name in indices:
            try:
                quote = self.get_quote(symbol)
                if quote:
                    overviews.append(MarketOverview(
                        index_name=name,
                        symbol=symbol,
                        price=quote.price,
                        change=quote.change,
                        change_percent=quote.change_percent,
                    ))
            except Exception:
                continue
        
        return overviews
    
    def search_symbols(self, query: str) -> List[Dict]:
        """搜索股票代码"""
        try:
            endpoint = "/v1/finance/search"
            params = {
                "q": query,
                "quotesCount": 10,
                "newsCount": 0,
            }
            
            data = self._make_request(endpoint, params)
            
            quotes = data.get("quotes", [])
            results = []
            for quote in quotes:
                results.append({
                    "symbol": quote.get("symbol", ""),
                    "name": quote.get("shortname", quote.get("longname", "")),
                    "exchange": quote.get("exchange", ""),
                    "type": quote.get("quoteType", ""),
                })
            
            return results
            
        except Exception as e:
            print(f"⚠️  搜索失败: {e}")
            return []


class DataSourceManager:
    """数据源管理器"""
    
    def __init__(self):
        self.sources: Dict[str, BaseDataSource] = {}
        self._init_sources()
    
    def _init_sources(self):
        """初始化数据源"""
        config = get_config()
        
        for ds_config in config.get_enabled_data_sources():
            if ds_config.name == "yahoo":
                self.sources["yahoo"] = YahooFinanceSource()
            # 可以扩展更多数据源
    
    def get_source(self, name: str) -> Optional[BaseDataSource]:
        """获取指定数据源"""
        return self.sources.get(name)
    
    def get_primary_source(self) -> Optional[BaseDataSource]:
        """获取主数据源"""
        if "yahoo" in self.sources:
            return self.sources["yahoo"]
        return next(iter(self.sources.values())) if self.sources else None
    
    def get_quote(self, symbol: str, source_name: Optional[str] = None) -> Optional[StockQuote]:
        """获取股票报价"""
        if source_name:
            source = self.get_source(source_name)
            if source:
                return source.get_quote(symbol)
            return None
        
        # 尝试所有数据源
        for source in self.sources.values():
            quote = source.get_quote(symbol)
            if quote:
                return quote
        
        return None
    
    def get_historical(self, symbol: str, period: str = "1mo", 
                       source_name: Optional[str] = None) -> List[HistoricalData]:
        """获取历史数据"""
        if source_name:
            source = self.get_source(source_name)
            if source:
                return source.get_historical(symbol, period)
            return []
        
        for source in self.sources.values():
            data = source.get_historical(symbol, period)
            if data:
                return data
        
        return []
    
    def get_market_overview(self) -> List[MarketOverview]:
        """获取市场概览"""
        for source in self.sources.values():
            overview = source.get_market_overview()
            if overview:
                return overview
        return []
    
    def search_symbols(self, query: str) -> List[Dict]:
        """搜索股票代码"""
        for source in self.sources.values():
            results = source.search_symbols(query)
            if results:
                return results
        return []
