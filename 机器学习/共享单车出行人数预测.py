import pandas as pd
import seaborn as sns
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
from sklearn.linear_model import LassoCV

#定义异常值剔除函数
def outlier(colname,cond1,cond2):
    variable=data1[colname][cond1&cond2]
    #计算上下四分位
    Qu=variable.quantile(0.75)
    Ql=variable.quantile(0.25)
    #计算四分位距
    IQR=Qu-Ql
    #计算上下临界值
    Ou=min(max(variable),Qu+1.5*IQR)
    Ol=max(0,Ql-1.5*IQR)
    return variable[(variable<Ol)|(variable>Ou)].index

def outlier2(colname):
    variable=data1[colname]
    #计算上下四分位
    Qu=variable.quantile(0.75)
    Ql=variable.quantile(0.25)
    #计算四分位距
    IQR=Qu-Ql
    #计算上下临界值
    Ou=min(max(variable),Qu+1.5*IQR)
    Ol=max(0,Ql-1.5*IQR)
    return variable[(variable<Ol)|(variable>Ou)].index

#载入数据集
data1=pd.read_csv('C:\\Users\\T\\Desktop\\共享单车\\day.csv')
data1.head(1)

#数据异常值检测
#剔除季节异常值
g=sns.boxplot(x='season',y='cnt',hue='yr',data=data1)
outlier_index=[]
for i in range(2):
    for j in range(1,5):
        outlier_index.extend(outlier(colname='cnt',cond1=(data1.yr==i),cond2=(data1.season==j)))

#剔除月份异常值
g=sns.boxplot(x='mnth',y='cnt',hue='yr',data=data1)
for i in range(2):
    for j in range(1,13):
        outlier_index.extend(outlier(colname='cnt',cond1=(data1.yr==i),cond2=(data1.mnth==j)))

#剔除星期异常值
g=sns.boxplot(x='weekday',y='cnt',hue='yr',data=data1)
for i in range(2):
    for j in range(7):
        outlier_index.extend(outlier(colname='cnt',cond1=(data1.yr==i),cond2=(data1.weekday==j)))

#剔除假期异常值
g=sns.boxplot(x='holiday',y='cnt',hue='yr',data=data1)
for i in range(2):
    for j in range(2):
        outlier_index.extend(outlier(colname='cnt',cond1=(data1.yr==i),cond2=(data1.holiday==j)))

#剔除天气异常值
g=sns.boxplot(x='weathersit',y='cnt',hue='yr',data=data1)
for i in range(2):
    for j in range(1,4):
        outlier_index.extend(outlier(colname='cnt',cond1=(data1.yr==i),cond2=(data1.weathersit==j)))

#剔除温度异常值
g=sns.boxplot(x='temp',data=data1)
outlier_index.extend(outlier2(colname='temp'))

#剔除体感温度异常值
g=sns.boxplot(x='atemp',data=data1)
outlier_index.extend(outlier2(colname='atemp'))

#剔除湿度异常值
g=sns.boxplot(x='hum',data=data1)
outlier_index.extend(outlier2(colname='hum'))

#剔除风速异常值
g=sns.boxplot(x='windspeed',data=data1)
outlier_index.extend(outlier2(colname='windspeed'))

#将异常点从数据集中剔除,最终剔除73个数据
data2=data1.ix[list(set(data1.index)-set(outlier_index))]

#将分类变量转化为哑变量
data2=pd.concat([data2,pd.get_dummies(data2.season,prefix='season',prefix_sep='_').iloc[:,0:3]],axis=1)
data2=pd.concat([data2,pd.get_dummies(data2.mnth,prefix='mnth',prefix_sep='_').iloc[:,0:11]],axis=1)
data2=pd.concat([data2,pd.get_dummies(data2.weekday,prefix='weekday',prefix_sep='_').iloc[:,0:6]],axis=1)
data2=pd.concat([data2,pd.get_dummies(data2.weathersit,prefix='weathersit',prefix_sep='_').iloc[:,0:3]],axis=1)
data2=data2.drop(['season','mnth','weekday','weathersit'],axis=1)
data2=data2.drop(['instant','dteday','casual','registered'],axis=1)


#利用LASSO进行变量选择
lassocv = LassoCV()
train_x=data2[list(set(data2.columns)-set(['cnt']))]
train_y=data2['cnt']
lassocv.fit(train_x,train_y)
lassocv.alpha_
lassocv.coef_

#保留非0变量，并建立多元回归模型
train_x_new=train_x[list(train_x.columns[lassocv.coef_!=0])]
f1=sm.OLS(train_y,train_x_new).fit()
f1.summary()

pred=f1.predict(train_x_new)
plt.plot(range(len(train_x_new)),train_y)
plt.plot(range(len(train_x_new)),pred)