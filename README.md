# 📈 StockPulse - 本地化股票行情追踪与分析平台

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.0.0-orange)](https://github.com/gitstq/stockpulse)

**🌐 [简体中文](#简体中文) | [繁體中文](#繁體中文) | [English](#english)**

</div>

---

## 简体中文

### 🎉 项目介绍

**StockPulse** 是一款开源的本地化股票行情追踪与分析平台，灵感来源于对昂贵商业行情软件的不满和对数据自主掌控的追求。

在当前的金融市场中，优质的行情数据往往被锁定在昂贵的付费墙之后。StockPulse 打破了这一壁垒，让每位投资者都能免费、实时地追踪全球股市动态，并通过智能分析辅助投资决策。

**核心价值：**
- 🆓 **完全免费** - 开源免费，无任何隐藏费用
- 🏠 **本地部署** - 数据本地处理，保护隐私安全
- 🌍 **全球覆盖** - 支持全球主要股票市场
- 🤖 **智能分析** - AI驱动的技术面与基本面分析

**自研差异化亮点：**
- ✅ 纯本地化运行，无需注册第三方API（可选配置）
- ✅ 多维度智能评分系统（技术面/基本面/情绪面）
- ✅ 实时Web监控面板，支持自选股追踪
- ✅ 模块化数据源架构，易于扩展新数据源
- ✅ 优雅的终端UI与Web界面双模式支持

### ✨ 核心特性

| 特性 | 描述 | 状态 |
|------|------|------|
| 📊 **实时行情** | 获取全球主要股票实时报价 | ✅ 可用 |
| 📈 **历史数据** | 支持多周期历史K线数据查询 | ✅ 可用 |
| 🔍 **股票搜索** | 智能搜索全球股票代码 | ✅ 可用 |
| ⭐ **自选股** | 自定义关注列表，实时追踪 | ✅ 可用 |
| 💡 **智能分析** | 技术面/基本面/情绪面综合评分 | ✅ 可用 |
| 🌍 **市场概览** | 全球主要指数实时监控 | ✅ 可用 |
| 🖥️ **Web面板** | 美观的Web可视化界面 | ✅ 可用 |
| 🖥️ **终端界面** | 优雅的命令行交互体验 | ✅ 可用 |
| 🔔 **价格预警** | 自定义价格变动提醒 | 🚧 开发中 |
| 📱 **移动端适配** | 响应式Web设计 | ✅ 可用 |

### 🚀 快速开始

#### 环境要求

- **Python** >= 3.8
- **pip** >= 21.0
- **操作系统**: Windows / macOS / Linux

#### 安装步骤

```bash
# 1. 克隆仓库
git clone https://github.com/gitstq/stockpulse.git
cd stockpulse

# 2. 安装依赖
pip install -r requirements.txt

# 3. 验证安装
python main.py --version
```

#### 快速启动

**命令行模式：**
```bash
# 查看股票实时报价
python main.py quote AAPL

# 查看市场概览
python main.py market

# 查看自选股
python main.py watchlist

# 启动实时监控
python main.py monitor
```

**Web模式：**
```bash
# 启动Web服务
python main.py web --port 5000

# 然后在浏览器中访问 http://localhost:5000
```

### 📖 详细使用指南

#### CLI 命令参考

```bash
# 获取股票报价
stockpulse quote <股票代码>

# 查看历史数据
stockpulse history <股票代码> --period 1mo

# 搜索股票
stockpulse search <关键词>

# 添加自选股
stockpulse add <股票代码> --name "公司名称" --notes "备注"

# 移除自选股
stockpulse remove <股票代码>

# 获取智能分析
stockpulse insight <股票代码>

# 实时监控
stockpulse monitor
```

#### Web 界面功能

1. **市场概览** - 首页展示全球主要指数实时行情
2. **股票搜索** - 顶部搜索框支持股票代码/名称搜索
3. **自选股管理** - 添加/删除关注股票，实时价格追踪
4. **详情分析** - 点击股票查看详细报价、历史图表、智能分析
5. **响应式设计** - 完美适配桌面端和移动端

#### 配置说明

配置文件位于 `~/.stockpulse/config.yaml`：

```yaml
debug: false
data_dir: "./data"
log_level: "INFO"

default_watchlist:
  - "AAPL"
  - "GOOGL"
  - "MSFT"

data_sources:
  - name: "yahoo"
    enabled: true
    rate_limit: 60

alert:
  enabled: true
  price_change_threshold: 5.0
  check_interval: 60

display:
  theme: "dark"
  refresh_interval: 5
```

### 💡 设计思路与迭代规划

#### 技术选型原因

| 技术 | 用途 | 选型理由 |
|------|------|----------|
| **Python** | 核心语言 | 生态丰富，金融库完善 |
| **Flask** | Web框架 | 轻量灵活，易于扩展 |
| **Rich** | 终端UI | 美观的终端界面渲染 |
| **Chart.js** | 图表绘制 | 轻量、响应式、易用 |
| **Tailwind CSS** | Web样式 | 原子化CSS，快速开发 |

#### 后续功能迭代计划

- [ ] **v1.1.0** - 价格预警系统（邮件/推送通知）
- [ ] **v1.2.0** - 多数据源聚合（Yahoo + Alpha Vantage + Tushare）
- [ ] **v1.3.0** - 技术指标扩展（MACD、KDJ、布林带等）
- [ ] **v1.4.0** - 投资组合管理功能
- [ ] **v1.5.0** - 数据导出（CSV/Excel/PDF）
- [ ] **v2.0.0** - 机器学习预测模型

#### 社区贡献方向

- 🌍 更多数据源适配（东方财富、同花顺等）
- 🎨 主题定制与UI优化
- 📊 更多技术指标实现
- 🌐 多语言界面支持

### 📦 打包与部署指南

#### Docker 部署

```bash
# 构建镜像
docker build -t stockpulse:latest .

# 运行容器
docker run -p 5000:5000 stockpulse:latest
```

#### 本地打包

```bash
# 安装打包工具
pip install pyinstaller

# 打包为可执行文件
pyinstaller --onefile --name stockpulse main.py
```

#### 开发环境

```bash
# 安装开发依赖
pip install -r requirements.txt
pip install pytest black flake8

# 运行测试
pytest tests/

# 代码格式化
black src/ tests/
```

### 🤝 贡献指南

1. **Fork** 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 **Pull Request**

### 📄 开源协议

本项目采用 [MIT](LICENSE) 开源协议。

---

## 繁體中文

### 🎉 專案介紹

**StockPulse** 是一款開源的本機化股票行情追蹤與分析平台，靈感來源於對昂貴商業行情軟體的不滿和對資料自主掌控的追求。

在當前的金融市場中，優質的行情資料往往被鎖定在昂貴的付費牆之後。StockPulse 打破了這一壁壘，讓每位投資者都能免費、即時地追蹤全球股市動態，並透過智慧分析輔助投資決策。

**核心價值：**
- 🆓 **完全免費** - 開源免費，無任何隱藏費用
- 🏠 **本地部署** - 資料本機處理，保護隱私安全
- 🌍 **全球覆蓋** - 支援全球主要股票市場
- 🤖 **智慧分析** - AI驅動的技術面與基本面分析

**自研差異化亮點：**
- ✅ 純本機化執行，無需註冊第三方API（可選配置）
- ✅ 多維度智慧評分系統（技術面/基本面/情緒面）
- ✅ 即時Web監控面板，支援自選股追蹤
- ✅ 模組化資料源架構，易於擴充套件新資料源
- ✅ 優雅的終端UI與Web介面雙模式支援

### ✨ 核心特性

| 特性 | 描述 | 狀態 |
|------|------|------|
| 📊 **即時行情** | 獲取全球主要股票即時報價 | ✅ 可用 |
| 📈 **歷史資料** | 支援多週期歷史K線資料查詢 | ✅ 可用 |
| 🔍 **股票搜尋** | 智慧搜尋全球股票代碼 | ✅ 可用 |
| ⭐ **自選股** | 自定義關注列表，即時追蹤 | ✅ 可用 |
| 💡 **智慧分析** | 技術面/基本面/情緒面綜合評分 | ✅ 可用 |
| 🌍 **市場概覽** | 全球主要指數即時監控 | ✅ 可用 |
| 🖥️ **Web面板** | 美觀的Web視覺化介面 | ✅ 可用 |
| 🖥️ **終端介面** | 優雅的命令列互動體驗 | ✅ 可用 |
| 🔔 **價格預警** | 自定義價格變動提醒 | 🚧 開發中 |
| 📱 **行動端適配** | 響應式Web設計 | ✅ 可用 |

### 🚀 快速開始

#### 環境要求

- **Python** >= 3.8
- **pip** >= 21.0
- **作業系統**: Windows / macOS / Linux

#### 安裝步驟

```bash
# 1. 克隆倉庫
git clone https://github.com/gitstq/stockpulse.git
cd stockpulse

# 2. 安裝依賴
pip install -r requirements.txt

# 3. 驗證安裝
python main.py --version
```

#### 快速啟動

**命令列模式：**
```bash
# 檢視股票即時報價
python main.py quote AAPL

# 檢視市場概覽
python main.py market

# 檢視自選股
python main.py watchlist

# 啟動即時監控
python main.py monitor
```

**Web模式：**
```bash
# 啟動Web服務
python main.py web --port 5000

# 然後在瀏覽器中訪問 http://localhost:5000
```

### 📖 詳細使用指南

#### CLI 命令參考

```bash
# 獲取股票報價
stockpulse quote <股票代碼>

# 檢視歷史資料
stockpulse history <股票代碼> --period 1mo

# 搜尋股票
stockpulse search <關鍵詞>

# 新增自選股
stockpulse add <股票代碼> --name "公司名稱" --notes "備註"

# 移除自選股
stockpulse remove <股票代碼>

# 獲取智慧分析
stockpulse insight <股票代碼>

# 即時監控
stockpulse monitor
```

#### Web 介面功能

1. **市場概覽** - 首頁展示全球主要指數即時行情
2. **股票搜尋** - 頂部搜尋框支援股票代碼/名稱搜尋
3. **自選股管理** - 新增/刪除關注股票，即時價格追蹤
4. **詳情分析** - 點選股票檢視詳細報價、歷史圖表、智慧分析
5. **響應式設計** - 完美適配桌面端和行動端

### 💡 設計思路與迭代規劃

#### 技術選型原因

| 技術 | 用途 | 選型理由 |
|------|------|----------|
| **Python** | 核心語言 | 生態豐富，金融庫完善 |
| **Flask** | Web框架 | 輕量靈活，易於擴充套件 |
| **Rich** | 終端UI | 美觀的終端介面渲染 |
| **Chart.js** | 圖表繪製 | 輕量、響應式、易用 |
| **Tailwind CSS** | Web樣式 | 原子化CSS，快速開發 |

#### 後續功能迭代計劃

- [ ] **v1.1.0** - 價格預警系統（郵件/推播通知）
- [ ] **v1.2.0** - 多資料源聚合（Yahoo + Alpha Vantage + Tushare）
- [ ] **v1.3.0** - 技術指標擴充套件（MACD、KDJ、布林帶等）
- [ ] **v1.4.0** - 投資組合管理功能
- [ ] **v1.5.0** - 資料匯出（CSV/Excel/PDF）
- [ ] **v2.0.0** - 機器學習預測模型

### 📦 打包與部署指南

#### Docker 部署

```bash
# 構建映象
docker build -t stockpulse:latest .

# 執行容器
docker run -p 5000:5000 stockpulse:latest
```

#### 開發環境

```bash
# 安裝開發依賴
pip install -r requirements.txt
pip install pytest black flake8

# 執行測試
pytest tests/

# 程式碼格式化
black src/ tests/
```

### 🤝 貢獻指南

1. **Fork** 本倉庫
2. 建立特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 建立 **Pull Request**

### 📄 開源協議

本專案採用 [MIT](LICENSE) 開源協議。

---

## English

### 🎉 Project Introduction

**StockPulse** is an open-source local stock market tracking and analysis platform, inspired by the frustration with expensive commercial market data software and the desire for data sovereignty.

In today's financial markets, quality market data is often locked behind expensive paywalls. StockPulse breaks down these barriers, allowing every investor to track global stock market dynamics in real-time for free, with intelligent analysis to aid investment decisions.

**Core Values:**
- 🆓 **Completely Free** - Open source, no hidden fees
- 🏠 **Local Deployment** - Data processed locally, privacy protected
- 🌍 **Global Coverage** - Support for major global stock markets
- 🤖 **Intelligent Analysis** - AI-driven technical and fundamental analysis

**Differentiation Highlights:**
- ✅ Pure local execution, no third-party API registration required (optional config)
- ✅ Multi-dimensional intelligent scoring system (Technical/Fundamental/Sentiment)
- ✅ Real-time Web monitoring dashboard with watchlist tracking
- ✅ Modular data source architecture, easy to extend new sources
- ✅ Elegant terminal UI and Web interface dual-mode support

### ✨ Core Features

| Feature | Description | Status |
|---------|-------------|--------|
| 📊 **Real-time Quotes** | Get real-time quotes for major global stocks | ✅ Available |
| 📈 **Historical Data** | Multi-period historical candlestick data | ✅ Available |
| 🔍 **Stock Search** | Intelligent global stock symbol search | ✅ Available |
| ⭐ **Watchlist** | Custom watchlist with real-time tracking | ✅ Available |
| 💡 **Smart Analysis** | Technical/Fundamental/Sentiment composite scoring | ✅ Available |
| 🌍 **Market Overview** | Real-time monitoring of major global indices | ✅ Available |
| 🖥️ **Web Dashboard** | Beautiful Web visualization interface | ✅ Available |
| 🖥️ **Terminal UI** | Elegant command-line interactive experience | ✅ Available |
| 🔔 **Price Alerts** | Custom price change notifications | 🚧 In Development |
| 📱 **Mobile Responsive** | Responsive Web design | ✅ Available |

### 🚀 Quick Start

#### Requirements

- **Python** >= 3.8
- **pip** >= 21.0
- **OS**: Windows / macOS / Linux

#### Installation

```bash
# 1. Clone the repository
git clone https://github.com/gitstq/stockpulse.git
cd stockpulse

# 2. Install dependencies
pip install -r requirements.txt

# 3. Verify installation
python main.py --version
```

#### Quick Launch

**CLI Mode:**
```bash
# View real-time stock quote
python main.py quote AAPL

# View market overview
python main.py market

# View watchlist
python main.py watchlist

# Start real-time monitoring
python main.py monitor
```

**Web Mode:**
```bash
# Start Web service
python main.py web --port 5000

# Then open http://localhost:5000 in your browser
```

### 📖 Detailed Usage Guide

#### CLI Command Reference

```bash
# Get stock quote
stockpulse quote <SYMBOL>

# View historical data
stockpulse history <SYMBOL> --period 1mo

# Search stocks
stockpulse search <KEYWORD>

# Add to watchlist
stockpulse add <SYMBOL> --name "Company Name" --notes "Notes"

# Remove from watchlist
stockpulse remove <SYMBOL>

# Get intelligent analysis
stockpulse insight <SYMBOL>

# Real-time monitoring
stockpulse monitor
```

#### Web Interface Features

1. **Market Overview** - Display real-time quotes for major global indices
2. **Stock Search** - Top search bar supports symbol/name search
3. **Watchlist Management** - Add/remove tracked stocks with real-time prices
4. **Detail Analysis** - Click stock to view detailed quotes, charts, and analysis
5. **Responsive Design** - Perfectly adapted for desktop and mobile

### 💡 Design Philosophy & Roadmap

#### Technology Stack

| Technology | Purpose | Rationale |
|------------|---------|-----------|
| **Python** | Core Language | Rich ecosystem, excellent financial libraries |
| **Flask** | Web Framework | Lightweight and flexible, easy to extend |
| **Rich** | Terminal UI | Beautiful terminal interface rendering |
| **Chart.js** | Charting | Lightweight, responsive, easy to use |
| **Tailwind CSS** | Web Styling | Atomic CSS, rapid development |

#### Future Roadmap

- [ ] **v1.1.0** - Price alert system (Email/Push notifications)
- [ ] **v1.2.0** - Multi-source data aggregation
- [ ] **v1.3.0** - Extended technical indicators (MACD, KDJ, Bollinger Bands)
- [ ] **v1.4.0** - Portfolio management features
- [ ] **v1.5.0** - Data export (CSV/Excel/PDF)
- [ ] **v2.0.0** - Machine learning prediction models

### 📦 Packaging & Deployment

#### Docker Deployment

```bash
# Build image
docker build -t stockpulse:latest .

# Run container
docker run -p 5000:5000 stockpulse:latest
```

#### Development Environment

```bash
# Install dev dependencies
pip install -r requirements.txt
pip install pytest black flake8

# Run tests
pytest tests/

# Format code
black src/ tests/
```

### 🤝 Contributing

1. **Fork** this repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Create a **Pull Request**

### 📄 License

This project is licensed under the [MIT](LICENSE) License.

---

<div align="center">

**Made with ❤️ by StockPulse Team**

⭐ Star us on GitHub — it motivates us a lot!

</div>
