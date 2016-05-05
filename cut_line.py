import os
import gpxpy

"""
file 是string类型参数，表示data_havetime文件夹下的某个数据文件
"""
def cutline(file):
    directory_in = os.path.join('data/data_havetime',file)
    directory_out = os.path.join('data/data_cutline',file)

    gpx_file = open(directory_in, 'r+')
    gpx = gpxpy.parse(gpx_file)

    gpx_file1 = open(directory_out, "w")  # 打开文件，进行写操作
    gpx1 = gpxpy.gpx.GPX()  # 变量gpx1为GPX类型

    i_trk = 0
    for track in gpx.tracks:
        i_trk += 1
        i_seg = 0
        new_trk = gpxpy.gpx.GPXTrack()  # 读取gpx同时，构建new_trk，准备存储
        for segment in track.segments:
            i_seg += 1
            pre_point = None  # 初始化空值
            i_p = 0  # 点的量
            i_dis = -1  # distance的量
            total_dis = 0  # 记录量：总距离
            # 第一次循环计算出avg
            for point in segment.points:
                i_p += 1
                i_dis += 1
                if pre_point:
                    newport_ri = (point.latitude, point.longitude)
                    distance = vincenty(pre_point, newport_ri).meters
                    total_dis += distance
                pre_point = (point.latitude, point.longitude)
            if i_p != 0:
                b_value = (total_dis / i_dis) * 3  # 临界值
            else:
                b_value = float('inf')  # seg里面point为空，照样输出.
            # 调用分割函数
            splite(0, b_value, segment, new_trk)
        gpx1.tracks.append(new_trk)  # gpx1文件中添加trk
    gpx_file1.write(gpx1.to_xml())


def splite(start,b_value,seg,new_trk): #遍历segment后调用
    i_p=0
    pre_point=None
    new_seg=gpxpy.gpx.GPXTrackSegment() #new_trk中的变量new_seg
    for point in seg.points[start:]:   #从start开始取到结尾

        i_p+=1
        #记录访问到segment.points中第几个point，从1开始计数
        index = i_p+start
        #判断distance
        if pre_point:
            newport_ri=(point.latitude,point.longitude)
            distance=vincenty(pre_point,newport_ri).meters
            if distance>b_value:
                #出口1：查出不合格的distance
                #完成以上一个new_seg，加入当前new_trk
                new_trk.segments.append(new_seg)
                #继续后面的检查
                splite(index-1,b_value,seg,new_trk)
                break
            else:
                #当前point[i]存入当前new_seg
                new_seg.points.append(seg.points[index-1]) #index从1开始计数
        else:
            #将首个point存入new_seg中
            new_seg.points.append(seg.points[index-1])
        if index == len(seg.points): #segment的最后一个pt
            #出口2：已检查完全部point，将最后一个new_seg加入
            new_trk.segments.append(new_seg)
        pre_point=(point.latitude,point.longitude)
