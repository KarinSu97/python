#使用BP神经网络识别手写数字
from numpy import *
from os import listdir

#将像素矩阵转化为数组形式
def DataToArray(filename):
    arr=[]
    fh=open(filename,"r")
    for line in fh.readlines():
        for i in line:
            if i!="\n":
                arr.append(int(i))
    return arr

#定义加载数据集函数
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

#加载数据集
train_data,train_labels=Load_data('C:/Users/T/Desktop/python视频/traindata/')
test_data,test_labels=Load_data('C:/Users/T/Desktop/python视频/testdata/')

#建立BP神经网络
from keras.models import Sequential   #Sequential用于初始化模型
from keras.layers.core import Dense,Activation   #Dense用于建立层数，Activation用于建立激活函数
from sklearn.preprocessing import LabelEncoder
from keras.utils import np_utils

#将因变量转化为虚拟变量
encoder=LabelEncoder()
encoder_labels=encoder.fit_transform(train_labels)
dummy_labels=np_utils.to_categorical(encoder_labels)

#初始化神经网络
net=Sequential()

#建立神经网络结构
net.add(Dense(output_dim=35,input_dim=1024))   #输入层到隐藏层,input_dim指定输入节点数，ouput_dim表示输出节点数
net.add(Activation('relu'))   #隐藏层的激活函数采用relu函数，一般准确率会高一点
net.add(Dense(output_dim=10,input_dim=35))   #隐藏层到输出层
net.add(Activation('softmax'))   #输出层的激活函数采用softmax函数,若是二分类则采用sigmoid

#编译神经网络
net.compile(loss='categorical_crossentropy',optimizer='adam')   #设置损失函数和求解方法

#训练模型
net.fit(x=train_data,y=dummy_labels,batch_size=200,nb_epoch=1000)   #batch_size表示每次进行训练的样本数，nb_epoch表示训练次数

#预测分类
pred=net.predict_classes(x=test_data).reshape(len(test_data))
test_labels=array(test_labels).astype(int)

#计算准确率
accuracy=sum(pred==test_labels)/len(pred)
print(accuracy)