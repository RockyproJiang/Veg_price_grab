"""
配置文件 - 蔬菜市场价格分析工具
"""

class Config:
    """项目配置"""
    # 输出目录
    OUTPUT_DIR = "charts"
    
    # 图片格式
    IMAGE_FORMAT = "png"
    
    # 图表尺寸 (宽, 高)
    FIGURE_SIZE = (14, 8)
    
    # 线条宽度
    LINE_WIDTH = 2.5
    
    # 标记大小
    MARKER_SIZE = 5
    
    # 价格曲线颜色 [最低价, 最高价, 平均价]
    COLORS = ["red", "green", "orange"]
    
    # CSV编码
    CSV_ENCODING = "utf-8-sig"
    
    # 请求头
    HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }
    
    # 请求超时时间（秒）
    REQUEST_TIMEOUT = 10
    
    # 目标URL
    TARGET_URL = "http://price.cnveg.com/market/2/3/"