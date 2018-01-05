import pandas as pd
import numpy as np

###离散化与面元划分
#将数据按照指定的区间进行分组
ages = [20, 22, 25, 27, 21, 23, 37, 31, 61, 45, 41, 32]
bins = [18, 25, 35, 60, 100]
cats = pd.cut(ages, bins)
cats
#显示各组的组别和标签
cats.labels
cats.levels
#统计各组的频数
pd.value_counts(cats)
#设置区间的开闭情况
pd.cut(ages, [18, 26, 36, 61, 100], right=False)
#设置分组的标签
group_names = ['Youth', 'YoungAdult', 'MiddleAged', 'Senior']
pd.cut(ages, bins, labels=group_names)
#按照指定的组数进行分组
data = np.random.rand(20)
pd.cut(data, 4, precision=2)
#按照分位点进行分组
data = np.random.randn(1000) # Normally distributed
cats = pd.qcut(data, 4) # Cut into quartiles
cats
pd.value_counts(cats)
pd.qcut(data, [0, 0.1, 0.5, 0.9, 1.])