#coding=utf-8
from models import GetEps,CorePoint
from collections import deque
from geopy.distance import vincenty


def getCore_Points(eps,segment):
    #存放core_points
    core_points = deque([])
    i_next = 0
    for i, p in enumerate(segment.points):
        # i_next用于循环的跳转，如果找到core，则需要跳过neighbors
        # 在找到core的时候，设置新值
        if i > i_next:
            neighbors, i_left, i_right = getNeighbors(i, eps, segment)
            # 判断neighbors是否为空
            if neighbors:
                # 如果是core point,如果是，加入list
                if isCorePoint(neighbors, p):
                    i_next = i + i_right
                    # 新建一个CorePoint对象，将其存储在core_points中
                    core_point = CorePoint(i, i_left, i_right)
                    core_points.append(core_point)
    return core_points

#获取该segment的Eps
def get_Eps(segment):
    geteps = GetEps(segment)  #实例化geteps为GetEps对象
    return geteps.getEpsFunc()  #对象调用类的方法

#获取定点p的线性邻域neighbors:
def getNeighbors(i,eps,segment):
    neighbors = deque([]) #双向链表
    #向前查找
    next = None
    dis = 0.0
    i_left=0
    for point in segment.points[i::-1]:
        if (next):
            dis += vincenty((point.latitude, point.longitude),
                            (next.latitude, next.longitude)).meters
            neighbors.appendleft(next)
            i_left+=1
            if dis > eps:
                i_left+=-1
                break
            elif dis==eps:
                neighbors.appendleft(point)
        next = point
    #向后查找
    pre = None
    dis=0.0
    i_right=0
    for point in segment.points[i::1]:
        if (pre):
            dis += vincenty((pre.latitude,pre.longitude),
                            (point.latitude,point.longitude)).meters
            neighbors.append(point)
            i_right+=1
            if dis > eps:
                i_right+=-1
                neighbors.pop()
                break
        pre = point
    return (neighbors,i_left,i_right)

#计算Tm-Tn来判断是否为core point
def isCorePoint(neighbors,p):
    first = neighbors[0]
    last = neighbors[len(neighbors)-1]
    time1=first.time
    time2=last.time
    time_dv=(time2-time1).seconds
    if time_dv > 90:
        print("时间差值为:{0}").format(time_dv)
        return True
    else:
        return False

'''
#打印neighbor[]
def printNeighbors(neighbors,left,right):
    for i in neighbors:
        print(i)
    print("left={0},right={1}").format(left,right)
'''

