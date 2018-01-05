#判断类型
A='abc'
isinstance(A,str)   #判断A是否是字符类型

#获取某个对象的所有属性和方法
dir('abc')

#判断某个对象是否含有某个属性
hasattr('abc','__len__')   #判断字符串abc里面是否含有__len__属性

#获取属性
getattr('abc','__len__')

#设置属性
setattr('abc','__len__',3)

#enumerate,可以同时获取数组或列表的索引和值
l=[1,2,3]
for index,value in enumerate(l):
    print(index,value)