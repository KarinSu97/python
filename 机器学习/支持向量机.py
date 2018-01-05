from sklearn import svm,datasets

#创建类，用于加载数据集并且进行数据集划分
class LoadData:
    #初始化
    def __init__(self,name):
        self.name=name

    #下载数据
    def download_data(self):
        if self.name=='iris':
            self.data=datasets.load_iris()
        elif self.name=='digits':
            self.data=datasets.load_digits()
        else:
            print('please input "iris" or "digits"')

    #生成x,y
    def generate_xy(self):
        self.download_data()
        x=self.data.data
        y=self.data.target
        return x,y

   #将数据分为训练集和测试集
    def split_data(self,ratio):
        x,y=self.generate_xy()
        n=len(x)
        sample_n=int(n*ratio)
        x_train=x[:sample_n]
        y_train=y[:sample_n]
        x_test=x[sample_n:]
        y_test=y[sample_n:]
        return x_train,y_train,x_test,y_test

#加载数据
data=LoadData('iris')
x_train,y_train,x_test,y_test=data.split_data(0.7)

#训练svm模型
f=svm.SVC()
f.fit(x_train,y_train)
pred=f.predict(x_test)

#计算准确率
acu=sum(pred==y_test)/len(y_test)
print(acu)