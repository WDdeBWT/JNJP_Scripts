# coding:utf-8
# @__Author__ = "WDdeBWT"
# @__Date__ : 2018/03/27

import os
import re
import ast
import csv
import math
import json

import jieba
import jieba.analyse
import jieba.posseg as pseg

class Vectorization:
    def __init__(self, source_path):
        self.key20_list = ['生活垃圾','居民','选址','政府','排放标准','污染','环评','填埋场','冲突'
            ,'意见','参与','信息公开','监管','二噁英','风险','抗议','补偿','协商','征求意见','信任']
        self.source_path = source_path + '\\'
        self.stop_words_list_path = self.source_path + 'stopWord_1.txt'
        self.sim_list_path = self.source_path + 'demo60_Similarity.csv'
        self.pattern = re.compile(r"^[A-Za-z0-9\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+$")
        # 打开stopword_1.txt
        self.stop_words_list = []
        self.stop_words_list_ge = (
            line.strip()
            for line in open(self.stop_words_list_path, 'r', encoding='UTF-8').readlines())
        for wd in self.stop_words_list_ge:
            self.stop_words_list.append(wd)
        # 打开Similarity.csv
        self.sim_list = []
        with open(self.sim_list_path) as f:
            reader = csv.reader(f)
            self.sim_list = list(reader)

    def get_format_matrix(self, ori_string):
        standard_list_path = self.source_path + 'demo60-standard-fmt.csv'
        format_matrix = []
        with open(standard_list_path) as f:
            reader = csv.reader(f)
            format_matrix = list(reader)
        format_matrix.append(self.oristring_to_fmtlist(ori_string))
        return format_matrix

    # def get_similarity_vector(self, format_matrix):
    #     #fmt_list形如：['search_string', '0.106853626', '0.338369816' ... '0.035617875', '0', '0.645989816']
    #     return {'str_name': 'search_string', 'sim_A': '0.618', 'sim_B': '0.816', 'sim_C': '0.916', 'sim_D': '0.214', 'max_sim': 'C'}
    
    def get_similarity_vector(self, format_matrix=[]):
        # 封装结果
        result_data = dict()
        # 封装值，用于求最大值
        result_value = []
        # 从最后一个list开始逐一与锚进行比较
        i = format_matrix.__len__() - 1
        j = 1
        result_data['str_name'] = 'search_string'
        while (j < format_matrix.__len__() - 1):
            result = self.pearson(format_matrix[i], format_matrix[j])
            result_value.append(result)
            if (j == 1):
                result_data['sim_A'] = result
            if (j == 2):
                result_data['sim_B'] = result
            if (j == 3):
                result_data['sim_C'] = result
            if (j == 4):
                result_data['sim_D'] = result
            j += 1
        # print(result_value.index(max(result_value)))
        if(result_value.index(max(result_value)) == 0):
            result_data['max_sim'] = 'A'
        elif(result_value.index(max(result_value)) == 1):
            result_data['max_sim'] = 'B'
        elif(result_value.index(max(result_value)) == 2):
            result_data['max_sim'] = 'C'
        else:
            result_data['max_sim'] = 'D'
        # result_data['max_sim'] = max(result_value)
        return result_data

    
    def get_case(self, flag):
        if flag == 'A':
            return 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
        if flag == 'B':
            return 'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB'
        if flag == 'C':
            return 'CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC'
        if flag == 'D':
            return 'DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD'
        return '没有找到相似的案例诶 (T_T) '
    
    def get_img(self, flag):
        pic_1 = '/static/' + flag + '1.jpg'
        pic_2 = '/static/' + flag + '2.jpg'
        pic_3 = '/static/' + flag + '3.jpg'
        return {'pic_1': pic_1, 'pic_2': pic_2, 'pic_3': pic_3}
    
    def get_suggest(self, flag):
        if flag == 'A':
            return '111111111111111111111111111111111111111'
        if flag == 'B':
            return '222222222222222222222222222222222222222'
        if flag == 'C':
            return '333333333333333333333333333333333333333'
        if flag == 'D':
            return '444444444444444444444444444444444444444'
        return '我也想不到什么好的建议 (=_=) '


    def oristring_to_fmtlist(self, ori_string):
        word_list = []
        ori_string.replace("\n", "").replace(" ", "")
        for seg in jieba.cut(ori_string.strip()):
            if self.word_judge(seg.strip()):
                if self.word_replace(seg.strip()):
                    seg = self.word_replace(seg.strip())
                    word_list.append(seg.strip())
        li1 = []
        li1.append('file_name')
        li2 = []
        li2.append('file_name')
        word_set = set(word_list)
        for word_1 in word_set:
            times = 0
            for word_2 in word_list:
                if word_1 == word_2:
                    times += 1
            li1.append(word_1)
            li2.append(times)
        fmt_list = self.format_list(li1, li2)
        return fmt_list
    
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
        new_list.append(numbers[0])
        for wd in self.key20_list:
            flag = 0
            for i in range(len(words)):
                if words[i] == wd:
                    flag = 1
                    new_list.append(str(numbers[i]/math.sqrt(square_sum)))
            if flag == 0:
                new_list.append(str(0))
        return new_list
    
    # 皮尔逊相关系数
    def pearson(self, list_one =[],list_two = []):
        # 定义索引
        i = 1
        # 保存x,y乘积的和
        sum_xy = 0
        # 保存x的和
        sum_x = 0
        # 保存y的和
        sum_y = 0
        # 保存x的平方和
        sum_xx = 0
        # 保存y的平方和
        sum_yy = 0
        # 向量个数
        n = list_one.__len__() -1
        while (i < list_one.__len__()):
            sum_xy += (ast.literal_eval(list_one[i]) * ast.literal_eval(list_two[i]))
            sum_x += ast.literal_eval(list_one[i])
            sum_y += ast.literal_eval(list_two[i])
            sum_xx += (ast.literal_eval(list_one[i]) * ast.literal_eval(list_one[i]))
            sum_yy += (ast.literal_eval(list_two[i]) * ast.literal_eval(list_two[i]))
            # print(list_one[i])
            i += 1
        try:
            result = (n * sum_xy - sum_x * sum_y)/((math.sqrt(n * sum_xx - pow(sum_x,2)))* math.sqrt(n * sum_yy - pow(sum_y,2)))
        except :
            result = 1.1
        # print(result)
        return result

