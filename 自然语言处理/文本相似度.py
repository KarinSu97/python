from gensim import corpora,models,similarities
import jieba
from collections import defaultdict

#读取文档
d1=open('C:/Users/T/Desktop/d1.txt','r').read()
d2=open('C:/Users/T/Desktop/d2.txt','r').read()

#分词
w1=jieba.cut(d1)
w2=jieba.cut(d2)

#将词语转变为空格连接的形式
w1_new=''
for item in w1:
    w1_new+=item+" "
w2_new=''
for item in w2:
    w2_new+=item+" "

#建立文档库
documents=[w1_new,w2_new]
texts=[[word for word in document.split()] for document in documents]

#计算词频
freq=defaultdict(int)
for text in texts:
    for word in text:
        freq[word]+=1

#过滤掉低频词汇
texts=[[word for word in text if freq[word]>=3] for text in texts]

#读取要计算相似度的文档
d3=open('C:/Users/T/Desktop/d3.txt','r').read()
w3=jieba.cut(d3)
w3_new=''
for item in w3:
    w3_new+=item+" "
new_vec=w3_new.split()

#建立字典
dictionary=corpora.Dictionary(texts)

#将词汇列表转变为稀疏向量形式
corpus=[dictionary.doc2bow(text) for text in texts]
new_doc=dictionary.doc2bow(new_vec)

#计算相似度
tfidf=models.TfidfModel(corpus)
feature_num=len(dictionary.token2id.keys())   #计算特征数
index=similarities.SparseMatrixSimilarity(tfidf[corpus],num_features=feature_num)   #计算稀疏矩阵
sim=index[tfidf[new_doc]]
print(sim)  #相似度
