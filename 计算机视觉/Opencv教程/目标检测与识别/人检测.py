import cv2

#定义检测矩形是否被某个矩形框住的函数
def is_inside(o,i):
    ox,oy,ow,oh=o
    ix,iy,iw,ih=i
    return ox>ix and oy>iy and ox+ow<ix+iw and oy+oh<iy+ih

#定义绘制人函数
def draw_person(image,person):
    x,y,w,h=person
    cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,255),2)

#载入图像
img=cv2.imread('C:\\Users\\T\\Downloads\\19.jpg')

#创建hog对象
hog=cv2.HOGDescriptor()

#使用svm作为分类器
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
found,w=hog.detectMultiScale(img,winStride=(4, 4), padding=(8, 8), scale=1.05)

#筛选矩形框
found_filtered=[]
for ri,r in enumerate(found):
    for qi,q in enumerate(found):
        if ri!=qi and is_inside(r,q):
            break
        else:
            found_filtered.append(r)

#绘制人
for person in found_filtered:
    draw_person(img,person)

#显示图像
cv2.imshow('img',img)
cv2.waitKey()
