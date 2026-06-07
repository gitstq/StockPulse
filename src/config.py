"""
StockPulse 配置管理模块
Configuration management module for StockPulse
"""

import os
import yaml
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, field, asdict


@dataclass
class DataSourceConfig:
    """数据源配置"""
    name: str
    enabled: bool = True
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    rate_limit: int = 60  # 每分钟请求次数限制
    timeout: int = 30


@dataclass
class AlertConfig:
    """预警配置"""
    enabled: bool = True
    price_change_threshold: float = 5.0  # 价格变动百分比阈值
    volume_spike_threshold: float = 3.0  # 成交量突增倍数阈值
    check_interval: int = 60  # 检查间隔（秒）


@dataclass
class DisplayConfig:
    """显示配置"""
    theme: str = "dark"
    refresh_interval: int = 5  # 刷新间隔（秒）
    max_watchlist_size: int = 50  # 最大自选股数量
    default_currency: str = "CNY"
    chart_style: str = "candlestick"


@dataclass
class StockPulseConfig:
    """StockPulse 主配置类"""
    app_name: str = "StockPulse"
    version: str = "1.0.0"
    debug: bool = False
    data_dir: str = "./data"
    log_level: str = "INFO"
    
    # 数据源配置
    data_sources: List[DataSourceConfig] = field(default_factory=lambda: [
        DataSourceConfig(name="yahoo", enabled=True, base_url="https://query1.finance.yahoo.com"),
        DataSourceConfig(name="alpha_vantage", enabled=False, base_url="https://www.alphavantage.co/query"),
        DataSourceConfig(name="tushare", enabled=False, base_url="http://api.tushare.pro"),
    ])
    
    # 预警配置
    alert: AlertConfig = field(default_factory=AlertConfig)
    
    # 显示配置
    display: DisplayConfig = field(default_factory=DisplayConfig)
    
    # 默认自选股列表
    default_watchlist: List[str] = field(default_factory=lambda: [
        "AAPL", "GOOGL", "MSFT", "AMZN", "TSLA",
        "BABA", "TCEHY", "0700.HK"
    ])


class ConfigManager:
    """配置管理器"""
    
    DEFAULT_CONFIG_PATH = Path.home() / ".stockpulse" / "config.yaml"
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = Path(config_path) if config_path else self.DEFAULT_CONFIG_PATH
        self.config = StockPulseConfig()
        self._load_config()
    
    def _load_config(self):
        """从文件加载配置"""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                if data:
                    self._update_config(data)
            except Exception as e:
                print(f"⚠️  加载配置文件失败，使用默认配置: {e}")
    
    def _update_config(self, data: Dict):
        """更新配置"""
        if 'debug' in data:
            self.config.debug = data['debug']
        if 'data_dir' in data:
            self.config.data_dir = data['data_dir']
        if 'log_level' in data:
            self.config.log_level = data['log_level']
        if 'default_watchlist' in data:
            self.config.default_watchlist = data['default_watchlist']
        
        # 更新数据源配置
        if 'data_sources' in data:
            self.config.data_sources = [
                DataSourceConfig(**ds) for ds in data['data_sources']
            ]
        
        # 更新预警配置
        if 'alert' in data:
            self.config.alert = AlertConfig(**data['alert'])
        
        # 更新显示配置
        if 'display' in data:
            self.config.display = DisplayConfig(**data['display'])
    
    def save_config(self):
        """保存配置到文件"""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        
        config_dict = asdict(self.config)
        
        with open(self.config_path, 'w', encoding='utf-8') as f:
            yaml.dump(config_dict, f, allow_unicode=True, default_flow_style=False)
    
    def get_config(self) -> StockPulseConfig:
        """获取当前配置"""
        return self.config
    
    def get_data_source(self, name: str) -> Optional[DataSourceConfig]:
        """获取指定数据源配置"""
        for ds in self.config.data_sources:
            if ds.name == name and ds.enabled:
                return ds
        return None
    
    def get_enabled_data_sources(self) -> List[DataSourceConfig]:
        """获取所有启用的数据源"""
        return [ds for ds in self.config.data_sources if ds.enabled]


# 全局配置实例
_config_manager: Optional[ConfigManager] = None


def get_config() -> StockPulseConfig:
    """获取全局配置"""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager.get_config()


def init_config(config_path: Optional[str] = None) -> ConfigManager:
    """初始化配置"""
    global _config_manager
    _config_manager = ConfigManager(config_path)
    return _config_manager
