import pandas as pd

#读取数据
datafile = 'd:/data/normalization_data.xls'
data = pd.read_excel(datafile, header = None)

#最小-最大规范化
(data - data.min())/(data.max() - data.min())

#零-均值规范化
(data - data.mean())/data.std()

#小数定标规范化
data/10**np.ceil(np.log10(data.abs().max()))