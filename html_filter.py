# coding:utf-8
# @__Author__ = "WDdeBWT"
# @__Date__ : 2018/03/18

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
        self.read_path = 'C:\\Users\\---\\Desktop\\parse_119.23.239.27\\'        
        self.write_path = "F:\\Files\\JNJP_test1\\parse\\matching_title.txt"
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
                    matching_times = self.get_matching_times(soup.title)
                    if matching_times >= 1:
                        i += 1
                        page_title = soup.title.text
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
    
    def show_title(self):
        i = 0
        file_list = os.listdir(self.read_path)
        with open(self.write_path, 'w') as w:
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
                        matching_times = self.get_matching_times(soup.title)
                        if matching_times >= 1:
                            i += 1
                            page_title = soup.title.text
                            print('----------↓ ' + str(i) + ' ↓----------')
                            print(file_name + "  " + page_title.strip())
                            w.write('----------↓ ' + str(i) + ' ↓----------\n')
                            w.write(file_name + "  " + page_title.strip() + '\n')
                except Exception as e:
                    print(e)
                    continue
    
    def get_matching_times(self, one_title):
        matching_times = 0
        if not one_title.text:
            return 0
        a_text = one_title.text
        for seg in jieba.cut(a_text, cut_all=True):
            if seg.strip() in self.stopword_list:
                return 0
            if seg.strip() in self.keyword_list:
                matching_times += 1
        return matching_times

hf = HtmlFilter()
hf.show_title()