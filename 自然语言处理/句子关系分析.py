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
data.index=np.arange(len(data))
data.head()
data.shape

#将每个句子内容转化为列表形式
def tran_to_list(text):
    return text.split(' ')
data['Source']=data['Source'].apply(tran_to_list)
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

#获取每一类前n个高频连接词,默认取前7个
def get_topn_conn(i,size=10):
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

#抽取1:1的正负例
def get_data(col_name):
    index1=list(data.index[data[col_name]==1])
    index2=list(data[data[col_name]==0].sample(len(index1),random_state=1234).index)
    index1.extend(index2)
    np.random.shuffle(index1)
    return index1

#定义预测函数
def word2vec_svm(size,min_count,gamma,data,y,confusion_mat=False):
    #使用word2vec提取词向量
    w2c_model=Word2Vec(data.Source,size=size,min_count=min_count)
    #计算每个句子词汇的平均值
    def compute_mean(text):
        vec=np.zeros(size).reshape((1,size))
        count=0
        for word in text:
            if word in w2c_model and word in Conn_all:
                vec+=w2c_model[word].reshape((1,size))
                count+=1
        if count!=0:
            vec/=count
        return vec
    data_features=np.concatenate([compute_mean(words) for words in data.Source])
    index1=get_data(y)
    data_features=data_features[index1]
    #建立分类器，这里采用SVM
    model=svm.SVC(kernel='rbf',gamma=gamma)
    #采用10折交叉验证确定最优参数
    transformed_scores = cross_val_score(model,data_features,data[y][index1],scoring='accuracy', cv=10)
    acc=np.mean(transformed_scores)
    if confusion_mat==True:
        model.fit(data_features,data[y][index1])
        pred=model.predict(data_features)
        mat=confusion_matrix(data[y][index1],pred)
        all_acc=sum(np.diag(mat))/len(pred)
    else:
        mat=[]
        all_acc=[]
    return acc,mat,all_acc


#二分类：判断是否是时序关系
for gamma in np.arange(0.1,2.0,0.1):
   acc,_,_=word2vec_svm(20,5,gamma,data=data,y='RelNO1')
   print(str(gamma)+':'+str(acc))

_,mat,all_acc=word2vec_svm(20,5,gamma=1.0,data=data,y='RelNO1',confusion_mat=True)
print(mat)
print(all_acc)

#二分类：判断是否是因果关系
for gamma in np.arange(0.1,2.0,0.1):
   acc,_,_=word2vec_svm(20,5,gamma,data=data,y='RelNO2')
   print(str(gamma)+':'+str(acc))

_,mat,all_acc=word2vec_svm(20,5,gamma=1.6,data=data,y='RelNO2',confusion_mat=True)
print(mat)
print(all_acc)

#二分类：判断是否是比较关系
for gamma in np.arange(0.1,2.0,0.1):
   acc,_,_=word2vec_svm(20,5,gamma,data=data,y='RelNO3')
   print(str(gamma)+':'+str(acc))

_,mat,all_acc=word2vec_svm(20,5,gamma=1.5,data=data,y='RelNO3',confusion_mat=True)
print(mat)
print(all_acc)

#二分类：判断是否是扩展关系
for gamma in np.arange(0.1,2.0,0.1):
   acc,_,_=word2vec_svm(20,5,gamma,data=data,y='RelNO4')
   print(str(gamma)+':'+str(acc))

_,mat,all_acc=word2vec_svm(20,5,gamma=1.6,data=data,y='RelNO4',confusion_mat=True)
print(mat)
print(all_acc)

#四分类
#定义预测函数
def word2vec_svm(size,min_count,gamma,data,y,confusion_mat=False):
    #使用word2vec提取词向量
    w2c_model=Word2Vec(data.Source,size=size,min_count=min_count)
    #计算每个句子词汇的平均值
    def compute_mean(text):
        vec=np.zeros(size).reshape((1,size))
        count=0
        for word in text:
            if word in w2c_model and word in Conn_all:
                vec+=w2c_model[word].reshape((1,size))
                count+=1
        if count!=0:
            vec/=count
        return vec
    data_features=np.concatenate([compute_mean(words) for words in data.Source])
    #建立分类器，这里采用SVM
    model=svm.SVC(kernel='rbf',gamma=gamma)
    #采用10折交叉验证确定最优参数
    transformed_scores = cross_val_score(model,data_features,data[y],scoring='accuracy', cv=10)
    acc=np.mean(transformed_scores)
    if confusion_mat==True:
        model.fit(data_features,data[y])
        pred=model.predict(data_features)
        mat=confusion_matrix(data[y],pred)
        all_acc=sum(np.diag(mat))/len(pred)
    else:
        mat=[]
        all_acc=[]
    return acc,mat,all_acc

for gamma in np.arange(0.1,2.0,0.1):
   acc,_,_=word2vec_svm(20,5,gamma,data=data,y='RelNO')
   print(str(gamma)+':'+str(acc))

_,mat,all_acc=word2vec_svm(20,5,gamma=1.8,data=data,y='RelNO',confusion_mat=True)
print(mat)
print(all_acc)