# ost = """
# 本报讯（记者 裴庆力 实习生 张乐 报道）2014年12月31日上午，市生活垃圾焚烧发电项目通过验收并启动，标志着该项目由建设阶段正式转入生产运营阶段。市委副书记、市长崔洪刚，副市长王瑜，中国天楹集团总裁曹德标共同启动项目机组，省电力质检中心处长李中秋宣布项目顺利通过验收。
# 据悉，市生活垃圾焚烧发电项目，位于滨城区滨孤路西侧滨北农场原址，技术工艺为机械炉排炉处理工艺，采用三炉两机的模式，总规模为日处理生活垃圾1200吨，占地面积约120亩。2010年4月市政府批准建设生活垃圾焚烧发电项目，2011年4月由中化国际招标代理公司通过招标的方式确定BOT项目投资商，同时注册成立了滨州天楹环保能源有限公司，项目于2013年5月正式开工建设。目前，项目除绿化景观工程外已全部结束，并于今年11月6日一次点火调试成功，11月18日并网发电。
# 该项目采用目前世界上领先的比利时机械炉排炉处理工艺，使用了世界最先进的西门子汽炉机组，实现了自动控制的集成化、智能化，各类排放指标均达到欧盟一级标准。工程获得省文明施工工地和省优质结构奖，并被列入国家优质结构奖候选名单。项目建成后，实现了国内同行业“五个领先”，即锅炉燃烧效率国内领先、热酌减率国内领先、二恶英排放世界领先、防臭技术工艺世界领先、厂区园林景观国内领先。
# """
# da = Vectorization('C:\\Users\\baiwt\\Desktop')
# format_matrix = da.get_format_matrix(ost)
# sim_dict = da.get_similarity_vector(format_matrix)
# case_description = da.get_case(sim_dict['max_sim'])
# img_dict = da.get_img(sim_dict['max_sim'])
# suggest_description = da.get_suggest(sim_dict['max_sim'])
# print(format_matrix)
# print("----------format_matrix----------")
# print(sim_dict)
# print("----------sim_dict----------")
# print(case_description)
# print("----------case_description----------")
# print(img_dict)
# print("----------img_dict----------")
# print(suggest_description)
# json_str = json.dumps({'format_matrix': format_matrix, 'sim_dict': sim_dict, 'case_description': case_description,
#     'img_dict': img_dict, 'suggest_description': suggest_description, 'status_code': 200, 'status_msg': '(^_^)'})
# print(json_str)