from pandas import DataFrame
import pandas as pd
import numpy as np

###计算指标与哑变量
#将离散变量转化为哑变量形式
df = DataFrame({'key': ['b', 'b', 'a', 'c', 'a', 'b'],
                'data1': range(6)})
pd.get_dummies(df['key'])

dummies = pd.get_dummies(df['key'], prefix='key')   #prefix设定哑变量的名称前缀
df_with_dummy = df[['data1']].join(dummies)
df_with_dummy

#分类不止一个的情况
mnames = ['movie_id', 'title', 'genres']
movies = pd.read_table('d:/data/movies.dat', sep='::', header=None,
                        names=mnames)
movies[:10]

genre_iter = (set(x.split('|')) for x in movies.genres)
genres = sorted(set.union(*genre_iter))

dummies = DataFrame(np.zeros((len(movies), len(genres))), columns=genres)

for i, gen in enumerate(movies.genres):
    dummies.ix[i, gen.split('|')] = 1

movies_windic = movies.join(dummies.add_prefix('Genre_'))
movies_windic.ix[0]
