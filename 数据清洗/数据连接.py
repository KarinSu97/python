from pandas import DataFrame,Series
import pandas as pd
import numpy as np

###dataframe合并
#当有相同的列名时，直接用on指定即可
df1 = DataFrame({'key': ['b', 'b', 'a', 'c', 'a', 'a', 'b'],
                 'data1': range(7)})
df2 = DataFrame({'key': ['a', 'b', 'd'],
                 'data2': range(3)})
df1
df2

pd.merge(df1, df2)
pd.merge(df1, df2, on='key')

#当列名不同时，需要用left_on和right_on分别指定
df3 = DataFrame({'lkey': ['b', 'b', 'a', 'c', 'a', 'a', 'b'],
                 'data1': range(7)})
df4 = DataFrame({'rkey': ['a', 'b', 'd'],
                 'data2': range(3)})
pd.merge(df3, df4, left_on='lkey', right_on='rkey')

pd.merge(df1, df2, how='outer')

#指定连接方式需要用how指定，有内连接、外连接等
df1 = DataFrame({'key': ['b', 'b', 'a', 'c', 'a', 'b'],
                 'data1': range(6)})
df2 = DataFrame({'key': ['a', 'b', 'a', 'b', 'd'],
                 'data2': range(5)})
df1
df2

pd.merge(df1, df2, on='key', how='left')
pd.merge(df1, df2, how='inner')

#当连接的字段不止一个时，用列表指定
left = DataFrame({'key1': ['foo', 'foo', 'bar'],
                  'key2': ['one', 'two', 'one'],
                  'lval': [1, 2, 3]})
right = DataFrame({'key1': ['foo', 'foo', 'bar', 'bar'],
                   'key2': ['one', 'one', 'one', 'two'],
                   'rval': [4, 5, 6, 7]})
pd.merge(left, right, on=['key1', 'key2'], how='outer')

#当存在其他相同的字段时，用suffixes指定连接后的字段名称
pd.merge(left, right, on='key1')

pd.merge(left, right, on='key1', suffixes=('_left', '_right'))


###索引上的合并
#1
left1 = DataFrame({'key': ['a', 'b', 'a', 'a', 'b', 'c'],'value': range(6)})
right1 = DataFrame({'group_val': [3.5, 7]}, index=['a', 'b'])
left1
right1

pd.merge(left1, right1, left_on='key', right_index=True)

pd.merge(left1, right1, left_on='key', right_index=True, how='outer')

#2
lefth = DataFrame({'key1': ['Ohio', 'Ohio', 'Ohio', 'Nevada', 'Nevada'],
                   'key2': [2000, 2001, 2002, 2001, 2002],
                   'data': np.arange(5.)})
righth = DataFrame(np.arange(12).reshape((6, 2)),
                   index=[['Nevada', 'Nevada', 'Ohio', 'Ohio', 'Ohio', 'Ohio'],
                          [2001, 2000, 2000, 2000, 2001, 2002]],
                   columns=['event1', 'event2'])
lefth
righth

pd.merge(lefth, righth, left_on=['key1', 'key2'], right_index=True)

pd.merge(lefth, righth, left_on=['key1', 'key2'],
         right_index=True, how='outer')

left2 = DataFrame([[1., 2.], [3., 4.], [5., 6.]], index=['a', 'c', 'e'],
                 columns=['Ohio', 'Nevada'])
right2 = DataFrame([[7., 8.], [9., 10.], [11., 12.], [13, 14]],
                   index=['b', 'c', 'd', 'e'], columns=['Missouri', 'Alabama'])
left2
right2
pd.merge(left2, right2, how='outer', left_index=True, right_index=True)

#3
left2.join(right2, how='outer')

left1.join(right1, on='key')

#4
another = DataFrame([[7., 8.], [9., 10.], [11., 12.], [16., 17.]],
                    index=['a', 'c', 'e', 'f'], columns=['New York', 'Oregon'])
left2.join([right2, another])

left2.join([right2, another], how='outer')

###轴向连接
#1
arr = np.arange(12).reshape((3, 4))
arr

np.concatenate([arr, arr], axis=1)

#2
s1 = Series([0, 1], index=['a', 'b'])
s2 = Series([2, 3, 4], index=['c', 'd', 'e'])
s3 = Series([5, 6], index=['f', 'g'])

pd.concat([s1, s2, s3])

pd.concat([s1, s2, s3], axis=1)

s4 = pd.concat([s1 * 5, s3])
pd.concat([s1, s4], axis=1)

pd.concat([s1, s4], axis=1, join='inner')

pd.concat([s1, s4], axis=1, join_axes=[['a', 'c', 'b', 'e']])

#3
result = pd.concat([s1, s1, s3], keys=['one', 'two', 'three'])
result

result.unstack()

#4
pd.concat([s1, s2, s3], axis=1, keys=['one', 'two', 'three'])

df1 = DataFrame(np.arange(6).reshape(3, 2), index=['a', 'b', 'c'],
                columns=['one', 'two'])
df2 = DataFrame(5 + np.arange(4).reshape(2, 2), index=['a', 'c'],
                columns=['three', 'four'])

pd.concat([df1, df2], axis=1, keys=['level1', 'level2'])

pd.concat({'level1': df1, 'level2': df2}, axis=1)

pd.concat([df1, df2], axis=1, keys=['level1', 'level2'],
          names=['upper', 'lower'])

#5
df1 = DataFrame(np.random.randn(3, 4), columns=['a', 'b', 'c', 'd'])
df2 = DataFrame(np.random.randn(2, 3), columns=['b', 'd', 'a'])

df1

df2

pd.concat([df1, df2], ignore_index=True)   #不同列数的合并

###合并重叠数据
#1
a = Series([np.nan, 2.5, np.nan, 3.5, 4.5, np.nan],
           index=['f', 'e', 'd', 'c', 'b', 'a'])
b = Series(np.arange(len(a), dtype=np.float64),
           index=['f', 'e', 'd', 'c', 'b', 'a'])
b[-1] = np.nan

a

b

np.where(pd.isnull(a), b, a)

#2
b[:-2].combine_first(a[2:])

#3
df1 = DataFrame({'a': [1., np.nan, 5., np.nan],
                 'b': [np.nan, 2., np.nan, 6.],
                 'c': range(2, 18, 4)})
df2 = DataFrame({'a': [5., 4., np.nan, 3., 7.],
                 'b': [np.nan, 3., 4., 6., 8.]})
df1.combine_first(df2)