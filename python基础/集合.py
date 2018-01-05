#并集
a=set([1,2,3,4,5,6])
b=set([4,5,6,7,8,9])
a|b
a.union(b)

#交集
a&b
a.intersection(b)

#差集
a-b
a.difference(b)

#对称差,相当于异或
a^b
a.symmetric_difference(b)

#添加元素
a.add(7)
a

#添加数组
a.update([1,2,3,8,9])
a

#删除元素
a.remove(1)
a