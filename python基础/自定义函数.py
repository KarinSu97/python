#可变参数,在变量前面添加*表示参数是可变的,此时是一个数组，在变量前面添加两个*则表示字典，另外注意可变参数必须在最后
def func(name,*number):
    print(number)

print(func('Lin',1,2,3))

def func(name,**kvs):
    print(name)
    print(kvs)

print(func('Tom',country='China',province='guangdong'))

#*后面的变量在传递参数时必须指定变量名称
def func(a,b,c,*,country,province):
    print(a,b,c)
    print(country,province)

func(1,2,3,country='china',province='guangdong')

#匿名函数,其实就是一个表达式
f=lambda x,y:x+y
f(2,3)

#reduce(func(),l),reduce表示对一个列表或元组进行func操作，其中func必须是一个二元操作，表示对l中的前两个数先进行func操作，
#然后再将其结果与第三个数进行操作，以此类推
from functools import reduce
l=[1,2,3,4,5]
reduce(lambda x,y:x+y,l)
reduce(lambda x,y:x+y,l,10)   #设置初始值10，此时第一个数是10

#map(func,l)函数，表示对l中每个元素执行func操作，返回的函数一个list
l=[1,2,3,4,5]
list(map(lambda x:x**2,l))
#也可对两个list执行操作
l2=[1,2,3,4,5]
list(map(lambda x,y:x+y,l,l2))

#filter函数，对列表或元组进行过滤
l=[1,2,3,4,5,6]
list(filter(lambda x:x % 2==0,l))

#偏函数，就是修改python函数的默认参数设置，然后赋值给另一个变量
import functools
int2=functools.partial(int,base=2)   #int默认base是10，即10进制，这里修改为2则为2进制
int2('100')
