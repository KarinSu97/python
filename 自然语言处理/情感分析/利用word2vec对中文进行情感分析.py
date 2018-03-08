import pandas as pd
import numpy as np
import jieba
from sklearn.cross_validation import train_test_split
import re
from gensim.models.word2vec import Word2Vec
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix
from sklearn.ensemble import RandomForestClassifier

#读取数据
neg=pd.read_excel('C:\\Users\\T\\Desktop\\python视频\\neg.xls',header=None,index=None)
pos=pd.read_excel('C:\\Users\\T\\Desktop\\python视频\\pos.xls',header=None,index=None)

#合并数据，并添加标签
sentiment=np.array(np.concatenate((np.zeros(len(neg)),np.ones(len(pos)))),dtype=int)
data=pd.DataFrame()
data['sentence']=np.concatenate((neg[0],pos[0]))
data['sentiment']=sentiment
data.head()

#停用词
with open('C:\\Users\\T\\Desktop\\python视频\\stopword.txt') as file:
    lines=file.readlines()
    stopwords=[re.sub('\\n','',line) for line in lines]

#定义分词和文本清洗函数
def cut_clean(text):
    text=list(jieba.cut(text))
    words=[w for w in text if w not in stopwords]
    return words

#对文本进行分词
data['words']=data.sentence.apply(cut_clean)
data.head()

#将数据划分为训练集和测试集
train_data,test_data=train_test_split(data,test_size=0.2)

#训练词向量模型，size表示神经网络的层数，min_count是过滤出现频次比较低的词汇
w2c_model=Word2Vec(train_data.words,size=300,min_count=10)

#计算每个句子词汇的平均值
def compute_mean(text):
    vec=np.zeros(300).reshape((1,300))
    count=0
    for word in text:
        if word in w2c_model:
            vec+=w2c_model[word].reshape((1,300))
            count+=1
    if count!=0:
        vec/=count
    return vec

train_data_features=np.concatenate([compute_mean(words) for words in train_data.words])
train_data_features.shape

#建立分类器，这里采用随机森林
forest=RandomForestClassifier(n_estimators=100)
forest=forest.fit(train_data_features,train_data.sentiment)

#对测试集进行预测
test_data_features=np.concatenate([compute_mean(words) for words in test_data.words])
confusion_matrix(test_data.sentiment,forest.predict(test_data_features))