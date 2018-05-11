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
        self.pattern = re.compile(r"^[A-Za-z0-9\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+$")
        # 打开stopword_1.txt
        self.stop_words_list_path = self.source_path + 'stopWord_1.txt'
        self.stop_words_list = []
        self.stop_words_list_ge = (
            line.strip()
            for line in open(self.stop_words_list_path, 'r', encoding='UTF-8').readlines())
        for wd in self.stop_words_list_ge:
            self.stop_words_list.append(wd)
        # 打开Similarity.csv
        self.sim_list_path = self.source_path + 'demo60_Similarity.csv'
        self.sim_list = []
        with open(self.sim_list_path) as f:
            reader = csv.reader(f)
            self.sim_list = list(reader)
        # 打开suggestion.csv
        self.sug_list_path = self.source_path + 'suggestion.csv'
        self.sug_list = []
        with open(self.sug_list_path , encoding="utf-8") as f:
            reader = csv.reader(f)
            self.sug_list = list(reader)

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
                result_data['sim_A'] = str(result)[0:6]
            if (j == 2):
                result_data['sim_B'] = str(result)[0:6]
            if (j == 3):
                result_data['sim_C'] = str(result)[0:6]
            if (j == 4):
                result_data['sim_D'] = str(result)[0:6]
            j += 1
        if max(result_value) == 1.1 or max(result_value) <= 0.8:
            result_data['sim_A'] = '--'
            result_data['sim_B'] = '--'
            result_data['sim_C'] = '--'
            result_data['sim_D'] = '--'
            result_data['max_sim'] = '--'
            return result_data
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
        case_a = '佛山南海垃圾焚烧发电厂，看生活垃圾欲火重生变绿色能源\n佛山南海垃圾焚烧厂位于南海固废处理环保产业园内，是一家主要从事垃圾焚烧发电、城乡一体化垃圾压缩转运、污泥处理、餐厨垃圾处理等业务的固废处理企业。\n在厂区中控室内的大屏幕上，实时显示着焚烧炉的火焰，以及焚烧流程中多个监控点的参数情况，以保证炉内温度超过标准要求，使得最令百姓“谈之色变”的二噁英得到充分分解，再加上强大的过滤系统，垃圾燃烧后排放的气体有害物质几乎为零，远超国家安全标准。而燃烧垃圾产生热能，转化为电能后经电网进入千家万户。\n为了消除“邻居们”的不理解，破解“邻避效应”，固废产业园首先修炼内功，以欧盟标准建设园区；其次，实施透明化管理、立体化监督，政府引入第三方专业公司对园区内的设施进行24小时全天候不间断的专业化、常态化监管，并聘请周边社区、村委代表为“环境监督员”，不定期对企业进行抽查监督；最后是共赢，让“邻居”成为环保的同盟军。\n附近住户大部分对此地的垃圾焚烧发电厂的态度还是比较客观的。首先确实并不存在垃圾填埋场常出现的严重异味，这一点在现场是最明显的感受。居民表示，在2000年以前，南海垃圾填埋场会常年散发出浓烈的恶臭，后来经过一期工程的改造，因为当时工艺不完善，仍然造成二次污染。直到近年由南海绿电接管运营，建立了二期工程并停用了原设施后，附近区域的异味才不再出现。许多学生甚至表示生活了几年，竟然完全不知道附近不到2公里就有一个垃圾焚烧发电厂，这也可以从侧面说明附近的空气质量良好。\n垃圾焚烧发电技术在先进技术和有效管控的双重作用下，可以成为替代垃圾填埋、解决城市垃圾之围的先进方案，为人担忧的二次污染也可以有效解决。'
        case_b = '2009年12月23日，在广州市城管委月度接访中，有广清交界居民到访，拿出当年9月10日至24日的《广州市花都区生活垃圾综合处理中心建设项目环境影响评价公示》复印件，称许多居民并不知道当年政府部门已在环评。选址几经波折后，最终落在区内西北侧的赤坭镇。此前，花都垃圾焚烧厂曾拟选址狮岭镇汾水林场和前进村两地，最终因抗议众多而被搁置。最终花都区循环经济产业园落户花都赤坭镇十八岭鲤塘村小水库旁，包括焚烧厂在内的整个循环经济产业园区占地约55.72万平方米。按照广州多年的征地惯例，农村土地被政府征去之后，村集体一般会获得一定比例的留用地返还，留给村作为发展经济用地。但规划报告显示，由于项目地处花都区以西的远郊地带，人口稀少、基础设施不足，不适宜按常规征用生态用地落实留用地方式维持村经济发展。所以，这次留用地指标将以折算货币补偿的方式进行补偿，具体采取每处理一吨垃圾补贴一定金额的方式实施，也就是说，花都循环经济产业园运转以后，每处理一吨垃圾污染物，选址所在地的花都赤坭镇鲤塘村都会获得一定的补贴。该生活垃圾焚烧发电厂据最近居民楼8公里 赤坭镇位于花都的西北部，距中心城区35公里，距新华镇13公里，北面是清远市，西南面是佛山三水区。而对于业主们来说最关心的一个问题就是这个垃圾焚烧厂离自己家究竟有多远。我们可以看到此次选址，政府部门特意避开了居住区，即使是距离垃圾焚烧厂最近的楼盘也在垃圾焚烧厂8公里之外。据了解，该选址位于赤泥镇鲤塘村猪仔迳水库附近，附近居民很少，记者观察发现离选址最近的住房也有500米的距离。'
        case_c = '村民质疑焚烧厂环评造假，蓟县垃圾焚烧发电厂位于天津市蓟县和河北唐山市玉田县的交界处，由天津绿色动力再生能源有限公司承建，预计日处理生活垃圾700吨。该项目于2014年通过了环境影响评价。然而该项目的环评方——天津市环境影响评价中心，因与当地环保部门有关联，逾期未脱钩，环评资质已经在2016年7月被环保部注销。据当地村民介绍，蓟县垃圾焚烧厂在2016年4月底开始试运行，4月初开始大量运进垃圾。附近村民认为，焚烧厂的污染导致村里孩子出现身体不适，对焚烧厂表示反对。2016年6月22日，与蓟县焚烧厂相邻的河北玉田县大庞各庄等六个村民委员会，由于质疑环评公众参与调查问卷造假，向天津市环保局申请公开“蓟县生活垃圾焚烧发电项目环境影响评价公众参与调查问卷以及被调查人员名单”。申请人之一，东九户村村委会书记张子臣对记者说，调查问卷里大部分的名单都是别人代签的，甚至还有死亡人员。他表示，做调查问卷的找到了东九户村的一个人，许诺了一定的好处，让他去代签调查问卷。环保组织自然之友2016年8月22日曾向天津市环境保护局发建议函，请求该局叫停天津蓟县垃圾焚烧发电项目试生产，并且重做环评。2016年7月11日，天津市环保局做出答复，张子臣等申请公开的信息涉及个人隐私，不予以公开。天津市环保局称，法律法规并未明确规定环境影响评价公众参与调查表和被调查人员名单是否属于应当公开的内容，但《侵权责任法》和《人民法院关于确定民事侵权精神损害赔偿责任若干问题的解释》对保护公民的隐私权，姓名权做出了规定，天津市环保局认为调查问卷属于法律保护的公民隐私权和姓名权，依法不得公开。随后六个村民委员会表示不服，向环保部申请行政复议。10月5日，张子臣收到环保部的行政复议决定书。'
        case_d = '锅顶山生活垃圾焚烧厂于2009年9月竣工，2012年底三条生产线运行，主要接纳和处理汉阳、硚口地区的城市生活垃圾。锅顶山医废垃圾焚烧厂，2012年7月试运行。\n2013年7月，湖北省环保厅环境违法监察通报显示，锅顶山垃圾焚烧存在未经环评验收擅自生产、治污设施未落实、擅自处置垃圾滤液、防护距离内居民未搬迁等严重违法问题。通报要求该厂立即停产整改，未经批准不得生产。当年10月12日，环保部公开通报了全国72家污染企业名单，锅顶山生活垃圾焚烧厂的运营方武汉博瑞能源环保有限公司也名列其中。2013年底，生活垃圾焚烧厂被叫停。2014年元旦，锅顶山生活垃圾焚烧厂、医废垃圾焚烧厂分别按300米和400米安全距离的要求，启动居民搬迁行动。2014年底，生活垃圾焚烧厂重新试运行。但其仍然未通过当地环保部门的环评。\n在锅顶山焚烧厂附近小区约50户居民。每个家庭面朝焚烧厂一侧的窗户，都为防止异味和粉尘入室采取了措施，双层玻璃、双层窗帘、塑料膜封窗，有的用玻璃胶封死。65岁的黄望生，家里只留背向垃圾厂的阳台窗户，其他窗户全用塑料膜密封，他还是经常在凌晨后被刺鼻气味呛醒，即便被子裹头也无济于事。扛不住了，他就和老伴深夜跑出去，“那味道难受得都想撞墙”。他和老伴都有咽炎、肺部疾病。居民黄先生6岁的儿子患上了罕见的过敏性气管纤维母细胞瘤，全家寻访了许多大城市医院，一直不能治愈。“儿子每次发病都咳着咳着就开始喷血，几次都差点没抢救过来”。他说，他和妻子也患有鼻炎、咽炎等呼吸道疾病。\n'
        if flag == 'A':
            return case_a
        if flag == 'B':
            return case_b
        if flag == 'C':
            return case_c
        if flag == 'D':
            return case_d
        return '没有找到相似的案例诶 (T_T) '
    
    def get_img(self, flag):
        pic_1 = '/static/Bayes_img/' + flag + '1.jpg'
        pic_2 = '/static/Bayes_img/' + flag + '2.jpg'
        pic_3 = '/static/Bayes_img/' + flag + '3.jpg'
        return {'pic_1': pic_1, 'pic_2': pic_2, 'pic_3': pic_3}
    
    def get_suggest(self, flag):
        sug_dict = {}
        if flag == 'A':
            for sug in self.sug_list:
                if sug[0] == 'A':
                    sug_dict["sug_" + sug[1][1:]] = sug[2]
        elif flag == 'B':
            for sug in self.sug_list:
                if sug[0] == 'B':
                    sug_dict["sug_" + sug[1][1:]] = sug[2]
        elif flag == 'C':
            for sug in self.sug_list:
                if sug[0] == 'C':
                    sug_dict["sug_" + sug[1][1:]] = sug[2]
        elif flag == 'D':
            for sug in self.sug_list:
                if sug[0] == 'D':
                    sug_dict["sug_" + sug[1][1:]] = sug[2]
        return sug_dict
    
    def get_order(self):
        order_str = 'RE=居民; SS=选址; PO=污染; EA=环评; CO=冲突; PA=参与; ID=信息公开; DI=二噁英; BC=补偿; GO=政府;'
        return order_str

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