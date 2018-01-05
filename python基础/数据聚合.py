import numpy as np
import pandas as pd
from pandas import DataFrame

#分组计算平均值
df = DataFrame({'key1' : ['a', 'a', 'b', 'b', 'a'],
                'key2' : ['one', 'two', 'one', 'two', 'one'],
                'data1' : np.random.randn(5),
                'data2' : np.random.randn(5)})
grouped = df['data1'].groupby(df['key1'])
grouped
grouped.mean()
means = df['data1'].groupby([df['key1'], df['key2']]).mean()
means
means.unstack()

df.groupby('key1').mean()   #所有数据按照key1进行分组计算平均值
df.groupby(['key1', 'key2']).mean()

#分组计数
df.groupby(['key1', 'key2']).size()

#通过字典或series进行分组
people = DataFrame(np.random.randn(5, 5),
                   columns=['a', 'b', 'c', 'd', 'e'],
                   index=['Joe', 'Steve', 'Wes', 'Jim', 'Travis'])
people.ix[2:3, ['b', 'c']] = np.nan # Add a few NA values
people
mapping = {'a': 'red', 'b': 'red', 'c': 'blue',
           'd': 'blue', 'e': 'red', 'f' : 'orange'}
by_column = people.groupby(mapping, axis=1)
by_column.sum()
map_series = pd.Series(mapping)
map_series
people.groupby(map_series, axis=1).count()

#通过索引进行分组
columns = pd.MultiIndex.from_arrays([['US', 'US', 'US', 'JP', 'JP'],
                                    [1, 3, 5, 1, 3]], names=['cty', 'tenor'])
hier_df = DataFrame(np.random.randn(4, 5), columns=columns)
hier_df
hier_df.groupby(level='cty', axis=1).count()

#分组求分位数
grouped = df.groupby('key1')
grouped['data1'].quantile(0.9)

#自定义函数分组计算
def peak_to_peak(arr):
    return arr.max() - arr.min()
grouped.agg(peak_to_peak)

#面向列的多函数应用
from seaborn import load_dataset
tips=load_dataset('tips')
tips['tip_pct'] = tips['tip'] / tips['total_bill']
tips[:6]
grouped = tips.groupby(['sex', 'smoker'])
grouped_pct = grouped['tip_pct']
grouped_pct.agg('mean')
grouped_pct.agg(['mean', 'std', peak_to_peak])
grouped_pct.agg([('foo', 'mean'), ('bar', np.std)])   #给计算后的列进行重命名
functions = ['count', 'mean', 'max']
result = grouped['tip_pct', 'total_bill'].agg(functions)
result
result['tip_pct']
ftuples = [('Durchschnitt', 'mean'), ('Abweichung', np.var)]
grouped['tip_pct', 'total_bill'].agg(ftuples)
grouped.agg({'tip' : np.max, 'size' : 'sum'})
grouped.agg({'tip_pct' : ['min', 'max', 'mean', 'std'],
             'size' : 'sum'})

#给变量名称添加前缀
k1_means = df.groupby('key1').mean().add_prefix('mean_')
k1_means

#apply方法
# ### apply方法
def top(df, n=5, column='tip_pct'):
    return df.sort_index(by=column)[-n:]
top(tips, n=6)
tips.groupby('smoker').apply(top)
tips.groupby(['smoker', 'day']).apply(top, n=1, column='total_bill')
#禁止分组键
tips.groupby('smoker', group_keys=False).apply(top)

#分组加权平均数
df = DataFrame({'category': ['a', 'a', 'a', 'a', 'b', 'b', 'b', 'b'],
                'data': np.random.randn(8),
                'weights': np.random.rand(8)})
df
grouped = df.groupby('category')
get_wavg = lambda g: np.average(g['data'], weights=g['weights'])
grouped.apply(get_wavg)

#透视表
tips.pivot_table(index=['sex', 'smoker'])
tips.pivot_table(['tip_pct', 'size'], index=['sex', 'day'],
                 columns='smoker')
tips.pivot_table(['tip_pct', 'size'], index=['sex', 'day'],
                 columns='smoker', margins=True)
tips.pivot_table('tip_pct', index=['sex', 'smoker'], columns='day',
                 aggfunc=len, margins=True)
tips.pivot_table('size', index=['time', 'sex', 'smoker'],
                 columns='day', aggfunc='sum', fill_value=0)