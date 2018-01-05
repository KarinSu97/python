import pandas as pd
from numpy.random import randn,rand
import numpy as np
import matplotlib.pyplot as plt


#线图
s=pd.Series(randn(10).cumsum(),index=np.arange(0,100,10))
s.plot()

d=pd.DataFrame(randn(10,4).cumsum(0),columns=['A','B','C','D'],index=np.arange(0,100,10))
d.plot()
d.plot(subplots=True)   #将各列单独画在一个图形

#柱形图
fig,axes=plt.subplots(2,1)
s=pd.Series(rand(10).cumsum(),index=list('abcdefghij'))
s.plot(kind='bar',ax=axes[0],color='k',alpha=0.5)
s.plot(kind='barh',ax=axes[1],color='k',alpha=0.5)

d=pd.DataFrame(rand(10,4).cumsum(0),index=list('abcdefghij'),columns=pd.Index(['A','B','C','D'],name='Genus'))
d.plot(kind='bar',alpha=0.5)

#堆积图
d.plot(kind='bar',stacked=True,alpha=0.5)

#直方图
import seaborn
tips=seaborn.load_dataset('tips')
tips['tip_pct']=tips['tip']/tips['total_bill']
tips['tip_pct'].hist()

#密度图
tips['tip_pct'].plot(kind='kde')

#散点图矩阵
from sklearn import datasets
iris=datasets.load_iris()
pd.scatter_matrix(pd.DataFrame(iris.data),diagonal='kde',alpha=0.5)

