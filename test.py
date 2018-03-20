import jieba
print('----------↓ 1 ↓----------')
seg_list1 = jieba.cut(r'垃圾焚烧处理内忧外患 破镜才能重生|垃圾焚烧_报告大厅www.chinabgao.com', cut_all=True)
for seg in seg_list1:
    print(seg)
print('----------↓ 2 ↓----------')
seg_list1 = jieba.cut(r'垃圾焚烧设施行业预测报告_2014-2018年中国垃圾焚烧设施行业发展前景预测报告_行业预测报告网forecast.chinabgao.com', cut_all=True)
for seg in seg_list1:
    print(seg)
print('----------↓ 3 ↓----------')
seg_list1 = jieba.cut(r'垃圾焚烧与烟气除尘研究报告_2017-2022年中国垃圾焚烧与烟气除尘行业市场供需前景预测深度研究报告_中国报告大厅www.chinabgao.com', cut_all=True)
for seg in seg_list1:
    print(seg)
    
    
    
