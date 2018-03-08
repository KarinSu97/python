from PIL import Image
from pylab import *

#读取图片
im=array(Image.open('C:\\Users\\T\\Downloads\\1.jpg'))
imshow(im)

#标注三个地方
x=ginput(3)
x