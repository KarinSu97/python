#创建类
class students:
    #在创建类时无需加上括号，如果有参数都放在构造函数里面
    def __init__(self,name,age,sex):
        #这个就是构造函数，其中name,age,sex属于类的变量，一般在建立类时，如果需要在初始化就完成的程序，则都写在构造函数里面
        self.name=name
        self.age=age
        self.__sex=sex   #变量前面加上__则外界无法进行修改

    def info(self,name):   #这里的name属于函数变量
        print(self.name)
        print(self.age)
        print(self.__sex)
        print(name)

student1=students('Lin',25,'male')
student1.info('Chuhai')

#继承
class CollegeStudents(students):
    #此时CollegeStudents继承了students类，具备其参数和方法，也可以增加自身独有的函数或变量
    def score(self,score):
        print(score)

college=CollegeStudents('Lin',25,'male')
college.info('Chuhai')
college.score(97)

#动态添加属性和方法
from types import MethodType
class MyClass(object):
    pass

def set_name(self,name):
    self.name=name

cls=MyClass()
cls.name='Lin'
cls.set_name=MethodType(set_name,cls)
cls.set_name('Huang')
cls.name

#使用__slots__限定只能添加的属性和方法，不过__slots__只能对当前实例起作用，对子类不起作用
class MyClass(object):
    __slots__ = ['name','set_name']   #此事只能添加name和set_name相关的属性或方法

cls=MyClass()
#使用traceback来打印错误信息
import traceback
try:
    cls.age=30
except AttributeError:
    traceback.print_exc()

#类的特殊方法:__str__,可以控制class的输出
class MyClass:
    def __init__(self,name):
        self.name=name

    def __str__(self):
        return "Hello, "+self.name+"!"
print(MyClass('Tom'))

#类的特殊方法：__iter__,实现迭代
class Fib100:
    def __init__(self):
        self._1,self._2=0,1

    def __iter__(self):
        return self

    def __next__(self):
        self._1,self._2=self._2,self._1+self._2
        if self._1>100:
            raise StopIteration
        return self._1

for i in Fib100():
    print(i)

#类的特殊方法：__getitem__可以支持下标操作
class Fib:
    def __getitem__(self, n):
        a,b=1,1
        for i in range(n):
            a,b=b,b+a
        return a

f=Fib()
print(f[5])

#用type动态创建类
def init(self,name):
    self.name=name

def SayHello(self):
    print("Hello,%s!" % self.name)

Hello=type('Hello',(object, ),dict(__init__=init,hello=SayHello))   #这里继承object基类需要写成(object, )的形式

h=Hello('Tom')
h.hello()

#元类，可以控制类的创建过程
class ListMetaClass(type):
    def __new__(cls, name, bases,attrs):
        attrs['add']=lambda self,value:self.append(value)
        return type.__new__(cls, name, bases,attrs)

class MyList(list,metaclass=ListMetaClass):
    pass

m=MyList()
m.add(1)
m.add(2)
m