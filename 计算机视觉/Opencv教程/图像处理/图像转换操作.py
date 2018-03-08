import cv2
from matplotlib.pyplot import *

#将图像转化为灰色图像
grayimage=cv2.imread('C:\\Users\\T\\Downloads\\5.jpg',cv2.IMREAD_GRAYSCALE)
cv2.imwrite('C:\\Users\\T\\Downloads\\5.png',grayimage)

#将指定区域替换为另一个区域
image=cv2.imread('C:\\Users\\T\\Downloads\\4.jpg')
imshow(image)
image[0:354,0:480]=image[500:854,0:480]
imshow(image)