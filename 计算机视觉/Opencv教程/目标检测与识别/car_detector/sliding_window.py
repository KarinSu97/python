'''滑动窗口函数'''
import numpy as np
def sliding_window(image,stepSize,windowSize):
    for y in np.arange(0,image.shape[0],stepSize):
        for x in np.arange(0,image.shape[1],stepSize):
            yield (x,y,image[y:y+windowSize[1],x:x+windowSize[0]])

# import cv2
# img = cv2.imread('C:\\Users\\T\\Downloads\\23.jpg',0)
# for (x,y,roi) in sliding_window(img,20,(100,40)):
#     print(x)
