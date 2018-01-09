'''
################################
LDA主题分析模型：新闻主题分析
################################
'''
import os
import jieba
import re
from gensim import models,corpora
import gensim
import jieba.posseg

#清洗文本，去除换行符、日期、数字、英文、ascii编码
def clean_text(text):
    text=re.sub("\\r|\\n",'',text)
    text=re.sub("[0-9]{2,4}年[0-9]{1,2}月[0-9]{1,2}日",'',text)
    text=re.sub('[0-9]*','',text)
    text=re.sub('[a-zA-Z]','',text)
    text=re.sub('[\x00-\xff]*','',text)
    return text

#加载停用词
stopwords=[]
with open(r'C:\Users\T\Desktop\python视频\stopword.txt','rb') as f:
    lines=f.readlines()
    for line in lines:
        stopwords.append(re.sub("\\r\\n",'',line.decode('utf-8')))

#加载数据
file_path=r'C:\Users\T\Desktop\python视频\Database\SogouC\Sample'
##读取文件夹列表
file_list=os.listdir(file_path)
docs=[]
labels=[]
for file in file_list:
    path1=os.path.join(file_path,file)
    doc_list=os.listdir(path1)
    for doc in doc_list:
        words = []
        path2=os.path.join(path1,doc)
        with open(path2,'rb') as f:
            text=f.read().decode('utf-8')
            text=clean_text(text)
            word_cut=jieba.posseg.cut(text)
            for item in word_cut:
                #去除停顿词并且只保留名词和动名词
                if item.word not in stopwords and item.flag in ['n','vn']:
                    words.append(item.word)
        docs.append(words)
        labels.append(file)

#将词汇用index标记,并统计词汇的出现次数
dictionary=corpora.Dictionary(docs)
corpus=[dictionary.doc2bow(text) for text in docs]

#建立lda主题分析模型,主题数需要事先指定，这里设置为9
lda=models.LdaModel(corpus=corpus,id2word=dictionary,num_topics=9)

#打印各主题
lda.print_topics(num_topics=9,num_words=20)

#获取文档的主题
topics=lda.get_document_topics(corpus)
for topic in topics:
    print(topic)