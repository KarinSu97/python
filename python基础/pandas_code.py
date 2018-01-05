import pandas as pd
from pandas import DataFrame

#生成一串数字，并且会自动给数据加上索引,也可以自定义索引
a=pd.Series([1,2,3,4])
b=pd.Series([1,2,3,4],index=['one','two','three','four'])

#通过数组创建数据框
c=pd.DataFrame([[3,2,4,1],[12,1,6,3],[89,76,53,27],[1,2,3,4]])
c
d=pd.DataFrame([[3,2,4,1],[12,1,6,3],[89,76,53,27],[1,2,3,4]],columns=['one','two','three','four'])   #指定列名称
d

#通过字典创建数据框
e=pd.DataFrame({
    'one':4,
    'two':[1,2,3],
    'three':list(str(789))
})
e

#显示前几行
e.head(2)

#显示后几行数据
e.tail(2)

#数据描述
e.describe()

#转置
e.T

#排序
e.sort_values(by='one')

#索引
e.values[0][1]   #第一行第二列

#切片
e.iloc(:,1:4)

#剔除重复数据
data = DataFrame({'k1': ['one'] * 3 + ['two'] * 4,
                  'k2': [1, 1, 2, 3, 3, 4, 4]})
##判断是否出现重复值
data.duplicated()
##删除重复值
data.drop_duplicates()
##只看某一列是否出现重复值
data['v1'] = range(7)
data.drop_duplicates(['k1'])
##保留最后一条记录
data.drop_duplicates(['k1', 'k2'], take_last=True)
