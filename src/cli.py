"""
StockPulse 命令行界面模块
Command Line Interface for StockPulse
"""

import click
import sys
from typing import Optional
from datetime import datetime

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.live import Live
from rich import box

from .config import init_config, get_config
from .data_source import DataSourceManager
from .watchlist import WatchlistManager
from .analyzer import InsightGenerator
from .models import AlertType


console = Console()


@click.group()
@click.option('--config', '-c', help='配置文件路径')
@click.pass_context
def cli(ctx, config):
    """🚀 StockPulse - 本地化股票行情追踪与分析平台"""
    ctx.ensure_object(dict)
    
    # 初始化配置
    init_config(config)
    
    # 初始化管理器
    ctx.obj['data_source'] = DataSourceManager()
    ctx.obj['watchlist'] = WatchlistManager()


@cli.command()
@click.argument('symbol')
@click.pass_context
def quote(ctx, symbol):
    """📊 获取股票实时报价"""
    ds = ctx.obj['data_source']
    
    with console.status(f"[bold green]正在获取 {symbol.upper()} 的报价..."):
        quote_data = ds.get_quote(symbol.upper())
    
    if not quote_data:
        console.print(f"[red]❌ 无法获取 {symbol.upper()} 的报价数据[/red]")
        return
    
    # 显示报价信息
    color = "green" if quote_data.is_positive else "red"
    change_icon = "📈" if quote_data.is_positive else "📉"
    
    panel_content = f"""
[bold]{quote_data.name} ({quote_data.symbol})[/bold]

当前价格: [bold {color}]{quote_data.price} {quote_data.currency}[/bold {color}]
涨跌额: [{color}]{change_icon} {quote_data.change:+.2f}[/{color}]
涨跌幅: [{color}]{quote_data.change_percent:+.2f}%[/{color}]

开盘价: {quote_data.open}
最高价: {quote_data.high}
最低价: {quote_data.low}
昨收价: {quote_data.previous_close}
成交量: {quote_data.volume:,}

更新时间: {quote_data.timestamp.strftime('%Y-%m-%d %H:%M:%S')}
    """
    
    console.print(Panel(panel_content, title="📊 股票报价", border_style=color))


@cli.command()
@click.argument('symbol')
@click.option('--period', '-p', default='1mo', 
              type=click.Choice(['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y']),
              help='历史数据周期')
@click.pass_context
def history(ctx, symbol, period):
    """📈 查看股票历史数据"""
    ds = ctx.obj['data_source']
    
    with console.status(f"[bold green]正在获取 {symbol.upper()} 的历史数据..."):
        historical = ds.get_historical(symbol.upper(), period)
    
    if not historical:
        console.print(f"[red]❌ 无法获取 {symbol.upper()} 的历史数据[/red]")
        return
    
    # 创建表格
    table = Table(title=f"📈 {symbol.upper()} 历史数据 ({period})", box=box.ROUNDED)
    table.add_column("日期", style="cyan")
    table.add_column("开盘", justify="right")
    table.add_column("最高", justify="right")
    table.add_column("最低", justify="right")
    table.add_column("收盘", justify="right")
    table.add_column("成交量", justify="right")
    table.add_column("涨跌", justify="right")
    
    for i, data in enumerate(historical):
        change = ""
        if i > 0:
            diff = data.close - historical[i-1].close
            change_pct = (diff / historical[i-1].close * 100) if historical[i-1].close else 0
            if diff >= 0:
                change = f"[green]+{change_pct:.2f}%[/green]"
            else:
                change = f"[red]{change_pct:.2f}%[/red]"
        
        table.add_row(
            data.date.strftime('%Y-%m-%d'),
            f"{data.open:.2f}",
            f"{data.high:.2f}",
            f"{data.low:.2f}",
            f"{data.close:.2f}",
            f"{data.volume:,}",
            change,
        )
    
    console.print(table)
    console.print(f"\n[dim]共 {len(historical)} 条记录[/dim]")


