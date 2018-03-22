# coding:utf-8
# @__Author__ = "WDdeBWT"
# @__Date__ : 2018/03/18

import os
import re
import time

import jieba
import jieba.analyse
import jieba.posseg as pseg
import bs4
from bs4 import BeautifulSoup
import chardet


class HtmlFilter:
    def __init__(self):
        self.source_path = 'C:\\Users\\baiwt\\Desktop\\'
        self.read_path = self.source_path + 'result_39.108.112.9_bjx\\'
        self.write_path = self.source_path + 'result\\'
        self.keyword_list_path = self.source_path + 'keyword_list.txt'
        self.stopword_list_path = self.source_path + 'stopword_list.txt'
        self.contentfilter_list_path = self.source_path + 'contentfilter_list.txt'
        self.place_list_path = self.source_path + 'place_list.txt'
        self.keyword_list_ge = (
            line.strip()
            for line in open(self.keyword_list_path, 'r',
                             encoding='UTF-8').readlines())
        self.keyword_list = []
        for wd in self.keyword_list_ge:
            self.keyword_list.append(wd)
        self.stopword_list_ge = (
            line.strip()
            for line in open(self.stopword_list_path, 'r',
                             encoding='UTF-8').readlines())
        self.stopword_list = []
        for wd in self.stopword_list_ge:
            self.stopword_list.append(wd)
        self.contentfilter_list_ge = (
            line.strip()
            for line in open(
                self.contentfilter_list_path, 'r',
                encoding='UTF-8').readlines())
        self.contentfilter_list = []
        for line in self.contentfilter_list_ge:
            self.contentfilter_list.append(line.split(','))
            print((line.split(',')))
        self.place_list_ge = (
            line.strip()
            for line in open(self.place_list_path, 'r',
                             encoding='UTF-8').readlines())
        self.place_list = []
        for wd in self.place_list_ge:
            self.place_list.append(wd)

    # def title_filter(self):
    #     i = 0
    #     title_list = []
    #     file_list = os.listdir(self.read_path)
    #     for file_name in file_list:
    #         try:
    #             matching_times = 0
    #             file_name = os.path.join(self.read_path, file_name)
    #             with open(file_name, 'rb') as r:
    #                 htmlpage_binary = r.read()
    #                 htmlpage = htmlpage_binary.decode(
    #                     chardet.detect(htmlpage_binary)['encoding'], 'ignore')
    #                 soup = BeautifulSoup(htmlpage, "html.parser")
    #                 if not soup.title:
    #                     continue
    #                 matching_times = self.get_matching_times(soup.title)
    #                 if matching_times >= 1:
    #                     i += 1
    #                     page_title = soup.title.text
    #                     title_list.append(file_name + "   " + page_title)
    #                     print('--------------------')
    #                     print(file_name)
    #                     print(i)
    #                     try:
    #                         print(page_title)
    #                     except:
    #                         print("small error")
    #                         continue
    #         except Exception as e:
    #             print(file_name)
    #             print(e)
    #             continue
    #     with open(self.write_path, 'w') as w:
    #         w.writelines(title_list)

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
                        htmlpage = htmlpage_binary.decode(
                            chardet.detect(htmlpage_binary)['encoding'],
                            'ignore')
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

    def page_filter(self):
        i = 0
        rstr = r"[\/\\\:\*\?\"\<\>\|]"
        file_list = os.listdir(self.read_path)
        for file_name in file_list:
            try:
                file_path = os.path.join(self.read_path, file_name)
                with open(file_path, 'rb') as r:
                    htmlpage_binary = r.read()
                htmlpage = htmlpage_binary.decode(
                    chardet.detect(htmlpage_binary)['encoding'], 'ignore')
                soup = BeautifulSoup(htmlpage, "html.parser")
                if not soup.title:
                    continue
                if not self.title_filter(soup.title):
                    continue
                if not self.content_filter(soup):
                    continue
                place_name = self.judge_place(soup.title.text.strip())
                if not place_name:
                    place_name = 'PlaceNotFind'
                new_file_path = self.write_path + place_name + '-' + re.sub(
                    rstr, '', soup.title.text.strip()) + '-' + file_name
                with open(new_file_path, 'wb') as w:
                    w.write(htmlpage_binary)
                i += 1
                print('----------↓ ' + str(i) + ' ↓----------\n')
                print(new_file_path)
            except Exception as e:
                print(e)
                continue
    
    def get_content(self):
        i = 0
        file_list = os.listdir(self.read_path)
        for file_name in file_list:
            try:
                write_list = []
                file_path = os.path.join(self.read_path, file_name)
                with open(file_path, 'rb') as r:
                    htmlpage_binary = r.read()
                htmlpage = htmlpage_binary.decode(
                    chardet.detect(htmlpage_binary)['encoding'], 'ignore')
                soup = BeautifulSoup(htmlpage, "html.parser")
                for script in soup(["script", "style"]):
                    script.extract()  # rip it out
                for string in soup.stripped_strings:
                    if (self.string_judge(string.strip())):
                        write_list.append(string.strip() + '\n')
                new_file_path = os.path.join(self.write_path, file_name[:-5] + '.txt')
                with open(new_file_path, 'w', encoding = 'utf-8') as w:
                    w.writelines(write_list)
                i += 1
                print('----------↓ ' + str(i) + ' ↓----------\n')
                print(new_file_path)
            except Exception as e:
                print(e)
                continue

    def title_filter(self, title):
        matching_times = self.get_matching_times(title)
        if matching_times >= 1:
            return True
        else:
            return False

    def content_filter(self, page_soup):
        string_list = []
        all_words = ''
        for script in page_soup(["script", "style"]):
            script.extract()  # rip it out
        # 获取所有div标签下的文字内容
        for string in page_soup.stripped_strings:
            if string:
                all_words += string.strip()
        if len(all_words) < 200:
            return False
        for string in page_soup.stripped_strings:
            string = string.strip("\n").strip()
            if self.string_judge(string):
                string_list.append(string + "\n")
        if not string_list:
            return False
        return True

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

    def string_judge(self, string):
        # self.contentfilter_list
        seg_list = []
        if len(string) < 20:
            return False
        if len(string) > 100:
            return True
        # if string contains contentfilter_list return false
        for seg in jieba.cut(string, cut_all=True):
            seg_list.append(seg.strip())
        seg_list = list(set(seg_list))
        for cf_sublist in self.contentfilter_list:
            new_list = list(set(seg_list + cf_sublist))
            if len(seg_list) == len(new_list):
                return False

    def judge_place(self, string):
        for seg in jieba.cut(string, cut_all=True):
            if seg in self.place_list:
                return seg
        return None


hf = HtmlFilter()
hf.get_content()
