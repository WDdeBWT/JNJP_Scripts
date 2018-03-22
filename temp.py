import jieba
import jieba.analyse
import jieba.posseg as pseg
import chardet
from bs4 import BeautifulSoup
import codecs
import os
import re
import csv

import win_unicode_console
win_unicode_console.enable()

class Temp:
    def __init__(self):
        self.source_path = 'C:\\Users\\baiwt\\Desktop\\'
        self.read_path = self.source_path + 'sample_200\\'
        self.write_path = self.source_path + 'result_200\\'
        self.pattern = re.compile(r"^[A-Za-z0-9\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+$")
        self.stop_words_list = []

    def Statistic_word_frequency(self):
        i = 0
        big_li1 = []
        big_li2 = []
        file_list = os.listdir(self.read_path)
        for file_name in file_list:
            i += 1
            print(i)
            try:
                word_list = []
                file_path = os.path.join(self.read_path, file_name)
                with open(file_path, 'r', encoding = 'utf-8') as r:
                    content = r.readlines()
                for line in content:
                    for seg in jieba.cut(line.strip()):
                        if self.word_judge(seg.strip()):
                            word_list.append(seg.strip())
                li1 = []
                li1.append(file_name)
                li2 = []
                li2.append(file_name)
                word_set = set(word_list)
                for word_1 in word_set:
                    times = 0
                    for word_2 in word_list:
                        if word_1 == word_2:
                            times += 1
                    li1.append(word_1)
                    li2.append(str(times))
                big_li1.append(li1)
                big_li2.append(li2)
            except Exception as e:
                print(e)
                continue
        with open(self.write_path + 'demo200-1.csv', 'w', newline="") as w1:
            writer1 = csv.writer(w1)
            for line in big_li1:
                writer1.writerow(line)
        with open(self.write_path + 'demo200-2.csv', 'w', newline="") as w2:
            writer2 = csv.writer(w2)
            for line in big_li2:
                writer2.writerow(line)
    
    def Statistic_word_frequency_1(self):
        i = 0
        big_word_list = []
        big_li1 = []
        big_li2 = []
        file_list = os.listdir(self.read_path)
        for file_name in file_list:
            i += 1
            print(i)
            word_list = []
            file_path = os.path.join(self.read_path, file_name)
            with open(file_path, 'r', encoding = 'utf-8') as r:
                content = r.readlines()
            for line in content:
                for seg in jieba.cut(line.strip()):
                    if self.word_judge(seg.strip()):
                        word_list.append(seg.strip())
            word_set = set(word_list)
            for word in word_set:
                big_word_list.append(word)
        
        big_word_set = set(big_word_list)
        for word_1 in big_word_set:
            times = 0
            for word_2 in big_word_list:
                if word_1 == word_2:
                    times += 1
            big_li1.append(word_1)
            big_li2.append(str(times))

        with open(self.write_path + 'demo200AllPage-1.csv', 'w', newline="") as w1:
            writer1 = csv.writer(w1)
            writer1.writerow(big_li1)
        with open(self.write_path + 'demo200AllPage-2.csv', 'w', newline="") as w2:
            writer2 = csv.writer(w2)
            writer2.writerow(big_li2)
    
    def word_judge(self, seg):
        if len(seg) < 2:
            return False
        match = self.pattern.match(seg)
        if match:
            return False
        if seg in self.stop_words_list:
            return False
        return True

te = Temp()
te.Statistic_word_frequency_1()







    