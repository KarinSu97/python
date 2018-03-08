import cv2
import cv2.xfeatures2d
import numpy as np

#训练样本路径
datapath='C:/Users/T/Downloads/TrainImages'
#定义文件路径函数
def path(cls,i):
    return '%s/%s%d.pgm' % (datapath,cls,i)

pos,neg='pos-','neg-'

#定义两个SIFT对象，一个用于用于获取关键点，一个用于提取特征
detect=cv2.xfeatures2d.SIFT_create()
extract=cv2.xfeatures2d.SIFT_create()

#使用FLANN算法作为特征匹配
flann_params=dict(algorithm=1,trees=5)
flann=cv2.FlannBasedMatcher(flann_params,{})

#创建BOW训练器，指定簇数为40
bow_kmeans_trainer=cv2.BOWKMeansTrainer(40)

#初始化BOW提取器,视觉词汇作为输入
extract_bow=cv2.BOWImgDescriptorExtractor(extract,flann)

#定义SIFT特征提取函数
def extract_sift(fn):
    im=cv2.imread(fn,0)
    return extract.compute(im,detect.detect(im))[1]

#从每个类读取8张图像训练bow训练器
for i in range(400):
    try:
        bow_kmeans_trainer.add(extract_sift(path(pos,i)))
        bow_kmeans_trainer.add(extract_sift(path(neg,i)))
    except:
        continue

#为bow提取器指定词汇，以便可以从图像中提取描述符
vocabulary=bow_kmeans_trainer.cluster()
extract_bow.setVocabulary(vocabulary)

#定义bow提取器描述符返回函数
def bow_features(fn):
    im=cv2.imread(fn,0)
    return extract_bow.compute(im,detect.detect(im))

#构建分类模型训练集,这里读取uiuc汽车数据集的前400张
traindata,trainlabels=[],[]
for i in range(400):
    try:
        traindata.extend(bow_features(path(pos,i)))
        trainlabels.append(1)
        traindata.extend(bow_features(path(neg,i)))
        trainlabels.append(-1)
    except:
        continue

#创建svm模型
svm=cv2.ml.SVM_create()
svm.setType(cv2.ml.SVM_C_SVC)
svm.setGamma(1)
svm.setC(35)
svm.setKernel(cv2.ml.SVM_RBF)
svm.train(np.array(traindata),cv2.ml.ROW_SAMPLE,np.array(trainlabels))

#定义预测模型
def predict(fn):
    img=cv2.imread(fn)
    f=bow_features(fn)
    p=svm.predict(f)
    print(p[1][0][0])
    if p[1][0][0]==1.0:
        cv2.putText(img,'Car detected',(10,30),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2,cv2.LINE_AA)
    else:
        cv2.putText(img, 'Car not detected', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.imshow('img',img)
    cv2.waitKey()

#进行预测
car_img='C:\\Users\\T\\Downloads\\21.jpg'
predict(car_img)
not_car_img='C:\\Users\\T\\Downloads\\13.jpg'
predict(not_car_img)
