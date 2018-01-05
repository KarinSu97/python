import matplotlib.pylab as pyl
import matplotlib.pyplot as plt

#折线图
x=[1,2,3,4,5]
y=[3,2,5,7,9]
pyl.plot(x,y)
pyl.show()

#散点图
x=[1,2,3,4,5]
y=[3,2,5,7,9]
pyl.plot(x,y,"o")
pyl.title('points_plot')   #标题
pyl.xlabel('age')   #横坐标标题
pyl.ylabel('wage')   #纵坐标标题
pyl.xlim(0,10)   #设置横坐标范围
pyl.ylim(0,10)   #设置纵坐标范围
pyl.show()

#修改颜色，y:黄色、r:红色、g:绿色、m:品红、k:黑色、w:白色、c:青色、b:蓝色
x=[1,2,3,4,5]
y=[3,2,5,7,9]
pyl.plot(x,y,"ob")
pyl.show()

#修改线条形式，-：直线、--：虚线、-.:-.形式、::细条虚线、
x=[1,2,3,4,5]
y=[3,2,5,7,9]
pyl.plot(x,y,"--")
pyl.show()

#直方图
import numpy as np
data=np.random.random_integers(1,20,100)
sty=np.arange(0,20,2)   #设置上下限和直方图宽度
pyl.hist(data,sty,histtype='stepfilled')
pyl.show()

#子图绘制
pyl.subplot(2,2,1)
x=[1,2,3,4,5]
y=[3,2,5,7,9]
pyl.plot(x,y,"ob")
pyl.subplot(2,2,2)
x=[1,2,3,4,5]
y=[3,2,5,7,9]
pyl.plot(x,y,"-.")
pyl.subplot(2,1,2)
data=np.random.random_integers(1,20,100)
sty=np.arange(0,20,2)   #设置上下限和直方图宽度
pyl.hist(data,sty,histtype='stepfilled')
pyl.show()

#调整subplot周围的间距
from numpy.random import randn
fig, axes = plt.subplots(2, 2, sharex=True, sharey=True)   #sharex和sharey表示子图之间共享坐标轴
for i in range(2):
    for j in range(2):
        axes[i, j].hist(randn(500), bins=50, color='k', alpha=0.5)
plt.subplots_adjust(wspace=0, hspace=0)

#设置图例位置
fig=plt.figure()
ax=fig.add_subplot(1,1,1)
ax.plot(randn(1000).cumsum(),'k--',label='line1')
ax.plot(randn(1000).cumsum(),'g--',label='line2')
ax.plot(randn(1000).cumsum(),'r--',label='line3')
plt.legend(loc='best')

#设置坐标轴刻度和刻度标签
fig=plt.figure()
ax=fig.add_subplot(1,1,1)
ax.plot(randn(1000).cumsum(),'k--')
ax.set_xticks([0,250,500,750,1000])
ax.set_xticklabels(['one','two','three','four','five'],fontsize='small',rotation=30)

#添加注释
from datetime import datetime
import pandas as pd

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

data = pd.read_csv('d:/data/spx.csv', index_col=0, parse_dates=True)
spx = data['SPX']

spx.plot(ax=ax, style='k-')

crisis_data = [
    (datetime(2007, 10, 11), 'Peak of bull market'),
    (datetime(2008, 3, 12), 'Bear Stearns Fails'),
    (datetime(2008, 9, 15), 'Lehman Bankruptcy')
]

for date, label in crisis_data:
    ax.annotate(label, xy=(date, spx.asof(date) + 50),
                xytext=(date, spx.asof(date) + 200),
                arrowprops=dict(facecolor='black'),
                horizontalalignment='left', verticalalignment='top')

#图片保存，dpi设置分辨率，bbox_inches设置空白边的颜色
fig.savefig('C:\\Users\\T\\Desktop\\python视频\\image.png',dpi=400,bbox_inches='tight')

#饼图
plt.figure(1,figsize=(8,8))
plt.axes([0.1,0.1,0.8,0.8])   #设置3D角度
labels='Spring','Summer','Autumn','Winter'
values=(15,16,16,28)
explode=[0.1,0.1,0.1,0.1]   #设置各版块距离
plt.pie(values,labels=labels,autopct='%1.1f%%',startangle=67,explode=explode)