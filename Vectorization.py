# coding:utf-8
import jieba
import jieba.analyse
import jieba.posseg as pseg
import chardet
from bs4 import BeautifulSoup
import codecs
import os
import re
import csv
import math

import win_unicode_console
win_unicode_console.enable()

class Vectorization:
    def __init__(self):
        self.key20_list = ['生活垃圾','居民','选址','政府','排放标准','污染','环评','填埋场','冲突'
            ,'意见','参与','信息公开','监管','二噁英','风险','抗议','补偿','协商','征求意见','信任']
        self.source_path = 'C:\\Users\\baiwt\\Desktop\\'
        self.read_path = self.source_path + 'demo60_txt_merge\\'
        self.write_path = self.source_path + 'demo60_result\\'
        self.stop_words_list_path = self.source_path + 'stopWord_1.txt'
        self.sim_list_path = self.source_path + 'demo60_Similarity.csv'
        self.pattern = re.compile(r"^[A-Za-z0-9\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+$")
        # 打开stopword_1.txt
        self.stop_words_list = []
        self.stop_words_list_ge = (
            line.strip()
            for line in open(self.stop_words_list_path, 'r',
                             encoding='UTF-8').readlines())
        for wd in self.stop_words_list_ge:
            self.stop_words_list.append(wd)
        # 打开Similarity.csv
        self.sim_list = []
        with open(self.sim_list_path) as f:
            reader = csv.reader(f)
            self.sim_list = list(reader)

    def Statistic_word_frequency(self):
        # 按文件统计词频
        i = 0
        big_li1 = []
        big_li2 = []
        file_list = os.listdir(self.read_path)
        for file_name in file_list:
            i += 1
            print('---------- ' + str(i) + ' ----------')
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
                # print(line)
                writer1.writerow(line)
        with open(self.write_path + 'demo200-2.csv', 'w', newline="") as w2:
            writer2 = csv.writer(w2)
            for line in big_li2:
                # print(line)
                writer2.writerow(line)
    
    def Statistic_word_frequency_1(self):
        # 统计全部词频
        i = 0
        big_word_list = []
        big_li1 = []
        big_li2 = []
        file_list = os.listdir(self.read_path)
        for file_name in file_list:
            i += 1
            print('---------- ' + str(i) + ' ----------')
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

    def Statistic_word_frequency_2(self):
        # 统计词频with相近词替换
        i = 0
        big_li2 = []
        big_li2.append(["File_Name"] + self.key20_list)
        file_list = os.listdir(self.read_path)
        for file_name in file_list:
            i += 1
            print('---------- ' + str(i) + ' ----------')
            # try:
            word_list = []
            file_path = os.path.join(self.read_path, file_name)
            with open(file_path, 'r', encoding = 'utf-8') as r:
                content = r.readlines()
            for line in content:
                for seg in jieba.cut(line.strip()):
                    if self.word_judge(seg.strip()):
                        if self.word_replace(seg.strip()):
                            seg = self.word_replace(seg.strip())
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
                li2.append(times)
            fmt_list = self.format_list(li1, li2)
            big_li2.append(fmt_list)
            # except Exception as e:
            #     print(e)
            #     continue
        with open(self.write_path + 'demo200-Vector.csv', 'w', newline="") as w2:
            writer2 = csv.writer(w2)
            for line in big_li2:
                writer2.writerow(line)
    
    def word_judge(self, seg):
        if len(seg) < 2:
            return False
        match = self.pattern.match(seg)
        if match:
            return False
        if seg in self.stop_words_list:
            return False
        return True
    
    def word_replace(self, seg):
        for one_sim in self.sim_list:
            if seg == one_sim[0]:
                return one_sim[1]
        return ''
    
    def format_list(self, words, numbers):
        # 求模
        square_sum = 0
        for num in numbers[1:]:
            square_sum += num*num
        # math.sqrt(square_sum)
        new_list = []
        new_list.append(words[0])
        for wd in self.key20_list:
            flag = 0
            for i in range(len(words)):
                if words[i] == wd:
                    flag = 1
                    new_list.append(str(numbers[i]/math.sqrt(square_sum)))
            if flag == 0:
                new_list.append(str(0))
        return new_list

    def get_format_list(self):
        # 根据现有文件输出单位向量
        with open(self.source_path + 'demo60-standard.csv') as f:
            reader = csv.reader(f)
            oricsv = list(reader)
        new_file = []
        for i in range(len(oricsv)):
            new_vector = []
            if i == 0:
                new_vector = oricsv[i]
            else:
                new_vector.append(oricsv[i][0])
                square_sum = 0
                for num in oricsv[i][1:]:
                    num = float(num)
                    square_sum += num*num
                for num in oricsv[i][1:]:
                    num = float(num)
                    new_vector.append(str(num/math.sqrt(square_sum)))
            new_file.append(new_vector)
        with open(self.write_path + 'demo60-standard-fmt.csv', 'w', newline="") as w2:
            writer2 = csv.writer(w2)
            for line in new_file:
                writer2.writerow(line)

vt = Vectorization()
# vt.Statistic_word_frequency()
# vt.Statistic_word_frequency_1()
# vt.Statistic_word_frequency_2()
vt.get_format_list()







    