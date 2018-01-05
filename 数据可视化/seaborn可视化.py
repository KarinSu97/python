import seaborn as sns
#官网API:http://seaborn.pydata.org/api.html

#热力图
import numpy as np
data=np.random.rand(10,12)
sns.set()  #初始化画板
sns.heatmap(data)   #热力图

#散点图
data=sns.load_dataset('tips')
sns.lmplot(x='total_bill',y='tip',data=data)

#分组图
import matplotlib.pyplot as plt
data=sns.load_dataset('tips')
#分组直方图
g=sns.FacetGrid(data,row='smoker',col='sex')
g=g.map(plt.hist,'total_bill')
#分组散点图
g=sns.FacetGrid(data,row='smoker',col='sex')
g=g.map(plt.scatter,'total_bill','tip')
