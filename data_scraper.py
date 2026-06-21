"""
数据抓取模块 - 从蔬菜价格网站获取市场数据
"""
import requests
import numpy as np
import pandas as pd
from lxml import etree
from typing import List, Tuple, Optional
from config import Config


class DataScraper:
    """数据抓取类 - 负责从网页获取和解析价格数据"""
    
    def __init__(self):
        self.base_url = "http://price.cnveg.com"
        self.session = requests.Session()
        self.session.headers.update(Config.HEADERS)
    
    def get_market_data(self, url: str) -> List[Tuple[str, Optional[pd.DataFrame]]]:
        """
        获取所有市场的价格数据
        
        Args:
            url: 目标页面URL
            
        Returns:
            List of (市场名称, DataFrame) 元组
        """
        markets_data = []
        
        # 获取市场列表
        markets = self._get_market_list(url)
        
        for name, child_link in markets:
            try:
                print(f"正在处理: {name}")
                df = self._fetch_market_prices(name, child_link)
                markets_data.append((name, df))
            except Exception as e:
                print(f"  {name} 错误: {str(e)}")
                markets_data.append((name, None))
        
        return markets_data
    
    def _get_market_list(self, url: str) -> List[Tuple[str, str]]:
        """从主页面获取市场名称和链接列表"""
        response = self.session.get(url, timeout=Config.REQUEST_TIMEOUT)
        response.encoding = "utf-8"
        html = etree.HTML(response.text)
        
        table = html.xpath('//*[@class="borderTop p_3_4 l_h_21"]/table')
        
        hrefs = []
        names = []
        for trs in table:
            hrefs = trs.xpath(".//a/@href")
            names = trs.xpath(".//td/a/text()")
        
        markets = []
        for href, name in zip(hrefs, names):
            if href.startswith("/"):
                child_link = self.base_url + href
            else:
                child_link = self.base_url + "/" + href
            markets.append((name, child_link))
        
        return markets
    
    def _fetch_market_prices(self, name: str, url: str) -> Optional[pd.DataFrame]:
        """获取单个市场的价格数据并转为DataFrame"""
        response = self.session.get(url, headers=Config.HEADERS, timeout=Config.REQUEST_TIMEOUT)
        response.encoding = "utf-8"
        
        data = []
        html = etree.HTML(response.text)
        table = html.xpath('//*[@class="f_s_14"]')
        
        for trs in table:
            tr = trs.xpath(".//tr")
            for tds in tr:
                td = tds.xpath(".//td/text()")[0:5]
                if td:
                    data.extend(td)
        
        if not data:
            print(f"  {name} 无数据，跳过")
            return None
        
        # 数据整形：每4个元素为一行（日期、最低价、最高价、平均价）
        try:
            data_array = np.array(data)
            rows = data_array.reshape(-1, 4)
        except ValueError:
            # 数据条目不是4的倍数时，截断多余部分
            trim_len = (len(data) // 4) * 4
            data_array = np.array(data[:trim_len])
            rows = data_array.reshape(-1, 4)
        
        df = pd.DataFrame(rows, columns=["日期", "最低价", "最高价", "平均价"])
        
        # 数据清洗：移除人民币符号并转为浮点数
        for col in ["最低价", "最高价", "平均价"]:
            df[col] = df[col].str.replace("¥", "").astype(float)
        
        # 日期处理：转为datetime并排序
        df["日期"] = pd.to_datetime(df["日期"])
        df = df.sort_values("日期").reset_index(drop=True)
        
        return df