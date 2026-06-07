"""
StockPulse 数据源测试
Tests for StockPulse data sources
"""

import pytest
from unittest.mock import Mock, patch
from src.data_source import YahooFinanceSource, DataSourceManager
from src.models import StockQuote, HistoricalData, MarketOverview


class TestYahooFinanceSource:
    """测试Yahoo Finance数据源"""
    
    def test_initialization(self):
        """测试初始化"""
        source = YahooFinanceSource()
        assert source.name == "yahoo"
        assert source.base_url == "https://query1.finance.yahoo.com"
    
    @patch('src.data_source.requests.Session.get')
    def test_get_quote_success(self, mock_get):
        """测试获取报价成功"""
        # 模拟响应
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "chart": {
                "result": [{
                    "meta": {
                        "shortName": "Apple Inc.",
                        "currency": "USD",
                        "previousClose": 148.0,
                    },
                    "timestamp": [1609459200],
                    "indicators": {
                        "quote": [{
                            "close": [150.0],
                            "open": [148.5],
                            "high": [151.0],
                            "low": [147.0],
                            "volume": [1000000],
                        }]
                    }
                }]
            }
        }
        mock_get.return_value = mock_response
        
        source = YahooFinanceSource()
        quote = source.get_quote("AAPL")
        
        assert quote is not None
        assert quote.symbol == "AAPL"
        assert quote.price == 150.0
    
    @patch('src.data_source.requests.Session.get')
    def test_get_quote_failure(self, mock_get):
        """测试获取报价失败"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        mock_get.side_effect = Exception("Network error")
        
        source = YahooFinanceSource()
        quote = source.get_quote("INVALID")
        
        assert quote is None
    
    @patch('src.data_source.requests.Session.get')
    def test_get_historical(self, mock_get):
        """测试获取历史数据"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "chart": {
                "result": [{
                    "timestamp": [1609459200, 1609545600],
                    "indicators": {
                        "quote": [{
                            "close": [100.0, 101.0],
                            "open": [99.0, 100.0],
                            "high": [101.0, 102.0],
                            "low": [98.0, 99.0],
                            "volume": [1000000, 1100000],
                        }]
                    }
                }]
            }
        }
        mock_get.return_value = mock_response
        
        source = YahooFinanceSource()
        historical = source.get_historical("AAPL", "1mo")
        
        assert len(historical) == 2
        assert historical[0].close == 100.0
        assert historical[1].close == 101.0
    
    @patch('src.data_source.requests.Session.get')
    def test_search_symbols(self, mock_get):
        """测试搜索股票"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "quotes": [
                {"symbol": "AAPL", "shortname": "Apple Inc.", "exchange": "NASDAQ"},
                {"symbol": "AAP", "shortname": "Advance Auto Parts", "exchange": "NYSE"},
            ]
        }
        mock_get.return_value = mock_response
        
        source = YahooFinanceSource()
        results = source.search_symbols("AAPL")
        
        assert len(results) == 2
        assert results[0]["symbol"] == "AAPL"


class TestDataSourceManager:
    """测试数据源管理器"""
    
    def test_initialization(self):
        """测试初始化"""
        manager = DataSourceManager()
        assert manager.get_primary_source() is not None
    
    @patch.object(YahooFinanceSource, 'get_quote')
    def test_get_quote(self, mock_get_quote):
        """测试获取报价"""
        mock_quote = StockQuote(symbol="AAPL", price=150.0)
        mock_get_quote.return_value = mock_quote
        
        manager = DataSourceManager()
        quote = manager.get_quote("AAPL")
        
        assert quote is not None
        assert quote.symbol == "AAPL"
    
    @patch.object(YahooFinanceSource, 'get_historical')
    def test_get_historical(self, mock_get_historical):
        """测试获取历史数据"""
        mock_data = [
            HistoricalData(
                date=__import__('datetime').datetime.now(),
                open=100.0, high=101.0, low=99.0, close=100.5, volume=1000000
            )
        ]
        mock_get_historical.return_value = mock_data
        
        manager = DataSourceManager()
        historical = manager.get_historical("AAPL")
        
        assert len(historical) == 1
        assert historical[0].close == 100.5
