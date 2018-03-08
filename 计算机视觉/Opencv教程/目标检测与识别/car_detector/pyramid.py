'''图像金字塔'''
import cv2

#调整图像大小
def resize(img,scaleFactor):
    return cv2.resize(img,
                      (int(img.shape[1]*(1/scaleFactor)),int(img.shape[0]*(1/scaleFactor))),
                      interpolation=cv2.INTER_AREA)

#建立图像金字塔，返回被调整过大小的图像，直到达到指定的最小尺度
def pyramid(image,scale=1.5,minSize=(200,80)):
    yield image
    while True:
        image=resize(image,scale)
        if image.shape[0]<minSize[1] or image.shape[1]<minSize[0]:
            break
        yield image