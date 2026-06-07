"""
StockPulse 模型测试
Tests for StockPulse models
"""

import pytest
from datetime import datetime
from src.models import (
    StockQuote, HistoricalData, StockAlert, 
    WatchlistItem, MarketOverview, StockInsight,
    MarketStatus, AlertType
)


class TestStockQuote:
    """测试股票报价模型"""
    
    def test_basic_creation(self):
        """测试基本创建"""
        quote = StockQuote(
            symbol="AAPL",
            name="Apple Inc.",
            price=150.0,
            change=2.5,
            change_percent=1.69,
        )
        
        assert quote.symbol == "AAPL"
        assert quote.name == "Apple Inc."
        assert quote.price == 150.0
        assert quote.is_positive == True
    
    def test_negative_change(self):
        """测试下跌情况"""
        quote = StockQuote(
            symbol="TSLA",
            price=200.0,
            change=-5.0,
            change_percent=-2.44,
        )
        
        assert quote.is_positive == False
        assert quote.change == -5.0
    
    def test_to_dict(self):
        """测试字典转换"""
        quote = StockQuote(
            symbol="GOOGL",
            price=2800.0,
            change=10.0,
            volume=1000000,
        )
        
        data = quote.to_dict()
        assert data["symbol"] == "GOOGL"
        assert data["price"] == 2800.0
        assert data["is_positive"] == True


class TestHistoricalData:
    """测试历史数据模型"""
    
    def test_creation(self):
        """测试创建"""
        data = HistoricalData(
            date=datetime(2024, 1, 1),
            open=100.0,
            high=105.0,
            low=98.0,
            close=103.0,
            volume=1000000,
        )
        
        assert data.close == 103.0
        assert data.volume == 1000000


class TestStockInsight:
    """测试股票洞察模型"""
    
    def test_creation(self):
        """测试创建"""
        insight = StockInsight(
            symbol="AAPL",
            technical_score=75.0,
            fundamental_score=80.0,
            sentiment_score=65.0,
            overall_rating="看好",
            recommendation="买入",
        )
        
        assert insight.symbol == "AAPL"
        assert insight.overall_rating == "看好"
        assert insight.recommendation == "买入"
    
    def test_to_dict(self):
        """测试字典转换"""
        insight = StockInsight(
            symbol="MSFT",
            technical_score=70.0,
            overall_rating="中性",
        )
        
        data = insight.to_dict()
        assert data["symbol"] == "MSFT"
        assert data["technical_score"] == 70.0


class TestWatchlistItem:
    """测试自选股项目模型"""
    
    def test_creation(self):
        """测试创建"""
        item = WatchlistItem(
            symbol="AAPL",
            name="Apple Inc.",
            notes="科技巨头",
        )
        
        assert item.symbol == "AAPL"
        assert item.notes == "科技巨头"
    
    def test_with_alerts(self):
        """测试带预警的自选股"""
        alert = StockAlert(
            symbol="AAPL",
            alert_type=AlertType.PRICE_UP,
            threshold=160.0,
        )
        
        item = WatchlistItem(
            symbol="AAPL",
            alerts=[alert],
        )
        
        assert len(item.alerts) == 1
        assert item.alerts[0].alert_type == AlertType.PRICE_UP
