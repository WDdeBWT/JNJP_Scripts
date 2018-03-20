# -*- coding: utf-8 -*-
# @__Author__ = "WDdeBWT"
# @__Date__ : 2018/03/19

import chardet

import jieba
import scrapy
from tld import get_tld
from bs4 import BeautifulSoup


class Test1Spider(scrapy.Spider):
    name = 'test1'
    start_urls = [r'https://www.baidu.com/s?wd=%E5%9E%83%E5%9C%BE%E7%84%9A%E7%83%A7',
    r'https://www.baidu.com/s?wd=%E9%82%BB%E9%81%BF',
    r'http://search.sina.com.cn/?c=blog&q=%C0%AC%BB%F8%B7%D9%C9%D5&by=title',
    # r'http://www.ftchinese.com/search/?keys=%E9%82%BB%E9%81%BF&ftsearchType=type_news',
    r'http://search.ifeng.com/sofeng/search.action?q=%E9%82%BB%E9%81%BF&c=1&p=1',
    r'http://search.infzm.com/search.php?q=%E9%82%BB%E9%81%BF',
    r'http://www.cn-hw.net/plus/search.php?kwtype=0&keyword=%C1%DA%B1%DC',
    r'https://a.jiemian.com/index.php?m=search&a=index&msg=%E9%82%BB%E9%81%BF']

    def __init__(self):
        self.times = 0
        self.stop_domian = ['1688.com', 'jd.com', 'taobao.com', 'tmall.com', 'hc360.com', 'ehsy.com', 'china.herostart.com',
         'herostart.com', 'hao123.com', 'chinabgao.com', 'chinabaogao.com', 'baogao.com']
        self.write_path = "F:\\Files\\JNJP_test1\\parse\\"
        self.keyword_list_path = 'F:\\Files\\JNJP_test1\\keyword_list.txt'
        self.stopword_list_path = 'F:\\Files\\JNJP_test1\\stopword_list.txt'
        self.keyword_list_ge = (line.strip() for line in open(self.keyword_list_path, 'r', encoding='UTF-8').readlines())
        self.keyword_list = []
        for wd in self.keyword_list_ge:
            self.keyword_list.append(wd)
        self.stopword_list_ge = (line.strip() for line in open(self.stopword_list_path, 'r', encoding='UTF-8').readlines())
        self.stopword_list = []
        for wd in self.stopword_list_ge:
            self.stopword_list.append(wd)

    def parse(self, response):
        self.times += 1
        print('----------' + str(self.times) + '----------')
        fname = self.write_path + str(self.times) + ".html"
        html_source_b = response.body
        try:
            with open(fname, 'wb') as f:
                f.write(html_source_b)
        except:
            pass
        try:
            html_source = html_source_b.decode(chardet.detect(html_source_b)['encoding'], 'ignore')
        except:
            html_source = html_source_b.decode('utf-8', 'ignore')
        soup = BeautifulSoup(html_source, "html.parser")
        all_a = soup.find_all('a')
        for one_a in all_a:
            try:
                if self.get_matching_times(one_a) >= 1:
                    try:
                        if get_tld(one_a.get('href')) not in self.stop_domian:
                            yield scrapy.Request(one_a.get('href'), callback=self.parse)
                    except:
                        continue
                else:
                    try:
                        if get_tld(one_a.get('href')) not in self.stop_domian:
                            yield scrapy.Request(one_a.get('href'), callback=self.parse_second)
                    except:
                        continue
            except:
                continue
    
    def parse_second(self, response):
        html_source_b = response.body
        try:
            html_source = html_source_b.decode(chardet.detect(html_source_b)['encoding'], 'ignore')
        except:
            html_source = html_source_b.decode('utf-8', 'ignore')
        soup = BeautifulSoup(html_source, "html.parser")
        all_a = soup.find_all('a')
        matching_a = 0
        for one_a in all_a:
            if self.get_matching_times(one_a) >= 1:
                matching_a += 1
        if matching_a >= 3:
            for one_a in all_a:
                try:
                    if self.get_matching_times(one_a) >= 1:
                        try:
                            if get_tld(one_a.get('href')) not in self.stop_domian:
                                yield scrapy.Request(one_a.get('href'), callback=self.parse)
                        except:
                            continue
                    else:
                        try:
                            if get_tld(one_a.get('href')) not in self.stop_domian:
                                yield scrapy.Request(one_a.get('href'), callback=self.parse_second)
                        except:
                            continue
                except:
                    continue

    
    def get_matching_times(self, one_a):
        matching_times = 0
        if not one_a.text:
            return 0
        a_text = one_a.text
        for seg in jieba.cut(a_text, cut_all=True):
            if seg.strip() in self.stopword_list:
                return 0
            if seg.strip() in self.keyword_list:
                matching_times += 1
        return matching_times
