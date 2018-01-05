from numpy import *
from os import listdir

class Bayes:
    def __init__(self):
        self.nrow=-1
        self.label_freq=dict()
        self.vector_label=dict()
        self.labels_set=[]
    def fit(self,train_data:list,labels:list):
        if len(train_data)!=len(labels):
            raise ValueError("输入的数据集与标签长度不一致")   #生成错误信息
        #计算各标签的频率
        self.labels_set=set(labels)
        self.nrow=len(train_data)
        for label in self.labels_set:
            self.label_freq[label]=labels.count(label)/self.nrow
        for vector,label in zip(train_data,labels):
            if label not in self.vector_label:
                self.vector_label[label]=[]
            self.vector_label[label].append(vector)
        print("训练结束")
        return self
    def test(self,test_data):
        if self.nrow==-1:
            raise ValueError("还未进行训练")
        result=dict()
        for label in self.labels_set:
            p=1
            vector=array(self.vector_label[label]).T
            for i in range(len(test_data)):
                vector_i=list(vector[i])
                p*=(vector_i.count(test_data[i])/len(vector_i))
            result[label]=self.label_freq[label]*p
        pred=sorted(result,key=lambda x:result[x],reverse=True)[0]
        return pred

# 将像素矩阵转化为数组形式
def DataToArray(filename):
    arr = []
    fh = open(filename, "r")
    for line in fh.readlines():
        for i in line:
            if i != "\n":
                arr.append(int(i))
    return arr

#加载数据集
def Load_data(file_path):
    file_list=listdir(file_path)
    labels=[]
    nrow=len(file_list)
    ncol=len(DataToArray(file_path+file_list[0]))
    data=zeros((nrow,ncol))
    for i in range(nrow):
        arr=DataToArray(file_path+file_list[i])
        data[i,:]=arr
        labels.append(file_list[i].split("_")[0])
    return data,labels

#采用贝叶斯分类对手写数字进行识别
train_data,train_labels=Load_data('C:/Users/T/Desktop/python视频/traindata/')
test_data,test_labels=Load_data('C:/Users/T/Desktop/python视频/testdata/')
m=Bayes()
m.fit(train_data,train_labels)
for i in range(len(test_data)):
    pred=m.test(test_data[i])
    print("预测值："+pred+",真实值:"+test_labels[i])