#ID3决策树
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier as DTC

#加载数据
file_path='C:/Users/T/Desktop/python视频/lesson2.csv'
data=pd.read_csv(file_path,encoding='utf-8')
data=data.iloc[:,1:]

#将数据标签转化为-1和1
data[data==u'是']=1
data[data==u'高']=1
data[data==u'多']=1
data[data!=1]=-1

#切分数据为x和y，记得数据类型要转化为int
x=data.iloc[:,0:4].as_matrix().astype(int)
y=data.iloc[:,4].as_matrix().astype(int)

#建立ID3决策树模型
f=DTC(criterion='entropy')
f.fit(x,y)
f.score(x,y)   #准确率

#决策树可视化，生成的是dot文件，需要用grppgviz进行转化，在cmd中输入“dot -Tpng 文件路径 -o 新的文件路径”即可
from sklearn.tree import export_graphviz
from sklearn.externals.six import StringIO
with open('C:/Users/T/Desktop/python视频/lesson.dot','w') as file:
    export_graphviz(f,feature_names=['combat','num','promotion','datnum'],out_file=file)

#预测
test_data=np.array([[1,1,-1,-1]])
f.predict(test_data)