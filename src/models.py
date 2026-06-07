"""
StockPulse 数据模型模块
Data models for StockPulse
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Dict
from enum import Enum


class MarketStatus(Enum):
    """市场状态"""
    PRE_MARKET = "盘前"
    OPEN = "交易中"
    CLOSED = "已收盘"
    AFTER_HOURS = "盘后"
    HALTED = "停牌"


class AlertType(Enum):
    """预警类型"""
    PRICE_UP = "价格上涨"
    PRICE_DOWN = "价格下跌"
    VOLUME_SPIKE = "成交量突增"
    PRICE_TARGET = "价格目标达成"


@dataclass
class StockQuote:
    """股票报价数据"""
    symbol: str                          # 股票代码
    name: str = ""                       # 股票名称
    price: float = 0.0                   # 当前价格
    change: float = 0.0                  # 涨跌额
    change_percent: float = 0.0          # 涨跌幅百分比
    volume: int = 0                      # 成交量
    avg_volume: int = 0                  # 平均成交量
    market_cap: Optional[float] = None   # 市值
    pe_ratio: Optional[float] = None     # 市盈率
    high: float = 0.0                    # 当日最高
    low: float = 0.0                     # 当日最低
    open: float = 0.0                    # 开盘价
    previous_close: float = 0.0          # 昨收
    fifty_two_week_high: Optional[float] = None  # 52周最高
    fifty_two_week_low: Optional[float] = None   # 52周最低
    timestamp: datetime = field(default_factory=datetime.now)  # 数据时间
    currency: str = "USD"                # 货币
    market_status: MarketStatus = MarketStatus.OPEN  # 市场状态
    
    @property
    def is_positive(self) -> bool:
        """是否上涨"""
        return self.change >= 0
    
    @property
    def volume_ratio(self) -> float:
        """成交量比率"""
        if self.avg_volume > 0:
            return self.volume / self.avg_volume
        return 0.0
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "symbol": self.symbol,
            "name": self.name,
            "price": self.price,
            "change": self.change,
            "change_percent": self.change_percent,
            "volume": self.volume,
            "avg_volume": self.avg_volume,
            "market_cap": self.market_cap,
            "pe_ratio": self.pe_ratio,
            "high": self.high,
            "low": self.low,
            "open": self.open,
            "previous_close": self.previous_close,
            "fifty_two_week_high": self.fifty_two_week_high,
            "fifty_two_week_low": self.fifty_two_week_low,
            "timestamp": self.timestamp.isoformat(),
            "currency": self.currency,
            "market_status": self.market_status.value,
            "is_positive": self.is_positive,
            "volume_ratio": self.volume_ratio,
        }


@dataclass
class HistoricalData:
    """历史数据点"""
    date: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int
    adj_close: Optional[float] = None
    
    def to_dict(self) -> Dict:
        return {
            "date": self.date.isoformat(),
            "open": self.open,
            "high": self.high,
            "low": self.low,
            "close": self.close,
            "volume": self.volume,
            "adj_close": self.adj_close,
        }


@dataclass
class StockAlert:
    """股票预警"""
    symbol: str
    alert_type: AlertType
    message: str
    trigger_value: float
    threshold: float
    timestamp: datetime = field(default_factory=datetime.now)
    is_triggered: bool = False
    
    def to_dict(self) -> Dict:
        return {
            "symbol": self.symbol,
            "alert_type": self.alert_type.value,
            "message": self.message,
            "trigger_value": self.trigger_value,
            "threshold": self.threshold,
            "timestamp": self.timestamp.isoformat(),
            "is_triggered": self.is_triggered,
        }


@dataclass
class WatchlistItem:
    """自选股项目"""
    symbol: str
    name: str = ""
    added_at: datetime = field(default_factory=datetime.now)
    notes: str = ""
    alerts: List[StockAlert] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            "symbol": self.symbol,
            "name": self.name,
            "added_at": self.added_at.isoformat(),
            "notes": self.notes,
            "alerts": [alert.to_dict() for alert in self.alerts],
        }


@dataclass
class MarketOverview:
    """市场概览"""
    index_name: str
    symbol: str
    price: float
    change: float
    change_percent: float
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict:
        return {
            "index_name": self.index_name,
            "symbol": self.symbol,
            "price": self.price,
            "change": self.change,
            "change_percent": self.change_percent,
            "timestamp": self.timestamp.isoformat(),
        }


@dataclass
class StockInsight:
    """股票洞察分析"""
    symbol: str
    technical_score: float = 0.0      # 技术面评分 (0-100)
    fundamental_score: float = 0.0    # 基本面评分 (0-100)
    sentiment_score: float = 0.0      # 情绪面评分 (0-100)
    overall_rating: str = "中性"       # 综合评级
    support_level: Optional[float] = None    # 支撑位
    resistance_level: Optional[float] = None # 阻力位
    recommendation: str = "观望"       # 操作建议
    analysis_summary: str = ""         # 分析摘要
    
    def to_dict(self) -> Dict:
        return {
            "symbol": self.symbol,
            "technical_score": self.technical_score,
            "fundamental_score": self.fundamental_score,
            "sentiment_score": self.sentiment_score,
            "overall_rating": self.overall_rating,
            "support_level": self.support_level,
            "resistance_level": self.resistance_level,
            "recommendation": self.recommendation,
            "analysis_summary": self.analysis_summary,
        }
