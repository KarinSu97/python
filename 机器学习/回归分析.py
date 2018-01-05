from numpy import *
import pandas as pd

#读取数据
data = pd.read_csv('http://www-bcf.usc.edu/~gareth/ISL/Advertising.csv', index_col=0)
data.head()

#相关性分析
import seaborn as sns
sns.pairplot(data,x_vars=['TV', 'radio', 'newspaper'],y_vars='sales',size=7,aspect=0.8,kind='reg')
data.corr()

#划分为训练集和测试集
from sklearn.cross_validation import train_test_split
x=data[['TV', 'radio', 'newspaper']]
y=data['sales']
train_x,test_x,train_y,test_y=train_test_split(x,y,random_state=1)

#线性回归模型
from sklearn.linear_model import LinearRegression
f1=LinearRegression()
f1.fit(train_x,train_y)
f1.intercept_   #常数项
f1.coef_   #回归系数
pred1=f1.predict(test_x)

#模型评估
from sklearn import metrics
metrics.mean_absolute_error(test_y,pred1)   #MAE
metrics.mean_squared_error(test_y,pred1)   #MSE
sqrt(metrics.mean_squared_error(test_y,pred1))   #RMSE