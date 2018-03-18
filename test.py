import jieba
seg_list = jieba.cut('垃圾焚烧 - 北极星环保网', cut_all=True)
for seg in seg_list:
    print(seg)