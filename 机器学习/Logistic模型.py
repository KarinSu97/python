import pandas as pd
from sklearn.linear_model import RandomizedLogisticRegression as RLR
from sklearn.linear_model import LogisticRegression as LR

#读取数据
data=pd.read_csv("C:/Users/T/Desktop/python视频/luqu.csv")
x=data.iloc[:,1:4].as_matrix()
y=data.iloc[:,:1].as_matrix()

#随机Logistic模型，用于筛选变量
f1=RLR()
f1.fit(x,y)
f1.get_support()   #筛选出的变量

#Logistic模型
f2=LR()
f2.fit(x,y)
f2.score(x,y)   #准确率

