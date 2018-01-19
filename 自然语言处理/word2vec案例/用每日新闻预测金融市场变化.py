import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re
from nltk.stem import WordNetLemmatizer
from gensim.models.word2vec import Word2Vec
import gensim
import numpy as np
from sklearn.svm import SVC
from sklearn.cross_validation import cross_val_score
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Convolution2D,MaxPooling2D
from keras.layers.core import Dense,Dropout,Activation,Flatten

#设置神经网络框架用Theano
from keras import backend as K
K.set_image_dim_ordering('th')

#加载数据
file_path=r'C:\Users\T\Desktop\python视频\Combined_News_DJIA.csv'
data=pd.read_csv(file_path)
data.head(5)

#划分训练集和测试集
train=data[data['Date']<='2014-12-31']
test=data[data['Date']>='2015-01-01']

#建立语料库，即将所有句子都扁平化，成为一个列表的元素，用于生成word2vec
corpus=train[train.columns[2:]].values.flatten().astype(str)

#将每天各主题的句子串接为一个句子
X_train=train[train.columns[2:]].values.astype(str)
X_train=[" ".join(x) for x in X_train]
X_test=test[test.columns[2:]].values.astype(str)
X_test=[" ".join(x) for x in X_test]
y_train=train['Label'].values
y_test=test['Label'].values

#分词
corpus=[word_tokenize(sen) for sen in corpus]
X_train=[word_tokenize(sen) for sen in X_train]
X_test=[word_tokenize(sen) for sen in X_test]

#加载停用词
stopword=stopwords.words('english')

#判断是否出现数字
def hasNumbers(word):
    return bool(re.search(r'\d',word))

#判断是否出现特殊符号
def hasSymbol(word):
    return bool(re.match(r'[^\w]',word))

#lemma,词性归一化
wordnet_lemmatizer=WordNetLemmatizer()

#定义判断函数，判断是否出现数字、包含特殊符号
def check(word):
    word=word.lower()
    if word in stopword:
        return False
    elif hasNumbers(word) or hasSymbol(word):
        return False
    else:
        return True

#定义最终的数据清洗函数
def preprocessing(sen):
    res=[]
    for word in sen:
        if check(word):
            word=word.lower().replace("b'", '').replace('b"', '').replace('"', '').replace("'", '')
            res.append(wordnet_lemmatizer.lemmatize(word))
    return res

#数据清洗
corpus=[preprocessing(sen) for sen in corpus]
X_train=[preprocessing(sen) for sen in X_train]
X_test=[preprocessing(sen) for sen in X_test]

#训练word2vec模型,每个单词用长度为128的向量表示
model=Word2Vec(corpus,size=128,window=5,min_count=5,workers=4)

'''
方案一：取每个句子的单词的向量平均值作为每个句子的表示，然后用SVM模型进行预测
'''
#获取单词列表
vocab=model.wv.vocab

#计算每个句子的单词向量平均值
def get_vector(text):
    res=np.zeros([128])
    count=0
    for word in text:
        if word in vocab:
            res+=model[word]
            count+=1
    return res/count

X_train1=[get_vector(sen) for sen in X_train]
X_test1=[get_vector(sen) for sen in X_test]

#建立SVM模型
params = [0.1,0.5,1,3,5,7,10,12,16,20,25,30,35,40]
test_scores=[]
for param in params:
    clf=SVC(gamma=param)
    test_score=cross_val_score(clf,X_train1,y_train,cv=3,scoring='roc_auc')
    test_scores.append(np.mean(test_score))

plt.plot(params,test_scores)

clf=SVC(gamma=15)
clf.fit(X_train1,y_train)
clf.score(X_test1,y_test)

'''
采用CNN进行预测
'''
#只取每天新闻的前256个单词，不足或缺失的都用0补上
def transform_to_matrix(x, padding_size=256, vec_size=128):
    res=[]
    for sen in x:
        matrix=[]
        for i in range(padding_size):
            try:
                matrix.append(model[sen[i]].tolist())
            except:
                matrix.append(np.zeros(vec_size).tolist())
        res.append(matrix)
    return res

X_train2=transform_to_matrix(X_train)
X_test2=transform_to_matrix(X_test)
X_train2=np.array(X_train2)
X_test2=np.array(X_test2)

#修改X_train2和X_test2的维度，以告诉CNN每个样本点是独立的
X_train2=X_train2.reshape(X_train2.shape[0],1,X_train2.shape[1],X_train2.shape[2])
X_test2=X_test2.reshape(X_test2.shape[0],1,X_test2.shape[1],X_test2.shape[2])

#建立CNN模型
batch_size = 32
n_filter = 16
filter_length = 4
nb_epoch = 5
n_pool = 2
model=Sequential()
model.add(Convolution2D(n_filter,filter_length,filter_length,input_shape=(1,256,128)))
model.add(Activation('relu'))
model.add(Convolution2D(n_filter,filter_length,filter_length))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(n_pool, n_pool)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(128))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(1))
model.add(Activation('softmax'))
model.compile(loss='mse',optimizer='adadelta',metrics=['accuracy'])
model.fit(X_train2, y_train, batch_size=batch_size, nb_epoch=nb_epoch)

#预测
score = model.evaluate(X_test2, y_test, verbose=0)
print('Test score:', score[0])
print('Test accuracy:', score[1])