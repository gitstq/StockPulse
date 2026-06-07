.PHONY: install test lint clean build run-web run-cli help

# 默认目标
.DEFAULT_GOAL := help

# 变量
PYTHON := python3
PIP := pip3
VENV := venv
VENV_BIN := $(VENV)/bin

help: ## 显示帮助信息
	@echo "StockPulse 构建工具"
	@echo ""
	@echo "可用命令:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## 安装依赖
	$(PIP) install -r requirements.txt

install-dev: ## 安装开发依赖
	$(PIP) install -r requirements.txt
	$(PIP) install pytest pytest-cov black flake8 mypy

test: ## 运行测试
	$(PYTHON) -m pytest tests/ -v --tb=short

test-cov: ## 运行测试并生成覆盖率报告
	$(PYTHON) -m pytest tests/ -v --cov=src --cov-report=html --cov-report=term

lint: ## 代码检查
	$(PYTHON) -m flake8 src/ --max-line-length=120
	$(PYTHON) -m black src/ --check

format: ## 格式化代码
	$(PYTHON) -m black src/ tests/

type-check: ## 类型检查
	$(PYTHON) -m mypy src/ --ignore-missing-imports

run-cli: ## 运行CLI模式
	$(PYTHON) main.py cli

run-web: ## 运行Web模式
	$(PYTHON) main.py web --port 5000

build: ## 构建包
	$(PYTHON) setup.py sdist bdist_wheel

clean: ## 清理构建产物
	rm -rf build/ dist/ *.egg-info/
	rm -rf .pytest_cache/ .coverage htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

docker-build: ## 构建Docker镜像
	docker build -t stockpulse:latest .

docker-run: ## 运行Docker容器
	docker run -p 5000:5000 stockpulse:latest