@cli.command()
@click.pass_context
def market(ctx):
    """🌍 查看市场概览"""
    ds = ctx.obj['data_source']
    
    with console.status("[bold green]正在获取市场数据..."):
        overview = ds.get_market_overview()
    
    if not overview:
        console.print("[red]❌ 无法获取市场概览数据[/red]")
        return
    
    table = Table(title="🌍 全球市场概览", box=box.ROUNDED)
    table.add_column("指数", style="cyan")
    table.add_column("代码", style="dim")
    table.add_column("价格", justify="right")
    table.add_column("涨跌", justify="right")
    table.add_column("涨跌幅", justify="right")
    
    for item in overview:
        color = "green" if item.change >= 0 else "red"
        change_icon = "▲" if item.change >= 0 else "▼"
        
        table.add_row(
            item.index_name,
            item.symbol,
            f"{item.price:,.2f}",
            f"[{color}]{change_icon} {item.change:+.2f}[/{color}]",
            f"[{color}]{item.change_percent:+.2f}%[/{color}]",
        )
    
    console.print(table)


@cli.command()
@click.argument('symbol')
@click.pass_context
def insight(ctx, symbol):
    """💡 获取股票智能分析"""
    ds = ctx.obj['data_source']
    symbol = symbol.upper()
    
    with console.status(f"[bold green]正在分析 {symbol}..."):
        quote = ds.get_quote(symbol)
        historical = ds.get_historical(symbol, "3mo")
    
    if not quote:
        console.print(f"[red]❌ 无法获取 {symbol} 的数据[/red]")
        return
    
    if not historical or len(historical) < 30:
        console.print(f"[yellow]⚠️  {symbol} 历史数据不足，无法生成完整分析[/yellow]")
        return
    
    # 生成洞察
    insight_data = InsightGenerator.generate_insight(symbol, quote, historical)
    
    # 显示分析结果
    rating_color = {
        "强烈看好": "bold bright_green",
        "看好": "green",
        "中性": "yellow",
        "看淡": "red",
        "强烈看淡": "bold bright_red",
    }.get(insight_data.overall_rating, "white")
    
    panel_content = f"""
[bold]综合评级: [{rating_color}]{insight_data.overall_rating}[/{rating_color}][/bold]
操作建议: [bold]{insight_data.recommendation}[/bold]

[cyan]评分详情:[/cyan]
  🔧 技术面: {insight_data.technical_score}/100
  📋 基本面: {insight_data.fundamental_score}/100
  😊 情绪面: {insight_data.sentiment_score}/100

[cyan]关键价位:[/cyan]
  📉 支撑位: {insight_data.support_level or 'N/A'}
  📈 阻力位: {insight_data.resistance_level or 'N/A'}

[cyan]分析摘要:[/cyan]
{insight_data.analysis_summary}
    """
    
    console.print(Panel(panel_content, title=f"💡 {symbol} 智能分析", border_style="blue"))


@cli.command()
@click.pass_context
def watchlist(ctx):
    ""️ 查看自选股列表"""
    wl = ctx.obj['watchlist']
    ds = ctx.obj['data_source']
    
    items = wl.get_watchlist()
    
    if not items:
        console.print("[yellow]📭 自选股列表为空，使用 `stockpulse add` 添加股票[/yellow]")
        return
    
    table = Table(title="📋 自选股列表", box=box.ROUNDED)
    table.add_column("代码", style="cyan")
    table.add_column("名称", style="dim")
    table.add_column("价格", justify="right")
    table.add_column("涨跌", justify="right")
    table.add_column("涨跌幅", justify="right")
    table.add_column("备注")
    
    for item in items:
        quote = ds.get_quote(item.symbol)
        
        if quote:
            color = "green" if quote.is_positive else "red"
            table.add_row(
                item.symbol,
                quote.name or item.name or "-",
                f"{quote.price:.2f}",
                f"[{color}]{quote.change:+.2f}[/{color}]",
                f"[{color}]{quote.change_percent:+.2f}%[/{color}]",
                item.notes or "-",
            )
        else:
            table.add_row(
                item.symbol,
                item.name or "-",
                "-",
                "-",
                "-",
                item.notes or "-",
            )
    
    console.print(table)
    console.print(f"\n[dim]共 {len(items)} 只股票[/dim]")


@cli.command()
@click.argument('symbol')
@click.option('--name', '-n', help='股票名称')
@click.option('--notes', '-t', help='备注')
@click.pass_context
def add(ctx, symbol, name, notes):
    ""➕ 添加股票到自选股"""
    wl = ctx.obj['watchlist']
    wl.add_stock(symbol, name or "", notes or "")


