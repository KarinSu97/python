import cv2
import matplotlib.pyplot as plt

#载入图像
img1=cv2.imread('C:\\Users\\T\\Downloads\\16.jpg',cv2.IMREAD_GRAYSCALE)
img2=cv2.imread('C:\\Users\\T\\Downloads\\17.jpg',cv2.IMREAD_GRAYSCALE)

#创建ORB对象
orb=cv2.ORB_create()
kp1,des1=orb.detectAndCompute(img1,None)
kp2,des2=orb.detectAndCompute(img2,None)

#暴力匹配
bf=cv2.BFMatcher(cv2.NORM_HAMMING,crossCheck=True)
matches=bf.match(des1,des2)
matches=sorted(matches,key=lambda x:x.distance)
img3=cv2.drawMatches(img1,kp1,img2,kp2,matches[:40],img2,flags=2)
plt.imshow(img3)