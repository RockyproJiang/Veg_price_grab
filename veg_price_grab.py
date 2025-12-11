# 导入必要的库
import requests  # 用于发送HTTP请求
from lxml import etree  # 用于HTML/XML解析
import csv  # 用于CSV文件操作
import numpy as np  # 用于数值计算
import pandas as pd  # 用于数据处理和分析
import matplotlib.pyplot as plt  # 用于数据可视化
import matplotlib.ticker as ticker  # 用于坐标轴格式化
import os  # 用于操作系统相关功能
import matplotlib  # 基础绘图库

# 关闭交互式绘图模式，适合脚本中生成静态图像
plt.ioff()  

# 设置matplotlib中文字体支持，解决中文显示问题
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
# 解决负号显示为方框的问题
plt.rcParams['axes.unicode_minus'] = False

# 设置请求头，模拟浏览器访问
# headers = {
#    'User-Agent': ("你自己网页的User-Agent")
# }

def get_market(url):
    """
    主函数：从指定URL获取市场数据，分析并生成可视化图表和CSV文件
    
    参数:
        url: 目标市场数据页面的URL
    """
    # 发送GET请求获取主页面内容
    response = requests.get(url)#, headers=headers)
    response.encoding = "utf-8"  # 设置编码为UTF-8
    html = etree.HTML(response.text)  # 解析HTML内容
    
    # 使用XPath定位包含市场列表的表格
    table = html.xpath('//*[@class="borderTop p_3_4 l_h_21"]/table')
    
    # 初始化存储链接和名称的列表
    hrefs = []
    names = []
    
    # 遍历表格，提取每个市场的链接和名称
    for trs in table:
        hrefs = trs.xpath(".//a/@href")  # 提取所有链接
        names = trs.xpath('.//td/a/text()')  # 提取所有市场名称
    
    # 构建基础URL
    head = 'http://price.cnveg.com'
    
    # 遍历每个市场链接
    for i, (href, name) in enumerate(zip(hrefs, names)):
        # 构建完整的子页面URL
        if href.startswith('/'):
            child_link = head + href
        else:
            child_link = head + '/' + href
        
        try:
            # 请求子页面数据
            response = requests.get(child_link, headers=headers, timeout=10)
            response.encoding = "utf-8"
            
            # 初始化数据存储列表
            data = []
            html = etree.HTML(response.text)
            
            # 定位价格数据表格
            table = html.xpath('//*[@class="f_s_14"]')
            
            # 提取表格中的数据
            for trs in table:
                tr = trs.xpath('.//tr')  # 获取所有行
                for tds in tr:
                    # 提取每行的前5个单元格数据（日期、最低价、最高价、平均价等）
                    td = tds.xpath('.//td/text()')[0:5]
                    if td:  # 如果数据不为空
                        datapart = td
                        data = data + datapart  # 添加到总数据列表
            
            # 检查是否成功获取数据
            if not data:
                print(f"  {name} 无数据，跳过")
                continue    
            
            # 数据处理部分
            # 将列表转换为numpy数组
            data_array = np.array(data)
            # 重塑数组为二维数组，每行4列（日期、最低价、最高价、平均价）
            rows = data_array.reshape(-1, 4)
            
            # 创建DataFrame
            df = pd.DataFrame(rows, columns=['日期', '最低价', '最高价', '平均价'])
            
            # 数据清洗：移除价格中的'￥'符号并转换为浮点数
            df['最低价'] = df['最低价'].str.replace('￥', '').astype(float)
            df['最高价'] = df['最高价'].str.replace('￥', '').astype(float)
            df['平均价'] = df['平均价'].str.replace('￥', '').astype(float)
            
            # 日期处理：转换为datetime类型并设置为索引
            df['日期'] = pd.to_datetime(df['日期'])
            df.set_index('日期', inplace=True)
            df = df.sort_index()  # 按日期排序
            
            # 数据可视化部分
            # 创建图形和坐标轴
            fig, ax = plt.subplots(figsize=(14, 8))
            
            # 绘制三条价格线
            df.plot(ax=ax, linewidth=2.5, marker='o', markersize=5, color=['red', 'green', 'orange'])
            
            # 设置图表标题和标签
            ax.set_title(f'{name} 价格走势', fontsize=16, fontweight='bold')
            ax.set_xlabel('日期', fontsize=12)
            ax.set_ylabel('价格(元)', fontsize=12)
            
            # 添加图例
            ax.legend(['最低价', '最高价', '平均价'], loc='best', fontsize=11)
            
            # 添加网格线
            ax.grid(True, alpha=0.3)
            
            # 格式化Y轴为货币格式
            ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('¥{x:.2f}'))
            
            # 旋转X轴标签以便更好地显示
            plt.xticks(rotation=45)
            plt.tight_layout()  # 自动调整子图参数
            
            # 清理文件名，移除特殊字符
            safe_name = "".join([c for c in name if c.isalnum() or c in (' ', '-', '_')]).rstrip()
            
            # 保存图表为PNG文件
            plt.savefig(f'{safe_name}_trend.png', dpi=300, bbox_inches='tight')
            plt.close(fig)  # 关闭图形以释放内存
            print(f"  {name} 已保存为 {safe_name}.png")
            
            # 数据处理部分
            safe_csv_name = "".join([c for c in name if c.isalnum() or c in (' ', '-', '_')]).rstrip()
            df_reset = df.reset_index()  # 重置索引，将日期变为普通列
            
            # 保存数据为CSV文件
            df_reset.to_csv(f'{safe_csv_name}_价格数据.csv', index=False, encoding='utf-8-sig')
                
            print(f"  {name} 处理完成")
            
        except Exception as e:
            # 异常处理：打印错误信息并继续处理下一个市场
            print(f"   {name} 错误: {str(e)}")
            continue

# 程序入口点
if __name__ == '__main__':
    # 创建保存图表的目录（如果不存在）
    if not os.path.exists('charts'):
        os.makedirs('charts')
    
    # 切换到charts目录
    os.chdir('charts')
    
    # 调用主函数，传入目标URL
    get_market("http://price.cnveg.com/market/2/3/")
    
    print("全部完成")