@cli.command()
@click.argument('symbol')
@click.pass_context
def remove(ctx, symbol):
    ""➖ 从自选股中移除股票"""
    wl = ctx.obj['watchlist']
    wl.remove_stock(symbol)


@cli.command()
@click.argument('query')
@click.pass_context
def search(ctx, query):
    """🔍 搜索股票"""
    ds = ctx.obj['data_source']
    
    with console.status(f"[bold green]正在搜索 '{query}'..."):
        results = ds.search_symbols(query)
    
    if not results:
        console.print(f"[yellow]⚠️  未找到与 '{query}' 相关的股票[/yellow]")
        return
    
    table = Table(title=f"🔍 搜索结果: '{query}'", box=box.ROUNDED)
    table.add_column("代码", style="cyan")
    table.add_column("名称")
    table.add_column("交易所", style="dim")
    table.add_column("类型", style="dim")
    
    for result in results:
        table.add_row(
            result["symbol"],
            result["name"] or "-",
            result["exchange"] or "-",
            result["type"] or "-",
        )
    
    console.print(table)


@cli.command()
@click.pass_context
def monitor(ctx):
    """👁️ 实时监控自选股"""
    wl = ctx.obj['watchlist']
    ds = ctx.obj['data_source']
    
    symbols = wl.get_symbols()
    
    if not symbols:
        console.print("[yellow]📭 自选股列表为空，请先添加股票[/yellow]")
        return
    
    console.print("[bold green]👁️ 开始实时监控自选股 (按 Ctrl+C 停止)[/bold green]\n")
    
    try:
        while True:
            table = Table(title=f"📊 自选股实时监控 - {datetime.now().strftime('%H:%M:%S')}", 
                         box=box.ROUNDED)
            table.add_column("代码", style="cyan")
            table.add_column("名称")
            table.add_column("价格", justify="right")
            table.add_column("涨跌", justify="right")
            table.add_column("涨跌幅", justify="right")
            table.add_column("成交量", justify="right")
            
            for symbol in symbols:
                quote = ds.get_quote(symbol)
                if quote:
                    color = "green" if quote.is_positive else "red"
                    table.add_row(
                        symbol,
                        quote.name or "-",
                        f"[{color}]{quote.price:.2f}[/{color}]",
                        f"[{color}]{quote.change:+.2f}[/{color}]",
                        f"[{color}]{quote.change_percent:+.2f}%[/{color}]",
                        f"{quote.volume:,}",
                    )
                else:
                    table.add_row(symbol, "-", "-", "-", "-", "-")
            
            console.clear()
            console.print(table)
            
            import time
            time.sleep(5)  # 每5秒刷新
            
    except KeyboardInterrupt:
        console.print("\n[bold yellow]👋 已停止监控[/bold yellow]")


@cli.command()
def version():
    """📌 显示版本信息"""
    from . import __version__
    console.print(f"[bold blue]StockPulse[/bold blue] 版本: [bold]{__version__}[/bold]")
    console.print("[dim]本地化股票行情追踪与分析平台[/dim]")


def main():
    """主入口"""
    cli()


if __name__ == '__main__':
    main()
