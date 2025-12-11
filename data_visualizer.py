# data_visualizer.py
"""
数据可视化模块
"""
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
import os
from config import Config

class DataVisualizer:
    """数据可视化类"""
    
    def __init__(self):
        self.setup_matplotlib()
    
    def setup_matplotlib(self):
        """设置matplotlib参数"""
        plt.ioff()
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
        plt.rcParams['axes.unicode_minus'] = False
    
    def plot_price_trend(self, name: str, df: pd.DataFrame):
        """绘制价格趋势图"""
        try:
            fig, ax = plt.subplots(figsize=Config.FIGURE_SIZE)
            
            # 绘制价格线
            df.plot(
                x='日期',
                y=['最低价', '最高价', '平均价'],
                ax=ax,
                linewidth=Config.LINE_WIDTH,
                marker='o',
                markersize=Config.MARKER_SIZE,
                color=Config.COLORS
            )
            
            # 设置图表样式
            self.setup_chart_style(ax, name)
            
            # 保存图表
            self.save_chart(name, fig)
            
            plt.close(fig)
            print(f"  {name}: 图表已生成")
            
        except Exception as e:
            print(f"  生成 {name} 图表时出错: {str(e)}")
    
    def setup_chart_style(self, ax, title: str):
        """设置图表样式"""
        ax.set_title(f'{title} 价格走势', fontsize=16, fontweight='bold')
        ax.set_xlabel('日期', fontsize=12)
        ax.set_ylabel('价格(元)', fontsize=12)
        ax.legend(['最低价', '最高价', '平均价'], loc='best', fontsize=11)
        ax.grid(True, alpha=0.3)
        ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('¥{x:.2f}'))
        plt.xticks(rotation=45)
        plt.tight_layout()
    
    def save_chart(self, name: str, fig):
        """保存图表到文件"""
        safe_name = self.clean_filename(name)
        output_dir = Config.OUTPUT_DIR
        os.makedirs(output_dir, exist_ok=True)
        
        filepath = os.path.join(output_dir, f'{safe_name}_trend.{Config.IMAGE_FORMAT}')
        fig.savefig(filepath, dpi=300, bbox_inches='tight')
    
    @staticmethod
    def clean_filename(filename: str) -> str:
        """清理文件名"""
        import re
        # 允许中文字符、字母、数字和常用符号
        cleaned = re.sub(r'[<>:"/\\|?*]', '', filename)
        return cleaned.strip()