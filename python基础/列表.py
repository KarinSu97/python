#元素位置
li=[1,2,3]
print(li.index(1))

#添加元素
li.append(4)
li

#添加列表
li.extend([5,6,7])
li

#删除元素
del(li[1])   #删除索引为1的元素
li

#生成重复元素
li=[0]*10   #生成含有10个0的列表
li=[[0]*3 for i in range(3)]

#生成器，只有在调用时才真正生成元素
li=(x*x for x in range(5000))
for i in range(5):
    print(next(li))

