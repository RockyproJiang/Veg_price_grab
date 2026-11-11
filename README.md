# 蔬菜市场价格分析工具 · Veg_price_grab

蔬菜市场价格分析工具，从公开价格站点抓取各地区蔬菜批发市场价格，生成含最低价/最高价/均价的高清趋势图并导出 CSV。

## 功能特性

- **自动获取市场列表**：从目标页面解析各地区批发市场的名称与链接。
- **网页抓取与数据清洗**：抓取价格表格，规整为「日期 / 最低价 / 最高价 / 平均价」结构化数据，去除货币符号并按日期排序。
- **高清趋势图**：为每个市场生成含最低价、最高价、平均价三条曲线的 300 dpi PNG 图表。
- **CSV 导出**：将每个市场的清洗后价格数据保存为 CSV 文件，便于进一步分析。
- **模块化设计**：配置管理、网页抓取、可视化、主流程各自独立，便于维护与扩展。

## 技术栈 / 依赖

- Python 3
- `requests>=2.28.0` — HTTP 请求
- `lxml>=4.9.0` — HTML 解析（XPath）
- `numpy>=1.24.0`、`pandas>=1.5.0` — 数据处理与清洗
- `matplotlib>=3.6.0` — 图表绘制

完整依赖见 `requirements.txt`。

## 目录结构

```
Veg_price_grab/
├── config.py            # 配置管理：输出目录、图表样式、请求头、目标 URL 等
├── data_scraper.py      # 网页抓取：市场列表获取与价格数据解析
├── data_visualizer.py   # 可视化：价格趋势图绘制与保存
├── market_analyzer.py   # 主流程入口：串联抓取、绘图与 CSV 导出
├── requirements.txt     # 依赖列表
├── README.md            # 项目说明
├── LICENSE              # MIT 许可证
├── .gitignore           # Git 忽略规则
└── charts/              # 运行后生成的输出目录（趋势图 PNG 与 CSV）
```

## 快速开始

```bash
git clone https://github.com/RockyproJiang/Veg_price_grab.git
cd Veg_price_grab
pip install -r requirements.txt
python market_analyzer.py
```

运行后，`charts/` 目录下会生成每个市场的 `*_trend.png` 价格趋势图与 `*_价格数据.csv` 数据文件，同时输出 `market_analyzer.log` 日志。

> 说明：仓库已做清理——删除残留垃圾文件 `charts/1`、把误提交的 `__pycache__/*.pyc` 纳入 `.gitignore` 忽略、补上 `.gitignore` 与 MIT LICENSE。

## 配置与安全说明

- 项目无 API Key、无密钥；目标地址、请求头、超时、图表尺寸与颜色、输出目录等均在 `config.py` 的 `Config` 类中配置。
- 抓取的是公开网站数据，请遵守目标站点的服务条款与 robots 协议，合理控制请求频率，避免对站点造成压力。
- 解析依赖目标页面的 HTML 结构（XPath），页面结构变动会导致解析失效；本项目仅用于学习与演示，不保证数据持续可用。

## 许可证

本项目采用 MIT 许可证，详见 [LICENSE](LICENSE)。
