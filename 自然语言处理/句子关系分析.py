import re
import os
import pandas as pd
from torch.utils.data import DataLoader
from torch import nn
from torch import optim
from torch.autograd import Variable
import numpy as np
import torch
import jieba
import random
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt

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
data['RelNO']=[int(i[0])-1 for i in data['RelNO']]
data.index=np.arange(len(data))
data.head()
data.shape

#连接词列表，获取所有的连接词，并对连接词再进行细切，最后去重
Connective_list=[]
for i in range(len(data)):
    words = data.Connective[i].split(";")
    for word in words:
        word=jieba.cut(word)
        for i in word:
            if not re.match('[0-9a-zA-Z０１２３４５６７９ｂｔｕ]+',i):
                Connective_list.append(i)
Connective_list=list(set(Connective_list))

#构建词汇矩阵
new_data=[]
for i in range(len(data)):
    this_list=np.zeros(len(Connective_list))
    word_list=data.Connective[i].split(";")
    for word in word_list:
        word = jieba.cut(word)
        for j in word:
            if j in Connective_list:
                this_list[Connective_list.index(j)]+=1
    this_list=np.array(this_list,dtype='float32')
    this_list=torch.from_numpy(this_list)
    new_data.append([this_list,data.RelNO[i]])

#按8：2划分训练集和测试集
random.seed(1234)
test_index=random.sample(range(len(new_data)),int(len(new_data)*0.2))
train_index=list(set(range(len(new_data))).difference(set(test_index)))
test_data=[new_data[i] for i in test_index]
train_data=[new_data[i] for i in train_index]

#定义超参数
batch_size=64
learning_rate=0.01
num_epoches=50

#加载数据集,shuffle=True表示在每个epoch都会对数据进行打乱
train_loader=DataLoader(train_data,batch_size=batch_size,shuffle=True)
test_loader=DataLoader(test_data,batch_size=batch_size,shuffle=False)


#定义两层全连接神经网络
class Batch_Net(nn.Module):
    def __init__(self,in_dim,n_hidden_1,out_dim):
        super(Batch_Net,self).__init__()
        #Sequential是对各个操作进行组合
        self.layer1=nn.Sequential(nn.Linear(in_dim,n_hidden_1),nn.ReLU(True))
        self.layer2=nn.Sequential(nn.Linear(n_hidden_1,out_dim))
    def forward(self, x):
        x=self.layer1(x)
        x=self.layer2(x)
        return x

model=Batch_Net(len(Connective_list),300,4).cuda()

#定义损失函数和优化函数
criterion=nn.CrossEntropyLoss()
optimizer=optim.SGD(model.parameters(),lr=learning_rate,momentum=0.9)

#进行迭代
train_losses=[]
train_acces=[]
test_losses=[]
test_acces=[]
for epoch in range(num_epoches):
    train_loss=0
    train_acc=0
    for im,label in train_loader:
        im=Variable(im).cuda()
        label=Variable(label).cuda()
        #前向传播
        out=model(im)
        loss=criterion(out,label)
        #反向传播
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        #计算训练集损失值和准确率
        train_loss+=loss.data[0]
        _,pred=out.max(1)
        train_acc+=(pred==label).sum().data[0]/im.shape[0]
    train_losses.append(train_loss/len(train_loader))
    train_acces.append(train_acc/len(train_loader))
    #计算测试集的准确率
    model.eval()
    test_loss=0
    test_acc=0
    for im,label in test_loader:
        im=Variable(im).cuda()
        label=Variable(label).cuda()
        out=model(im)
        loss=criterion(out,label)
        test_loss+=loss.data[0]
        _,pred=out.max(1)
        test_acc+=(pred==label).sum().data[0]/im.shape[0]
    test_losses.append(test_loss/len(test_loader))
    test_acces.append(test_acc/len(test_loader))
    print('epoch:%d,train_loss:%.6f,train_acc:%.6f,test_loss:%.6f,test_acc:%.6f' % (
        epoch,train_loss/len(train_loader),train_acc/len(train_loader),test_loss/len(test_loader),test_acc/len(test_loader)
    ))

#绘制损失函数和准确率曲线
fig=plt.figure()
ax=fig.add_subplot(2,1,1)
ax.plot(range(50),train_losses,'r',label='train_loss')
ax.plot(range(50),test_losses,'b',label='test_loss')
plt.legend(loc='best')
ax=fig.add_subplot(2,1,2)
ax.plot(range(50),train_acces,'r',label='train_acc')
ax.plot(range(50),test_acces,'b',label='test_acc')
plt.legend(loc='best')

#计算混淆矩阵
model.eval()
#训练集混淆矩阵
train_pred=[]
train_y=[]
for im,label in train_data:
    im=Variable(im).cuda()
    out=model(im)
    _,predict=out.max(0)
    train_pred.append(predict.data[0])
    train_y.append(label)
confusion_matrix(train_y,train_pred)
np.sum(np.diag(confusion_matrix(train_y,train_pred)))/len(train_data)
#测试集混淆矩阵
test_pred=[]
test_y=[]
for im,label in test_data:
    im=Variable(im).cuda()
    out=model(im)
    _,predict=out.max(0)
    test_pred.append(predict.data[0])
    test_y.append(label)
confusion_matrix(test_y,test_pred)
np.sum(np.diag(confusion_matrix(test_y,test_pred)))/len(test_data)