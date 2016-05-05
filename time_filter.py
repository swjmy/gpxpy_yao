import os
import gpxpy

"""
file 是string类型参数，表示需要读入的数据文件,路径是确定的，不能改变
"""

def time_filter(file):
    directory_in = os.path.join('data/gpxdata',file)
    directory_out = os.path.join('data/data_havetime',file)

    #读入数据文件
    gpx_file = open(directory_in, 'r+')
    gpx = gpxpy.parse(gpx_file)

    #输出路径
    gpx_file1 = open(directory_out, "w")  # 打开文件，进行写操作
    gpx1 = gpxpy.gpx.GPX()

    i_trk = 0
    i_nt = 0  # 没有时间属性的segment的个数
    for track in gpx.tracks:
        i_trk += 1
        i_seg = 0
        new_trk = gpxpy.gpx.GPXTrack()  # 遍历trk的同时，建立new_trk
        for segment in track.segments:
            i_seg += 1
            i_p = 0
            new_seg = gpxpy.gpx.GPXTrackSegment()  # 遍历segment的同时，建立new_seg
            for point in segment.points:
                i_p += 1
                if point.time != None:  # 遍历point的时候判断是否有time属性，有则存入建好的new_seg中
                    new_seg.points.append(point)
                else:  # 没有则统计seg个数，并跳出“遍历该segment”的进程
                    i_nt += 1
                    break
            if len(new_seg.points) != 0:  # 判断new_seg中point的个数，非0则将new_seg存入建好的new_trk中
                new_trk.segments.append(new_seg)
            else:  # point的个数为0，则跳出该过程，不执行将new_seg存入建好的new_trk中
                break
        if len(new_trk.segments) != 0:  # 同时要判断new_trk中segment的个数，不能存空的trk.
            gpx1.tracks.append(new_trk)
    gpx_file1.write(gpx1.to_xml())  # 输出到gpx1中
