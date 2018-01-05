from pandas import Series
import numpy as np

###替换值
data = Series([1., -999., 2., -999., -1000., 3.])
data

#替换一个值
data.replace(-999, np.nan)

#替换多个值
data.replace([-999, -1000], np.nan)

#将多个值替换为多个对应的值
data.replace([-999, -1000], [np.nan, 0])
data.replace({-999: np.nan, -1000: 0})