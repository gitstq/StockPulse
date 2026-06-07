"""
StockPulse 分析器模块
Stock analysis and insight generation for StockPulse
"""

import numpy as np
from typing import List, Optional, Dict
from datetime import datetime, timedelta

from .models import HistoricalData, StockInsight, StockQuote


class TechnicalAnalyzer:
    """技术分析器"""
    
    @staticmethod
    def calculate_sma(data: List[HistoricalData], period: int) -> List[float]:
        """计算简单移动平均线 (SMA)"""
        closes = [d.close for d in data]
        if len(closes) < period:
            return []
        
        sma = []
        for i in range(len(closes)):
            if i < period - 1:
                sma.append(None)
            else:
                sma.append(np.mean(closes[i - period + 1:i + 1]))
        return sma
    
    @staticmethod
    def calculate_ema(data: List[HistoricalData], period: int) -> List[float]:
        """计算指数移动平均线 (EMA)"""
        closes = [d.close for d in data]
        if len(closes) < period:
            return []
        
        multiplier = 2 / (period + 1)
        ema = [np.mean(closes[:period])]
        
        for i in range(period, len(closes)):
            ema.append((closes[i] - ema[-1]) * multiplier + ema[-1])
        
        # 补齐前面的None
        result = [None] * (period - 1) + ema
        return result
    
    @staticmethod
    def calculate_rsi(data: List[HistoricalData], period: int = 14) -> List[float]:
        """计算相对强弱指标 (RSI)"""
        closes = [d.close for d in data]
        if len(closes) < period + 1:
            return []
        
        deltas = np.diff(closes)
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)
        
        avg_gains = []
        avg_losses = []
        
        # 初始平均值
        avg_gains.append(np.mean(gains[:period]))
        avg_losses.append(np.mean(losses[:period]))
        
        # 平滑处理
        for i in range(period, len(gains)):
            avg_gains.append((avg_gains[-1] * (period - 1) + gains[i]) / period)
            avg_losses.append((avg_losses[-1] * (period - 1) + losses[i]) / period)
        
        rsi = []
        for i in range(len(avg_gains)):
            if avg_losses[i] == 0:
                rsi.append(100.0)
            else:
                rs = avg_gains[i] / avg_losses[i]
                rsi.append(100 - (100 / (1 + rs)))
        
        # 补齐
        result = [None] * period + rsi
        return result
    
    @staticmethod
    def calculate_macd(data: List[HistoricalData], 
                       fast: int = 12, slow: int = 26, signal: int = 9) -> Dict:
        """计算MACD指标"""
        closes = [d.close for d in data]
        if len(closes) < slow:
            return {"macd": [], "signal": [], "histogram": []}
        
        ema_fast = TechnicalAnalyzer.calculate_ema(data, fast)
        ema_slow = TechnicalAnalyzer.calculate_ema(data, slow)
        
        # 过滤None值
        valid_fast = [x for x in ema_fast if x is not None]
        valid_slow = [x for x in ema_slow if x is not None]
        
        if len(valid_fast) != len(valid_slow):
            min_len = min(len(valid_fast), len(valid_slow))
            valid_fast = valid_fast[-min_len:]
            valid_slow = valid_slow[-min_len:]
        
        macd_line = [f - s for f, s in zip(valid_fast, valid_slow)]
        
        # 计算信号线 (EMA of MACD)
        if len(macd_line) < signal:
            return {"macd": macd_line, "signal": [], "histogram": []}
        
        signal_line = [np.mean(macd_line[:signal])]
        multiplier = 2 / (signal + 1)
        for i in range(signal, len(macd_line)):
            signal_line.append((macd_line[i] - signal_line[-1]) * multiplier + signal_line[-1])
        
        # 补齐
        signal_padded = [None] * (slow - signal) + signal_line
        
        # 计算柱状图
        histogram = []
        for i in range(len(macd_line)):
            si = i - (slow - signal)
            if si >= 0 and si < len(signal_line):
                histogram.append(macd_line[i] - signal_line[si])
            else:
                histogram.append(None)
        
        return {
            "macd": macd_line,
            "signal": signal_line,
            "histogram": histogram,
        }
    
    @staticmethod
    def calculate_bollinger_bands(data: List[HistoricalData], 
                                   period: int = 20, 
                                   std_dev: float = 2.0) -> Dict:
        """计算布林带"""
        closes = [d.close for d in data]
        if len(closes) < period:
            return {"upper": [], "middle": [], "lower": []}
        
        sma = TechnicalAnalyzer.calculate_sma(data, period)
        
        upper = []
        lower = []
        
        for i in range(len(closes)):
            if i < period - 1:
                upper.append(None)
                lower.append(None)
            else:
                std = np.std(closes[i - period + 1:i + 1])
                upper.append(sma[i] + std_dev * std)
                lower.append(sma[i] - std_dev * std)
        
        return {
            "upper": upper,
            "middle": sma,
            "lower": lower,
        }
    
    @staticmethod
    def find_support_resistance(data: List[HistoricalData], 
                                 lookback: int = 20) -> Dict:
        """寻找支撑位和阻力位"""
        if len(data) < lookback:
            return {"support": None, "resistance": None}
        
        recent = data[-lookback:]
        lows = [d.low for d in recent]
        highs = [d.high for d in recent]
        
        # 简单方法：使用近期最低和最高
        support = min(lows)
        resistance = max(highs)
        
        return {
            "support": round(support, 2),
            "resistance": round(resistance, 2),
        }


