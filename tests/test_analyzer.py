"""
StockPulse 分析器测试
Tests for StockPulse analyzer
"""

import pytest
from datetime import datetime, timedelta
from src.analyzer import TechnicalAnalyzer, InsightGenerator
from src.models import StockQuote, HistoricalData, StockInsight


class TestTechnicalAnalyzer:
    """测试技术分析器"""
    
    def create_sample_data(self, days=30):
        """创建样本历史数据"""
        data = []
        base_price = 100.0
        
        for i in range(days):
            date = datetime.now() - timedelta(days=days-i)
            # 模拟价格波动
            price = base_price + (i * 0.5) + (i % 5 - 2) * 2
            
            data.append(HistoricalData(
                date=date,
                open=price - 1,
                high=price + 2,
                low=price - 2,
                close=price,
                volume=1000000 + i * 1000,
            ))
        
        return data
    
    def test_calculate_sma(self):
        """测试SMA计算"""
        data = self.create_sample_data(30)
        sma = TechnicalAnalyzer.calculate_sma(data, 10)
        
        # 前9个应该是None
        assert all(x is None for x in sma[:9])
        # 第10个开始应该有值
        assert sma[9] is not None
        assert isinstance(sma[9], float)
    
    def test_calculate_rsi(self):
        """测试RSI计算"""
        data = self.create_sample_data(30)
        rsi = TechnicalAnalyzer.calculate_rsi(data)
        
        # RSI应该在0-100之间
        valid_rsi = [r for r in rsi if r is not None]
        assert len(valid_rsi) > 0
        assert all(0 <= r <= 100 for r in valid_rsi)
    
    def test_calculate_bollinger_bands(self):
        """测试布林带计算"""
        data = self.create_sample_data(30)
        bands = TechnicalAnalyzer.calculate_bollinger_bands(data, 20)
        
        assert "upper" in bands
        assert "middle" in bands
        assert "lower" in bands
        
        # 检查上轨 > 中轨 > 下轨
        for i in range(20, len(data)):
            if bands["upper"][i] is not None:
                assert bands["upper"][i] >= bands["middle"][i]
                assert bands["middle"][i] >= bands["lower"][i]
    
    def test_find_support_resistance(self):
        """测试支撑阻力位"""
        data = self.create_sample_data(30)
        sr = TechnicalAnalyzer.find_support_resistance(data)
        
        assert "support" in sr
        assert "resistance" in sr
        
        if sr["support"] and sr["resistance"]:
            assert sr["resistance"] >= sr["support"]


class TestInsightGenerator:
    """测试洞察生成器"""
    
    def create_sample_data(self, days=30):
        """创建样本历史数据"""
        data = []
        base_price = 100.0
        
        for i in range(days):
            date = datetime.now() - timedelta(days=days-i)
            price = base_price + (i * 0.5)
            
            data.append(HistoricalData(
                date=date,
                open=price - 1,
                high=price + 2,
                low=price - 2,
                close=price,
                volume=1000000,
            ))
        
        return data
    
    def test_generate_insight(self):
        """测试生成洞察"""
        quote = StockQuote(
            symbol="AAPL",
            name="Apple Inc.",
            price=150.0,
            change=2.0,
            change_percent=1.35,
            pe_ratio=25.0,
        )
        
        historical = self.create_sample_data(30)
        insight = InsightGenerator.generate_insight("AAPL", quote, historical)
        
        assert isinstance(insight, StockInsight)
        assert insight.symbol == "AAPL"
        assert 0 <= insight.technical_score <= 100
        assert 0 <= insight.fundamental_score <= 100
        assert 0 <= insight.sentiment_score <= 100
        assert insight.overall_rating in ["强烈看好", "看好", "中性", "看淡", "强烈看淡"]
    
    def test_insufficient_data(self):
        """测试数据不足的情况"""
        quote = StockQuote(symbol="AAPL", price=150.0)
        historical = self.create_sample_data(10)  # 少于30天
        
        insight = InsightGenerator.generate_insight("AAPL", quote, historical)
        
        assert insight.overall_rating == "数据不足"
    
    def test_calculate_technical_score(self):
        """测试技术面评分"""
        historical = self.create_sample_data(30)
        score = InsightGenerator._calculate_technical_score(historical)
        
        assert 0 <= score <= 100
        assert isinstance(score, float)
    
    def test_calculate_fundamental_score(self):
        """测试基本面评分"""
        quote = StockQuote(
            symbol="AAPL",
            pe_ratio=15.0,
            change_percent=3.0,
        )
        
        score = InsightGenerator._calculate_fundamental_score(quote)
        
        assert 0 <= score <= 100
        assert isinstance(score, float)
