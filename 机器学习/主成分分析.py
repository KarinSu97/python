import pymysql
from sklearn.decomposition import PCA
import pandas as pd

#读取数据
conn=pymysql.connect(host='localhost',user='root',passwd='123456',db='spiders',charset='utf8mb4')
sql='select price,good_rate from jingdong'
data=pd.read_sql(sql,conn)

#主成分分析
pca1=PCA()
pca1.fit(data)
pca1.components_   #特征向量
pca1.explained_variance_ratio_    #贡献率

#降维
pca2=PCA(1)   #这里取1维
pca2.fit(data)
pca2.transform(data)   #降维后的数据