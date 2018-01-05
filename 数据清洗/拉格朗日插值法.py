from scipy.interpolate import lagrange
import pandas as pd

#读取数据
file_path='C:/Users/T/Desktop/python视频/catering_sale.xls'
data=pd.read_excel(file_path)

#剔除异常值
data['销量'][(data['销量']<400)|(data['销量']>5000)]=None

#定义插值函数,s为差值的向量，n为插值的位置，k为取前后的数据个数
def ployinterp_column(s,n,k=5):
    y=s[list(range(n-k,n))+list(range(n+1,n+1+k))]   #取数
    y=y[y.notnull()]
    return lagrange(y.index,list(y))(n)   #插值并返回插值结果

#插值
for i in data.columns:
    for j in range(len(data)):
        if(data[i].isnull())[j]:
            data[i][j]=ployinterp_column(data[i],j)

