import cv2
import cv2.xfeatures2d

#载入图像
img=cv2.imread('C:\\Users\\T\\Downloads\\12.jpg')
gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

#构建sift对象
sift=cv2.xfeatures2d.SIFT_create()
keypoints,descriptor=sift.detectAndCompute(gray,None)
img=cv2.drawKeypoints(image=img,outImage=img,keypoints=keypoints,flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS,color=(51,163,236))
cv2.imshow('img',img)
cv2.waitKey()
