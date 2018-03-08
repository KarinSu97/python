'''
################################
采用bag of words方法
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

#读取数据
train_data=pd.read_csv('C:\\Users\\T\\Desktop\\python视频\\labeledTrainData.tsv',sep='\t',escapechar='\\')
train_data.head()
test_data=pd.read_csv('C:\\Users\\T\\Desktop\\python视频\\testData.tsv',sep='\t',escapechar='\\')
test_data.shape

#停用词
stopword=stopwords.words('english')

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
    return ' '.join(words)

#对训练集和测试集执行数据清洗
train_data['clean_review']=train_data.review.apply(clean_text)
test_data['clean_review']=test_data.review.apply(clean_text)

#提取特征，这里提取前5000个词汇
vectorizer=CountVectorizer(max_features=5000)
train_data_features=vectorizer.fit_transform(train_data.clean_review).toarray()
test_data_features=vectorizer.fit_transform(test_data.clean_review).toarray()

#建立分类模型，这里采用随机森林模型
forest=RandomForestClassifier(n_estimators=100)
model=forest.fit(train_data_features,train_data.sentiment)

#预测，计算混淆矩阵
confusion_matrix(train_data.sentiment,model.predict(train_data_features))

#对测试集进行预测
test_data['sentiment']=model.predict(test_data_features)
test_data.head()
