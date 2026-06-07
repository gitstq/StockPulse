"""
StockPulse 自选股管理模块
Watchlist management for StockPulse
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict

from .models import WatchlistItem, StockAlert, AlertType


class WatchlistManager:
    """自选股管理器"""
    
    DEFAULT_WATCHLIST_PATH = Path.home() / ".stockpulse" / "watchlist.json"
    
    def __init__(self, watchlist_path: Optional[str] = None):
        self.watchlist_path = Path(watchlist_path) if watchlist_path else self.DEFAULT_WATCHLIST_PATH
        self.watchlist: Dict[str, WatchlistItem] = {}
        self._load_watchlist()
    
    def _load_watchlist(self):
        """从文件加载自选股列表"""
        if self.watchlist_path.exists():
            try:
                with open(self.watchlist_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                for item_data in data.get("watchlist", []):
                    item = WatchlistItem(
                        symbol=item_data["symbol"],
                        name=item_data.get("name", ""),
                        added_at=datetime.fromisoformat(item_data["added_at"]),
                        notes=item_data.get("notes", ""),
                    )
                    self.watchlist[item.symbol] = item
                    
            except Exception as e:
                print(f"⚠️  加载自选股列表失败: {e}")
    
    def save_watchlist(self):
        """保存自选股列表到文件"""
        self.watchlist_path.parent.mkdir(parents=True, exist_ok=True)
        
        data = {
            "updated_at": datetime.now().isoformat(),
            "watchlist": [item.to_dict() for item in self.watchlist.values()],
        }
        
        with open(self.watchlist_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def add_stock(self, symbol: str, name: str = "", notes: str = "") -> bool:
        """添加股票到自选股"""
        symbol = symbol.upper().strip()
        
        if symbol in self.watchlist:
            print(f"⚠️  {symbol} 已在自选股列表中")
            return False
        
        if len(self.watchlist) >= 50:
            print("⚠️  自选股数量已达上限 (50)")
            return False
        
        self.watchlist[symbol] = WatchlistItem(
            symbol=symbol,
            name=name,
            notes=notes,
        )
        
        self.save_watchlist()
        print(f"✅ 已添加 {symbol} 到自选股")
        return True
    
    def remove_stock(self, symbol: str) -> bool:
        """从自选股中移除股票"""
        symbol = symbol.upper().strip()
        
        if symbol not in self.watchlist:
            print(f"⚠️  {symbol} 不在自选股列表中")
            return False
        
        del self.watchlist[symbol]
        self.save_watchlist()
        print(f"✅ 已从自选股中移除 {symbol}")
        return True
    
    def get_watchlist(self) -> List[WatchlistItem]:
        """获取自选股列表"""
        return list(self.watchlist.values())
    
    def get_symbols(self) -> List[str]:
        """获取自选股代码列表"""
        return list(self.watchlist.keys())
    
    def is_in_watchlist(self, symbol: str) -> bool:
        """检查股票是否在自选股中"""
        return symbol.upper().strip() in self.watchlist
    
    def update_notes(self, symbol: str, notes: str) -> bool:
        """更新股票备注"""
        symbol = symbol.upper().strip()
        
        if symbol not in self.watchlist:
            return False
        
        self.watchlist[symbol].notes = notes
        self.save_watchlist()
        return True
    
    def add_alert(self, symbol: str, alert_type: AlertType, 
                  threshold: float, message: str = "") -> bool:
        """添加预警"""
        symbol = symbol.upper().strip()
        
        if symbol not in self.watchlist:
            print(f"⚠️  {symbol} 不在自选股列表中")
            return False
        
        alert = StockAlert(
            symbol=symbol,
            alert_type=alert_type,
            message=message or f"{alert_type.value} 阈值: {threshold}",
            trigger_value=0.0,
            threshold=threshold,
        )
        
        self.watchlist[symbol].alerts.append(alert)
        self.save_watchlist()
        print(f"✅ 已为 {symbol} 添加 {alert_type.value} 预警")
        return True
    
    def remove_alert(self, symbol: str, alert_index: int) -> bool:
        """移除预警"""
        symbol = symbol.upper().strip()
        
        if symbol not in self.watchlist:
            return False
        
        alerts = self.watchlist[symbol].alerts
        if alert_index < 0 or alert_index >= len(alerts):
            return False
        
        del alerts[alert_index]
        self.save_watchlist()
        return True
    
    def clear_watchlist(self):
        """清空自选股列表"""
        self.watchlist.clear()
        self.save_watchlist()
        print("✅ 已清空自选股列表")
    
    def get_watchlist_size(self) -> int:
        """获取自选股数量"""
        return len(self.watchlist)
