from pandas import DataFrame
import numpy as np

###重命名索引与标签
data = DataFrame(np.arange(12).reshape((3, 4)),
                 index=['Ohio', 'Colorado', 'New York'],
                 columns=['one', 'two', 'three', 'four'])
data.index.map(str.upper)
data.columns.map(str.upper)
data.index = data.index.map(str.upper)
data

data.rename(index=str.title, columns=str.upper)

#修改指定的索引和标签
data.rename(index={'OHIO': 'INDIANA'},
            columns={'three': 'peekaboo'})

#inplace=True,总是返回DataFrame的引用
_ = data.rename(index={'OHIO': 'INDIANA'}, inplace=True)
data