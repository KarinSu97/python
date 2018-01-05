#这里的apriori是直接网上下载的代码
from apriori import *
import pandas as pd

#加载数据
file_path='C:/Users/T/Desktop/python视频/lesson_buy.xls'
data=pd.read_excel(file_path,header=None)

#将数据转化为0-1矩阵
change=lambda x:pd.Series(1,index=x[pd.notnull(x)])
map_change=list(map(change,data.as_matrix()))
data1=pd.DataFrame(map_change).fillna(0)

#关联规则
find_rule(data1,0.2,0.5)   #设置支持度为0.2，置信度为0.5