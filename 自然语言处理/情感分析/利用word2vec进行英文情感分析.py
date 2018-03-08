'''
################################
采用word2vec方法
################################
'''
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import re
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
import nltk
from gensim.models.word2vec import Word2Vec

#读取数据
train_data=pd.read_csv('C:\\Users\\T\\Desktop\\python视频\\labeledTrainData.tsv',sep='\t',escapechar='\\')
train_data.head()
test_data=pd.read_csv('C:\\Users\\T\\Desktop\\python视频\\testData.tsv',sep='\t',escapechar='\\')
test_data.shape

#停用词
stopword=stopwords.words('english')

#分词器
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

#定义数据清洗函数
def clean_text(text):
    #去除文本中的html标签
    text=BeautifulSoup(text,'html.parser').get_text()
    #去除非英文字符
    text=re.sub('[^a-zA-Z]',' ',text)
    #转变为小写字母
    words=text.lower().split()
    #去除停用词
    words=[w for w in words if w not in stopword]
    return words

def split_sentences(review):
    raw_sentences=tokenizer.tokenize(review)
    sentences = [clean_text(s) for s in raw_sentences if s]
    return sentences

#对数据进行清洗
train_data_sentences = sum(train_data.review.apply(split_sentences),[])

#训练word2vec模型
w2v_model=Word2Vec(train_data_sentences,size=300,window=10,min_count=40)
w2v_model.most_similar('man')

#计算每个句子词向量的均值
def to_review_vector(review):
    words = clean_text(review)
    array = np.array([w2v_model[w] for w in words if w in w2v_model])
    return pd.Series(array.mean(axis=0))

train_data_features = train_data.review.apply(to_review_vector)

#建立分类器，这里采用随机森林模型
forest = RandomForestClassifier(n_estimators = 100, random_state=42)
forest = forest.fit(train_data_features, train_data.sentiment)

#对训练集进行预测，计算混淆矩阵
confusion_matrix(train_data.sentiment,forest.predict(train_data_features))

#对测试集进行预测
test_data_features=test_data.review.apply(to_review_vector)
test_data['sentiment']=forest.predict(test_data_features)
test_data.head()