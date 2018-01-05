#索引
d={'a':1,'b':2,'c':3,4:'a',5:'b'}
d['a']

#删除元素
del[d['a']]
d

#遍历
#方法一：
for key in d:
    print(d[key])

#方法二：
for key,value in d.items():
    print(key,value)