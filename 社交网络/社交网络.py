#官方文档：http://www.cs.rhul.ac.uk/home/tamas/development/igraph/tutorial/tutorial.html
from igraph import *

#构建图
##方式一
g=Graph([(0,1),(0,2),(2,3),(3,4),(4,2),(2,5),(5,0),(6,3),(5,6)])
g
##方式二
data=[(0,1),(0,2),(2,3),(3,4),(4,2),(2,5),(5,0),(6,3),(5,6)]
g=Graph.TupleList(data,directed=True,vertex_name_attr="name")
print(g)

#图的点数和边数
summary(g)

#各点的度数
g.degree()
##显示节点的名字和度数
for i in g.vs:
    print(i['name'],i.degree())

#获取某个点到其他点的最短路径
g.get_all_shortest_paths(0)

#紧密中心性，即点到其他所有点的难易程度，即点与其他所有点的距离平均值的倒数，数值越大，表示越处于中心的位置
ccvs=[]
for p in zip(g.vs,g.closeness()):
    ccvs.append({"name":p[0]["name"],"cc":p[1]})
sorted(ccvs,key=lambda k:k["cc"],reverse=True)

#点介数,即属于最短路径中介点的次数，数值越大，则该点越属于网络中的枢纽
btvs=[]
for p in zip(g.vs,g.betweenness()):
    btvs.append({"name":p[0]["name"],"bt":p[1]})
sorted(btvs,key=lambda k:k['bt'],reverse=True)

#社区发现——GN算法
communities=g.community_edge_betweenness(directed=True)
print(communities)
print(g.vs['name'])

#绘图
g=Graph.Famous('petersen')
plot(g)


'''
===========================
案例：权利的游戏
===========================
'''
import pandas as pd
data=pd.read_csv('C:\\Users\\T\\Desktop\\python视频\\stormofswords.csv')
data=data.as_matrix()
g=Graph.TupleList(data,directed=True,vertex_name_attr="name",weights=True)
print(g)

#节点名字和边权重
name=g.vs["name"]
print(name)
weight=g.es['weight']
print(weight)

#网络的直径，即网络中最长最短路径
g.diameter()
g.get_diameter()
print([name[x] for x in g.get_diameter()])

#最短路径
g.shortest_paths('Bronn','Sandor')
g.get_shortest_paths('Bronn','Sandor')
print([name[x] for x in g.get_shortest_paths('Bronn','Sandor')[0]])

#加权度中心性
for p in g.vs:
    weightDegree=sum([x.degree() for x in p.neighbors()])
    if weightDegree>250:
        print(p["name"],weightDegree)

#紧密中心性，即点到其他所有点的难易程度，即点与其他所有点的距离平均值的倒数，数值越大，表示越处于中心的位置
ccvs=[]
for p in zip(g.vs,g.closeness()):
    ccvs.append({"name":p[0]["name"],"cc":p[1]})
sorted(ccvs,key=lambda k:k["cc"],reverse=True)

#点介数,即属于最短路径中介点的次数，数值越大，则该点越属于网络中的枢纽
btvs=[]
for p in zip(g.vs,g.betweenness()):
    btvs.append({"name":p[0]["name"],"bt":p[1]})
sorted(btvs,key=lambda k:k['bt'],reverse=True)

#社区发现，采用随机游走发现社区
clusters=g.community_walktrap().as_clustering()
nodes=[{"name":node["name"]} for node in g.vs()]
communities={}
for node in nodes:
    idx=g.vs.find(node["name"]).index
    cluster=clusters.membership[idx]
    if cluster not in communities:
        communities[cluster]=[node["name"]]
    else:
        communities[cluster].append(node["name"])
for i,node in communities.items():
    print(i,node)

#画图
g.vs['label']=g.vs['name']   #添加标签
color_dict={0:"blue",1:"red",2:"pink",3:'green',4:"yellow",5:"black",6:"orange"}
g.vs['cluster'] = g.community_walktrap().as_clustering().membership
g.vs['color']=[color_dict[x] for x in g.vs['cluster']]   #设置社区颜色
layout=g.layout('kk')
plot(g,layout=layout)