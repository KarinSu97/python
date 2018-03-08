from PIL import Image
from pylab import *

#读取图片,需要转化为灰度图像
im=array(Image.open('C:\\Users\\T\\Downloads\\1.jpg').convert('L'))
figure()
gray()   #不使用颜色
contour(im, origin='image')
