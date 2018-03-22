# coding:utf-8
# @__Author__ = "WDdeBWT"
# @__Date__ : 2018/03/22

import os
import re
import csv
import time

from aip import AipNlp

class SimilarityCalculation:
    def __init__(self):
        self.source_path = 'C:\\Users\\baiwt\\Desktop\\'
        self.write_path = self.source_path + 'Similarity.csv'
        self.key20_list = ['无害化', '烟气', '污染', '减量化', '滤液', '废弃物', '飞灰', '清洁', '基础设施', 
            '有害物质', '环境', '效益', '噪声', '处理工艺', '监测', '风险', '臭气', '补贴', '管理', '法律法规']
        self.top500_list_path = self.source_path + 'top500.txt'
        self.top500_list = []
        self.top500_list_ge = (line.strip() for line in open(self.top500_list_path, 'r',encoding='UTF-8').readlines())
        for wd in self.top500_list_ge:
            self.top500_list.append(wd)
        
        APP_ID = '10975759'
        API_KEY = 'CNLZcnqL3E6NLeFNGzUE06fY'
        SECRET_KEY = 'b8Z7nQPmASHHhPLjRG6dXKQG7W97DxNk'
        self.client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

    
    def main(self):
        i = 0
        write_list = []
        for wdtp in self.top500_list:
            big_li = self.get_similarity(wdtp)
            time.sleep(0.02)
            for small_li in big_li:
                write_list.append(small_li) #[top500, key20, value]
            i += 1
            print('---------- ' + str(i) + ' ----------')
            if i == 20:
                break
        with open(self.write_path, 'w', newline="") as w:
            writer = csv.writer(w)
            for line in write_list:
                writer.writerow(line)
    
    def get_similarity(self, word_compaire,top_max=1):
        # 百度返回的score
        list_score=[]
        # 排序后的list
        list_range=[]
        # 需要比较的词top500，关键词key20，score 临时list
        temp_list=[]
        # 返回的list
        similarity_list=[]
        # 关键词个数
        keyword_num=len(self.key20_list)
        # 得到所有关键词与需要比较的词的相似度
        for i in range(keyword_num):
            try:
                list_score.append(self.client.simnet(self.key20_list[i], word_compaire)['score'])
            except Exception as e:
                list_score.append(0.01)
        # 排序，不改变原来的值
        list_range=sorted(list_score, reverse=True)
        # 确定返回值
        for i in range(top_max if top_max<=keyword_num else keyword_num):
            # 初始化为空
            temp_list=[]
            # 添加需要比较的值
            temp_list.append(word_compaire)
            temp_list.append(self.key20_list[list_score.index(list_range[i])])
            temp_list.append(list_range[i])
            similarity_list.append(temp_list)

        return similarity_list

smca = SimilarityCalculation()
smca.main()