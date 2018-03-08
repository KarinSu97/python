import cv2

#Canny边缘检测
img=cv2.imread('C:\\Users\\T\\Downloads\\6.jpg',0)
canny_img=cv2.Canny(img,200,300)
canny_img=255-canny_img
cv2.imshow('canny_img',canny_img)
cv2.waitKey()