class InsightGenerator:
    """洞察生成器"""
    
    @staticmethod
    def generate_insight(symbol: str, 
                         quote: StockQuote, 
                         historical: List[HistoricalData]) -> StockInsight:
        """生成股票洞察分析"""
        if not historical or len(historical) < 30:
            return StockInsight(
                symbol=symbol,
                overall_rating="数据不足",
                recommendation="请提供更多历史数据",
            )
        
        # 技术面评分
        technical_score = InsightGenerator._calculate_technical_score(historical)
        
        # 基本面评分 (基于可用数据)
        fundamental_score = InsightGenerator._calculate_fundamental_score(quote)
        
        # 情绪面评分
        sentiment_score = InsightGenerator._calculate_sentiment_score(historical)
        
        # 综合评分
        overall = (technical_score + fundamental_score + sentiment_score) / 3
        
        # 确定评级
        if overall >= 70:
            rating = "强烈看好"
            recommendation = "买入"
        elif overall >= 55:
            rating = "看好"
            recommendation = "考虑买入"
        elif overall >= 45:
            rating = "中性"
            recommendation = "观望"
        elif overall >= 30:
            rating = "看淡"
            recommendation = "考虑卖出"
        else:
            rating = "强烈看淡"
            recommendation = "卖出"
        
        # 寻找支撑阻力位
        sr = TechnicalAnalyzer.find_support_resistance(historical)
        
        # 生成分析摘要
        summary = InsightGenerator._generate_summary(
            symbol, quote, technical_score, fundamental_score, sentiment_score
        )
        
        return StockInsight(
            symbol=symbol,
            technical_score=round(technical_score, 1),
            fundamental_score=round(fundamental_score, 1),
            sentiment_score=round(sentiment_score, 1),
            overall_rating=rating,
            support_level=sr.get("support"),
            resistance_level=sr.get("resistance"),
            recommendation=recommendation,
            analysis_summary=summary,
        )
    
    @staticmethod
    def _calculate_technical_score(historical: List[HistoricalData]) -> float:
        """计算技术面评分"""
        score = 50.0
        
        # RSI分析
        rsi_values = TechnicalAnalyzer.calculate_rsi(historical)
        valid_rsi = [r for r in rsi_values if r is not None]
        
        if valid_rsi:
            latest_rsi = valid_rsi[-1]
            if latest_rsi < 30:
                score += 15  # 超卖，可能反弹
            elif latest_rsi > 70:
                score -= 15  # 超买，可能回调
            elif 40 <= latest_rsi <= 60:
                score += 5   # 健康区间
        
        # 趋势分析 (价格 vs SMA)
        sma_20 = TechnicalAnalyzer.calculate_sma(historical, 20)
        valid_sma = [s for s in sma_20 if s is not None]
        
        if valid_sma and len(historical) > 0:
            current_price = historical[-1].close
            latest_sma = valid_sma[-1]
            
            if current_price > latest_sma * 1.05:
                score += 10  # 强势上涨
            elif current_price > latest_sma:
                score += 5   # 上涨
            elif current_price < latest_sma * 0.95:
                score -= 10  # 强势下跌
            elif current_price < latest_sma:
                score -= 5   # 下跌
        
        # 成交量分析
        recent_volume = historical[-5:]
        if len(recent_volume) >= 5:
            avg_volume = np.mean([d.volume for d in historical[-20:]])
            latest_volume = recent_volume[-1].volume
            
            if avg_volume > 0:
                vol_ratio = latest_volume / avg_volume
                if vol_ratio > 2:
                    score += 5  # 放量
                elif vol_ratio < 0.5:
                    score -= 5  # 缩量
        
        return max(0, min(100, score))
    
    @staticmethod
    def _calculate_fundamental_score(quote: StockQuote) -> float:
        """计算基本面评分"""
        score = 50.0
        
        # 市盈率分析
        if quote.pe_ratio:
            if quote.pe_ratio < 10:
                score += 15  # 低估值
            elif quote.pe_ratio < 20:
                score += 10
            elif quote.pe_ratio > 50:
                score -= 10  # 高估值
            elif quote.pe_ratio > 100:
                score -= 20
        
        # 涨跌幅分析
        if quote.change_percent > 5:
            score += 5   # 强势
        elif quote.change_percent < -5:
            score -= 5   # 弱势
        
        return max(0, min(100, score))
    
    @staticmethod
    def _calculate_sentiment_score(historical: List[HistoricalData]) -> float:
        """计算情绪面评分"""
        score = 50.0
        
        if len(historical) < 5:
            return score
        
        # 近期趋势
        recent = historical[-5:]
        closes = [d.close for d in recent]
        
        if len(closes) >= 2:
            if closes[-1] > closes[0]:
                score += 10  # 近期上涨
            else:
                score -= 10  # 近期下跌
        
        # 波动性分析
        if len(historical) >= 20:
            returns = []
            for i in range(1, min(21, len(historical))):
                ret = (historical[-i].close - historical[-i-1].close) / historical[-i-1].close
                returns.append(ret)
            
            volatility = np.std(returns) * np.sqrt(252) * 100  # 年化波动率
            
            if volatility > 50:
                score -= 5  # 高波动，风险大
            elif volatility < 20:
                score += 5  # 低波动，稳定
        
        return max(0, min(100, score))
    
    @staticmethod
    def _generate_summary(symbol: str, quote: StockQuote, 
                          technical: float, fundamental: float, 
                          sentiment: float) -> str:
        """生成分析摘要"""
        parts = []
        
        parts.append(f"📊 {symbol} 当前价格: {quote.price} {quote.currency}")
        
        if quote.change >= 0:
            parts.append(f"📈 今日上涨 {quote.change_percent}%")
        else:
            parts.append(f"📉 今日下跌 {abs(quote.change_percent)}%")
        
        parts.append(f"🔧 技术面评分: {technical:.1f}/100")
        parts.append(f"📋 基本面评分: {fundamental:.1f}/100")
        parts.append(f"😊 情绪面评分: {sentiment:.1f}/100")
        
        avg = (technical + fundamental + sentiment) / 3
        parts.append(f"📊 综合评分: {avg:.1f}/100")
        
        return "\n".join(parts)
