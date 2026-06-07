from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="stockpulse",
    version="1.0.0",
    author="StockPulse Team",
    description="本地化股票行情追踪与分析平台",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gitstq/stockpulse",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Office/Business :: Financial",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.31.0",
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "matplotlib>=3.7.0",
        "rich>=13.0.0",
        "click>=8.1.0",
        "pydantic>=2.0.0",
        "python-dateutil>=2.8.0",
        "pyyaml>=6.0",
        "tabulate>=0.9.0",
        "plotly>=5.15.0",
        "flask>=2.3.0",
        "flask-socketio>=5.3.0",
    ],
    entry_points={
        "console_scripts": [
            "stockpulse=main:main",
        ],
    },
)
