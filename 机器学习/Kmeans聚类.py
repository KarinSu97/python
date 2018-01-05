import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pylab as pyl
import numpy as np

#加载数据
file_path='C:\\Users\T\\Desktop\\python视频\\luqu.csv'
data=pd.read_csv(file_path)
x=data.iloc[:,1:4].as_matrix()

#Kmeans聚类
kms=KMeans(n_clusters=2,n_init=10)   #设置程序运行10次
y=kms.fit_predict(x)
print(y)

#可视化
d1=data[y==0]
pyl.plot(d1['gre'],d1['gpa'],'*r')
d2=data[y==1]
pyl.plot(d2['gre'],d2['gpa'],'sy')
for i in np.arange(0,len(data)):
    pyl.text(data['gre'][i],data['gpa'][i],str(data['admit'][i]),ha='right')
pyl.show()

#确定最佳k值
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist
K = range(1, 10)
meandistortions = []
for k in K:
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(X)
    #计算每次聚类的平均距离
    meandistortions.append(sum(np.min(cdist(X, kmeans.cluster_centers_, 'euclidean'), axis=1)) / X.shape[0])
plt.plot(K, meandistortions, 'bx-')
plt.xlabel('k')
plt.ylabel('The average degree of distortion')
plt.title('Best k')