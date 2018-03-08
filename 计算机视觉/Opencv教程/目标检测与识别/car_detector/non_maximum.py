'''非最大化限制'''
import numpy as np

def non_max_suppression_fast(boxes,overlapThresh):
    #首先判断是否存在矩形框
    if len(boxes)==0:
        return []
    #判断矩形框的数据类型是否是整数，若是则转化为浮点型
    if boxes.dtype.kind=='i':
        boxes=boxes.astype('float')
    #初始化选择列表
    pick=[]
    #获取包围盒的各个部分
    x1=boxes[:,0]
    y1=boxes[:,1]
    x2=boxes[:,2]
    y2=boxes[:,3]
    scores=boxes[:,4]
    #计算各盒子的面积，并根据其分数进行排序
    area=(x2-x1+1)*(y2-y1+1)
    idxs=np.argsort(scores)[::-1]
    #对idxs进行筛选，剔除重叠面积超过阈值的盒子
    while len(idxs)>0:
        last=len(idxs)-1
        i=idxs[last]
        pick.append(i)
        #计算重叠区域
        xx1=np.maximum(x1[i],x1[idxs[:last]])
        yy1 = np.maximum(y1[i], y1[idxs[:last]])
        xx2 = np.minimum(x2[i], x2[idxs[:last]])
        yy2 = np.minimum(y2[i], y2[idxs[:last]])
        w=np.maximum(0,xx2-xx1+1)
        h=np.maximum(0,yy2-yy1+1)
        overlap=(w*h)/area[idxs[:last]]
        idxs=np.delete(idxs,np.concatenate(([last],np.where(overlap>overlapThresh)[0])))
    return boxes[pick].astype('int')



