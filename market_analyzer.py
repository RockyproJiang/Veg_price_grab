# market_analyzer.py
"""
蔬菜市场价格分析工具
Author: 蔬菜价格分析器
Version: 1.0.0
"""

import os
import re
import logging
from typing import List, Tuple, Optional
import pandas as pd
from config import Config
from data_scraper import DataScraper
from data_visualizer import DataVisualizer

class MarketAnalyzer:
    """市场分析主类"""

    def __init__(self):
        self.setup_logging()
        self.scraper = DataScraper()
        self.visualizer = DataVisualizer()

    def setup_logging(self):
        """设置日志记录"""
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler("market_analyzer.log", encoding="utf-8"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def run(self, url: str = None):
        """运行主程序"""
        if url is None:
            url = Config.TARGET_URL

        try:
            self.logger.info(f"开始分析市场数据: {url}")

            # 确保输出目录存在
            os.makedirs(Config.OUTPUT_DIR, exist_ok=True)

            # 获取并处理数据
            markets_data = self.scraper.get_market_data(url)

            success_count = 0
            for name, df in markets_data:
                if df is not None:
                    # 生成可视化图表
                    self.visualizer.plot_price_trend(name, df)
                    # 保存数据为CSV
                    self.save_data(name, df)
                    success_count += 1

            self.logger.info(f"数据处理完成 — 成功: {success_count}/{len(markets_data)}")

        except Exception as e:
            self.logger.error(f"程序运行出错: {str(e)}")
            raise

    def save_data(self, name: str, df: pd.DataFrame):
        """保存数据到CSV文件"""
        safe_name = self.clean_filename(name)
        csv_path = os.path.join(
            Config.OUTPUT_DIR,
            f"{safe_name}_价格数据.csv"
        )
        df.to_csv(csv_path, encoding=Config.CSV_ENCODING, index=False)
        self.logger.info(f"数据已保存: {csv_path}")

    @staticmethod
    def clean_filename(filename: str) -> str:
        """清理文件名中的特殊字符"""
        cleaned = re.sub(r"[<>:\"/\\|?*]", "", filename)
        return cleaned.strip().replace(" ", "_")

def main():
    """程序入口点"""
    analyzer = MarketAnalyzer()
    analyzer.run()

if __name__ == "__main__":
    main()
