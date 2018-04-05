import re
import os
import pandas as pd
from sklearn.cross_validation import train_test_split
from gensim.models.word2vec import Word2Vec
import numpy as np
from sklearn import svm
from sklearn.metrics import confusion_matrix
from sklearn.cross_validation import cross_val_score
import jieba.posseg
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer

#文件路径
path1='C:\\Users\\T\\Desktop\\Distribution Data HIT\\Corpus Data\\XML'

#获取所有文件列表
file_list=[]
for root,dirs,files in os.walk(path1):
    for file in files:
        if not file.endswith('.txt'):
            file_list.append(os.path.join(root,file))

#读取每个文件对应的显式句子
type=[]
Re1NO=[]
Source=[]
Sentence=[]
Connective=[]
for i in file_list:
    f=open(i,'r').read()
    #获取句子是隐式还是显式类型
    pattern1='<Sense type="(.*?)" RelNO'
    this_type=re.compile(pattern1).findall(f)
    type.extend(this_type)
    #获取句子的关系类型
    pattern2='<Sense type=".*?" RelNO="(.*?)" content=".*">'
    this_RelNO=re.compile(pattern2).findall(f)
    Re1NO.extend(this_RelNO)
    #获取句子的内容
    pattern3='<Source>(.*?)</Source>'
    this_Source=re.compile(pattern3).findall(f)
    Source.extend(this_Source)
    #获取句子是复句还是单句
    sentence=i[-2:]
    Sentence.extend(list(np.repeat(sentence,len(this_Source))))
    #获取连接词
    pattern4='<Connectives>\n\t\t<Span>.*</Span>\n\t\t<Content>(.*?)</Content>\n\t</Connectives>'
    connective=re.compile(pattern4).findall(f)
    Connective.extend(connective)

#构造数据集，筛选显式句子
data=pd.DataFrame()
data['type']=type
data['RelNO']=Re1NO
data['Source']=Source
data['Sentence']=Sentence
data['Connective']=Connective
data.head()
data=data[data['type']=='Explicit']
data.head()

#提取数据的类型，这里只提取第一大类，即将数据总共分为4类
data['RelNO']=[int(i[0]) for i in data['RelNO']]
data.head()
data.shape

#将每个句子内容转化为列表形式
def tran_to_list(text):
    return text.split(' ')
data['Source']=data['Source'].apply(tran_to_list)
data.index=np.arange(len(data))
data.head()

#将结果转化为二分类
def change_2class(text,l=[]):
    if text in l:
        text=0
    else:
        text=1
    return text

data['RelNO1']=data['RelNO'].apply(change_2class,l=[2,3,4])
data['RelNO2']=data['RelNO'].apply(change_2class,l=[1,3,4])
data['RelNO3']=data['RelNO'].apply(change_2class,l=[1,2,4])
data['RelNO4']=data['RelNO'].apply(change_2class,l=[1,2,3])

#获取每一类前n个高频连接词,默认取前70个
def get_topn_conn(i,size=50):
    Connective=list(data['Connective'][data['RelNO']==i])
    Conn=[]
    for j in Connective:
        Conn.extend(j.split(';'))
    Conn_count=Counter(Conn)
    topn=Conn_count.most_common(size)
    Conn_topn=[]
    for word,freq in topn:
        Conn_topn.append(word)
    return Conn_topn
Conn1=get_topn_conn(1)
Conn2=get_topn_conn(2)
Conn3=get_topn_conn(3)
Conn4=get_topn_conn(4)
Conn_all=[]
Conn_all.extend(Conn1)
Conn_all.extend(Conn2)
Conn_all.extend(Conn3)
Conn_all.extend(Conn4)
Conn_all=list(set(Conn_all))

#统计词频
def filter_topn(text):
    words=[]
    for i in text:
        if i in Conn_all:
            words.append(i)
    return ' '.join(words)
data['Source1']=data['Source'].apply(filter_topn)
vec=CountVectorizer(vocabulary=Conn_all)
words_matrix=vec.fit_transform(data['Source1'])

#抽取1:1的正负例
def get_data(col_name):
    index1=list(data.index[data[col_name]==1])
    index2=list(data[data[col_name]==0].sample(len(index1)).index)
    index1.extend(index2)
    np.random.shuffle(index1)
    return words_matrix[index1],data[col_name][index1]

#二分类：时序关系判断
x_data,y_data=get_data('RelNO1')
for i in np.arange(0.1,5,0.1):
    model=svm.SVC(kernel='rbf',gamma=i)
    # 采用10折交叉验证确定最优参数
    transformed_scores = cross_val_score(model, x_data, y_data, scoring='accuracy', cv=10)
    acc = np.mean(transformed_scores)
    print(str(i)+":"+str(acc))

model = svm.SVC(kernel='rbf', gamma=0.4)
model.fit(x_data, y_data)
pred = model.predict(x_data)
confusion_matrix(y_data, pred)

#二分类：因果关系判断
x_data,y_data=get_data('RelNO2')
for i in np.arange(0.1,5,0.1):
    model=svm.SVC(kernel='rbf',gamma=i)
    # 采用10折交叉验证确定最优参数
    transformed_scores = cross_val_score(model, x_data, y_data, scoring='accuracy', cv=10)
    acc = np.mean(transformed_scores)
    print(str(i)+":"+str(acc))

model = svm.SVC(kernel='rbf', gamma=0.2)
model.fit(x_data, y_data)
pred = model.predict(x_data)
confusion_matrix(y_data, pred)

#二分类：比较关系判断
x_data,y_data=get_data('RelNO3')
for i in np.arange(0.1,5,0.1):
    model=svm.SVC(kernel='rbf',gamma=i)
    # 采用10折交叉验证确定最优参数
    transformed_scores = cross_val_score(model, x_data, y_data, scoring='accuracy', cv=10)
    acc = np.mean(transformed_scores)
    print(str(i)+":"+str(acc))

model = svm.SVC(kernel='rbf', gamma=0.4)
model.fit(x_data, y_data)
pred = model.predict(x_data)
confusion_matrix(y_data, pred)

#二分类：扩展关系判断
x_data,y_data=get_data('RelNO4')
for i in np.arange(0.1,5,0.1):
    model=svm.SVC(kernel='rbf',gamma=i)
    # 采用10折交叉验证确定最优参数
    transformed_scores = cross_val_score(model, x_data, y_data, scoring='accuracy', cv=10)
    acc = np.mean(transformed_scores)
    print(str(i)+":"+str(acc))

model = svm.SVC(kernel='rbf', gamma=0.2)
model.fit(x_data, y_data)
pred = model.predict(x_data)
confusion_matrix(y_data, pred)

#四分类
for i in np.arange(0.1,2,0.1):
    model=svm.SVC(kernel='rbf',gamma=i)
    # 采用10折交叉验证确定最优参数
    transformed_scores = cross_val_score(model, words_matrix, data['RelNO'], scoring='accuracy', cv=10)
    acc = np.mean(transformed_scores)
    print(str(i)+":"+str(acc))

model = svm.SVC(kernel='rbf', gamma=0.3)
model.fit(words_matrix, data['RelNO'])
pred = model.predict(words_matrix)
confusion_matrix(data['RelNO'], pred)

