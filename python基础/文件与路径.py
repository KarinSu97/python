#文件读写
#方式一:当出现编码问题或者是图片、视频时，则采用二进制读写，然后再使用decode进行编码即可
f=open('C:\\Users\\T\\Desktop\\1.txt','rb')
for line in f.readlines():
    print(line.decode('utf-8'))
f.close()   #最后要对文件进行关闭

#方式二：使用with，自带close
with open('C:\\Users\\T\\Desktop\\1.txt','rb') as f:
    for line in f.readlines():
        print(line.decode('utf-8'))

#判断文件是否关闭
f.closed

#判断文件的访问模式
f.mode

#文件的名字
f.name

#查看环境变量
import os
os.environ

#查看当前路径
os.path.abspath(".")

#查看路径
import sys
print(sys.path)
sys.path.append('路径')   #添加路径，之后python就可以自动识别这个路径下的模块

#新建文件夹
os.mkdir('C:/Users/T/Desktop/1')

#删除文件夹
os.rmdir('C:/Users/T/Desktop/1')

#删除文件
os.remove('1.txt')

#合并路径
os.path.join('C:/Users/T/Desktop/','1')

#分割路径
os.path.split('C:/Users/T/Desktop/1')

#获取文件的拓展名
os.path.splitext('C:/Users/T/Desktop/1.txt')

#文件重命名
os.rename('C:/Users/T/Desktop/1.txt','C:/Users/T/Desktop/2.txt')

#复制文件
import shutil
shutil.copyfile('C:/Users/T/Desktop/2.txt','C:/Users/T/Desktop/3.txt')