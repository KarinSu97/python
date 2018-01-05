import jieba
import jieba.posseg
import jieba.analyse

#分词
'''
jieba分词有三种模式：
全局模式：全局模式是根据所有的分词可能结果进行分词
精准模式：精准模式是根据词汇的重要性，选择最可能的一种分词模式
搜索引擎模式：采用搜索引擎中的分词进行分词
'''

#全局模式
sentence='我爱上海东方明珠'
w1=jieba.cut(sentence,cut_all=True)
for item in w1:
    print(item)

w1=jieba.lcut(sentence,cut_all=True)   #直接返回列表形式

#精准模式
sentence='我爱上海东方明珠'
w1=jieba.cut(sentence,cut_all=False)
for item in w1:
    print(item)

#搜索引擎模式
sentence='我爱上海东方明珠'
w1=jieba.cut_for_search(sentence)
for item in w1:
    print(item)

w1=jieba.lcut_for_search(sentence)   #直接返回列表形式

#词性标注,word是单词，flag是对应的词性
sentence='我爱上海东方明珠'
w1=jieba.posseg.cut(sentence)
for item in w1:
    print(item.word+":"+item.flag)

#加载自定义词典
jieba.load_userdict('C:/Program Files/Anaconda3/Lib/site-packages/jieba/dict1.txt')
sentence='天善智能是一个好机构'
w1=jieba.posseg.cut(sentence)
for item in w1:
    print(item.word+":"+item.flag)

#动态添加或删除词汇
jieba.add_word('天善智能')
jieba.lcut('天善智能是一个好机构')
jieba.del_word('天善智能')

#修改词频，使得某些词可以切分出来
jieba.lcut('如果放到旧词典中将出错')
jieba.suggest_freq(("中",'将'),True)
jieba.lcut('如果放到旧词典中将出错')

#提取关键词,基于TF-IDF
sentence='天善智能是一个好机构'
tag=jieba.analyse.extract_tags(sentence,3)   #提取三个关键词
print(tag)

#返回词语的位置
sentence='我喜欢上海的东方明珠，是因为东方明珠很好看'
w1=jieba.tokenize(sentence)
for item in w1:
    print(item)