from pandas import DataFrame,Series
import pandas as pd
import numpy as np

###重塑层次化索引
#1
data = DataFrame(np.arange(6).reshape((2, 3)),
                 index=pd.Index(['Ohio', 'Colorado'], name='state'),
                 columns=pd.Index(['one', 'two', 'three'], name='number'))
data

result = data.stack()
result

result.unstack()

result.unstack(0)

result.unstack('state')

#2
s1 = Series([0, 1, 2, 3], index=['a', 'b', 'c', 'd'])
s2 = Series([4, 5, 6], index=['c', 'd', 'e'])
data2 = pd.concat([s1, s2], keys=['one', 'two'])
data2.unstack()

data2.unstack().stack()

data2.unstack().stack(dropna=False)

#3
df = DataFrame({'left': result, 'right': result + 5},
               columns=pd.Index(['left', 'right'], name='side'))
df

df.unstack('state')

df.unstack('state').stack('side')

###长宽格式的转换
#1
data = pd.read_csv('C:\\Users\\T\\Desktop\\python视频\\macrodata.csv')
periods = pd.PeriodIndex(year=data.year, quarter=data.quarter, name='date')
data = DataFrame(data.to_records(),
                 columns=pd.Index(['realint', 'infl', 'unemp'], name='item'),
                 index=periods.to_timestamp('D', 'end'))

ldata = data.stack().reset_index().rename(columns={0: 'value'})
wdata = ldata.pivot('date', 'item', 'value')   #将数据变为宽格式

#2
ldata[:10]

pivoted = ldata.pivot('date', 'item', 'value')
pivoted.head()

ldata['value2'] = np.random.randn(len(ldata))
ldata[:10]

pivoted = ldata.pivot('date', 'item')
pivoted[:5]

pivoted['value'][:5]

unstacked = ldata.set_index(['date', 'item']).unstack('item')
unstacked[:7]