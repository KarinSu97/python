import cv2

#读取图片
image=cv2.imread('C:\\Users\\T\\Downloads\\5.jpg')

#访问图像的像素点
image[0,0]   #访问第一个像素点
image.item(0,0,1)   #访问指定的像素点对应通道的值
image.itemset((0,0,1),255)   #将(0,0)位置第二个通道的像素值设置为255

#初始化一个名为Image的窗口
cv2.namedWindow('Image')

#显示图片
cv2.imshow('Image',image)
cv2.waitKey(0)

#输出图片
cv2.imwrite('C:\\Users\\T\\Downloads\\5.png',image)

