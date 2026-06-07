#!/usr/bin/env python3
"""
StockPulse - 本地化股票行情追踪与分析平台
StockPulse - Local Stock Market Tracking and Analysis Platform

主入口文件
Main entry point
"""

import sys
import argparse
from src.cli import main as cli_main
from src.web_app import run_web_app


def print_banner():
    """打印启动横幅"""
    banner = """
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║   📈 StockPulse - 本地化股票行情追踪与分析平台                ║
    ║   Local Stock Market Tracking & Analysis Platform             ║
    ║                                                               ║
    ║   版本 Version: 1.0.0                                         ║
    ║   协议 License: MIT                                           ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='StockPulse - 本地化股票行情追踪与分析平台',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例 Examples:
  python main.py cli quote AAPL          # 查看AAPL实时报价
  python main.py cli watchlist           # 查看自选股列表
  python main.py cli market              # 查看市场概览
  python main.py web --port 8080         # 启动Web服务
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # CLI 命令
    cli_parser = subparsers.add_parser('cli', help='命令行模式')
    cli_parser.add_argument('args', nargs='*', help='CLI参数')
    
    # Web 命令
    web_parser = subparsers.add_parser('web', help='Web服务模式')
    web_parser.add_argument('--host', default='0.0.0.0', help='主机地址 (默认: 0.0.0.0)')
    web_parser.add_argument('--port', type=int, default=5000, help='端口号 (默认: 5000)')
    web_parser.add_argument('--debug', action='store_true', help='调试模式')
    
    args = parser.parse_args()
    
    print_banner()
    
    if args.command == 'web':
        print(f"🌐 启动Web服务...")
        print(f"   地址: http://{args.host}:{args.port}")
        print(f"   按 Ctrl+C 停止服务\n")
        run_web_app(host=args.host, port=args.port, debug=args.debug)
    else:
        # 默认CLI模式
        if len(sys.argv) > 1 and sys.argv[1] == 'cli':
            sys.argv = sys.argv[1:]  # 移除 'cli' 参数
        cli_main()


if __name__ == '__main__':
    main()
