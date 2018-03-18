# coding:utf-8
# @__Author__ = "WDdeBWT"
# @__Date__ : 2017/10/20

import os
import re
import time

import jieba
# import jieba.analyse
# import jieba.posseg as pseg
from bs4 import BeautifulSoup
# import csv
import chardet

import win_unicode_console
win_unicode_console.enable()

class HtmlFilter:
    def __init__(self):
        self.read_path = 'F:\\Files\\JNJP_test1\\read_path'
        self.write_path = 'F:\\Files\\JNJP_test1\\write_path\\1.txt'
        self.keyword_list_path = 'F:\\Files\\JNJP_test1\\keyword_list.txt'
        self.keyword_list = []
        self.keyword_list_ge = (line.strip() for line in open(self.keyword_list_path, 'r', encoding='UTF-8').readlines())
        self.keyword_list = []
        for wd in self.keyword_list_ge:
            self.keyword_list.append(wd)
    
    def title_filter(self):
        i = 0
        title_list = []
        file_list = os.listdir(self.read_path)
        for file_name in file_list:
            try:
                matching_times = 0
                file_name = os.path.join(self.read_path, file_name)
                with open(file_name, 'rb') as r:
                    htmlpage_binary = r.read()
                    htmlpage = htmlpage_binary.decode(chardet.detect(htmlpage_binary)['encoding'], 'ignore')
                    soup = BeautifulSoup(htmlpage, "html.parser")
                    if not soup.title:
                        continue
                    page_title = soup.title.string
                    if not page_title:
                        continue
                    for seg in jieba.cut(page_title, cut_all=True):
                        if seg.strip() in self.keyword_list:
                            matching_times += 1
                    # try:
                    #     print(page_title)
                    # except:
                    #     print("small error")
                    #     continue
                    if matching_times >= 1:
                        i += 1
                        title_list.append(file_name + "   " + page_title)
                        print('--------------------')
                        print(file_name)
                        print(i)
                        try:
                            print(page_title)
                        except:
                            print("small error")
                            continue
            except Exception as e:
                print(file_name)
                print(e)
                continue
        with open(self.write_path, 'w') as w:
            w.writelines(title_list)

hf = HtmlFilter()
hf.title_filter()