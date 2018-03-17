# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup


class Test1Spider(scrapy.Spider):
    name = 'test1'
    start_urls = [r'https://www.baidu.com/s?wd=%E5%9E%83%E5%9C%BE%E7%84%9A%E7%83%A7']

    def __init__(self):
        self.times = 0

    def parse(self, response):
        self.times += 1
        fname = "F:\\Files\\JNJP_test1\\parse_1\\" + str(self.times) + ".html"
        try:
            with open(fname, 'wb') as f:
                f.write(response.body)
        except:
            pass
        soup = BeautifulSoup(response.body, "html.parser")
        all_href = soup.find_all('a')
        for url in all_href:
            try:
                yield scrapy.Request(url.get('href'), callback=self.parse_2)
            except:
                pass
    
    def parse_2(self, response):
        self.times += 1
        fname = "F:\\Files\\JNJP_test1\\parse_2\\" + str(self.times) + ".html"
        try:
            with open(fname, 'wb') as f:
                f.write(response.body)
        except:
            pass
        soup = BeautifulSoup(response.body, "html.parser")
        all_href = soup.find_all('a')
        for url in all_href:
            try:
                yield scrapy.Request(url.get('href'), callback=self.parse_3)
            except:
                pass
    
    def parse_3(self, response):
        self.times += 1
        fname = "F:\\Files\\JNJP_test1\\parse_3\\" + str(self.times) + ".html"
        try:
            with open(fname, 'wb') as f:
                f.write(response.body)
        except:
            pass
