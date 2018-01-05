from numpy import *
import operator
from os import listdir

#定义knn函数
def KNN(k,test_data,train_data,labels):
    train_data_nrow=train_data.shape[0]
    test_data=tile(test_data,(train_data_nrow,1))
    diff=test_data-train_data
    sq_diff=diff**2
    sum_sq_diff=sum(sq_diff,axis=1)
    distance=sqrt(sum_sq_diff)
    sort_distance=distance.argsort()
    count={}
    for i in range(0,k):
        vote=labels[sort_distance[i]]
        count[vote]=count.get(vote,0)+1
    sort_count=sorted(count.items(),key=operator.itemgetter(1),reverse=True)   #对标签出现的次数进行排序
    return sort_count[0][0]

#将像素矩阵转化为数组形式
def DataToArray(filename):
    arr=[]
    fh=open(filename,"r")
    for line in fh.readlines():
        for i in line:
            if i!="\n":
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

#测试数据
def Test_testdata(traindata_path,testdata_path,k):
    train_data,train_labels=Load_data(traindata_path)
    test_data,test_labels=Load_data(testdata_path)
    for i in range(len(test_data)):
        pred=KNN(k,test_data[i,:],train_data,train_labels)
        print("预测值："+pred+"，真实值："+test_labels[i])

traindata_path='C:/Users/T/Desktop/python视频/traindata/'
testdata_path='C:/Users/T/Desktop/python视频/testdata/'
k=10
Test_testdata(traindata_path,testdata_path,k)