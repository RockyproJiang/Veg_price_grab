# 蔬菜市场价格分析工具 🥬

一个用于抓取、分析和可视化蔬菜市场价格数据的 Python 工具。从
[price.cnveg.com](http://price.cnveg.com) 获取各地区蔬菜批发市场的历史价格数据，自动生成价格趋势
图表和 CSV 数据文件。

## 功能

- **数据抓取** — 自动从目标网站获取各市场的蔬菜价格数据
- **数据清洗** — 处理日期格式、价格符号，生成结构化的 DataFrame
- **趋势可视化** — 生成包含最低价、最高价、平均价曲线的高清 PNG 图表
- **数据导出** — 将每个市场的价格数据保存为 CSV 文件，便于进一步分析

## 项目结构

```
Veg_price_grab/
├── config.py           # 配置文件（路径、样式、请求头等）
├── data_scraper.py     # 数据抓取模块
├── data_visualizer.py  # 数据可视化模块
├── market_analyzer.py  # 主程序入口
├── requirements.txt    # 依赖列表
├── .gitignore          # Git 忽略规则
├── README.md           # 项目说明
└── charts/             # 输出目录（图表 + CSV）
```

## 安装

```bash
git clone <your-repo-url>
cd Veg_price_grab
pip install -r requirements.txt
```

## 使用

```bash
python market_analyzer.py
```

运行后，`charts/` 目录下将生成每个市场的价格趋势图和 CSV 数据文件。

## 依赖

- Python 3.8+
- requests — HTTP 请求
- lxml — HTML 解析
- numpy / pandas — 数据处理
- matplotlib — 图表绘制

## 许可

MIT License
