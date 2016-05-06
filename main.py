#coding=utf-8
import gpxpy
import gpxpy.gpx
from core_point import get_Eps,getCore_Points
from models import CorePoint
import os
from time_filter import time_filter
from cut_line import cutline


#最终输出文件
directory_out = os.path.join('data/data_output', 'out.gpx')
gpx_file1 = open(directory_out, "w")  # 打开文件，进行写操作
gpx1 = gpxpy.gpx.GPX()  # 变量gpx1为GPX类型



def process(file):
    num = 32  # 定义读取的文件数量
    for i in range(num):
        file = 'CAStd_116.3714132_39.8774446_116.4615850_39.9267762_0_0_p' + str(i + 1) + '.gpx'


num=32#定义读取的文件数量
for i in range(num):
    file = 'CAStd_116.3714132_39.8774446_116.4615850_39.9267762_0_0_p'+str(i+1)+'.gpx'
    #从gpxdata中读取数据，过滤没有time属性的数据,输出到data_havetime文件夹中
    time_filter(file)
    #从data_havetime文件夹中读取数据，截断不合法的trk，输出到data_cutline文件夹中
    cutline(file)
    #从data_cutline文件夹中读取数据，计算出corepoints。输出到data_output文件夹中
    directory_in = os.path.join('data/data_cutline', file)
    #
    gpx_file = open(directory_in, 'r+')
    gpx = gpxpy.parse(gpx_file)
    #
    gpx_file.close()
    for track in gpx.tracks:
        new_trk = gpxpy.gpx.GPXTrack()  # 遍历trk的同时，建立new_trk
        gpx1.tracks.append(new_trk)
        for segment in track.segments:
            CorePoint.currentSegment = segment
            print('points :%d' % len(segment.points))
            eps = get_Eps(segment)
            print('eps:%f' % eps)

            if eps:
                # 如果eps有效，则算出该segment的corepoints
                # core_points是一个deque
                core_points = getCore_Points(eps, segment)
                for core_point in core_points:
                    new_seg = gpxpy.gpx.GPXTrackSegment()
                    new_trk.segments.append(new_seg)
                    print(core_point)
                    for i in range(core_point.index - core_point.left, core_point.index + core_point.right + 1):
                        new_seg.points.append(segment.points[i])
#
gpx_file1.write(gpx1.to_xml())  # 输出到gpx1中








