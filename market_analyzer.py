# market_analyzer.py
"""
蔬菜市场价格分析工具
Author: [你的名字]
Version: 1.0.0
"""

import os
import logging
from typing import List, Tuple, Optional
import pandas as pd
import matplotlib.pyplot as plt
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
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('market_analyzer.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def run(self, url: str):
        """运行主程序"""
        try:
            self.logger.info(f"开始分析市场数据: {url}")
            
            # 确保输出目录存在
            os.makedirs(Config.OUTPUT_DIR, exist_ok=True)
            
            # 获取并处理数据
            markets_data = self.scraper.get_market_data(url)
            
            for name, df in markets_data:
                if df is not None:
                    # 生成可视化图表
                    self.visualizer.plot_price_trend(name, df)
                    
                    # 保存数据
                    self.save_data(name, df)
                    
            self.logger.info("数据处理完成")
            
        except Exception as e:
            self.logger.error(f"程序运行出错: {str(e)}")
            raise
    
    def save_data(self, name: str, df: pd.DataFrame):
        """保存数据到CSV"""
        safe_name = self.clean_filename(name)
        csv_path = os.path.join(
            Config.OUTPUT_DIR, 
            f'{safe_name}_价格数据.csv'
        )
        df.to_csv(csv_path, encoding=Config.CSV_ENCODING, index=False)
        self.logger.info(f"数据已保存: {csv_path}")
    
    @staticmethod
    def clean_filename(filename: str) -> str:
        """清理文件名中的特殊字符"""
        # 保留中文字符、字母、数字和允许的特殊字符
        import re
        # 移除非法字符
        cleaned = re.sub(r'[<>:"/\\|?*]', '', filename)
        cleaned = cleaned.strip()
        return cleaned

def main():
    """程序入口点"""
    # 目标URL
    TARGET_URL = "http://price.cnveg.com/market/2/3/"
    
    # 创建分析器并运行
    analyzer = MarketAnalyzer()
    analyzer.run(TARGET_URL)

if __name__ == "__main__":
    main()