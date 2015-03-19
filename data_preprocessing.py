__author__ = 'steve'
# -*- coding:utf-8 -*-


import numpy


def sync_timeline(wifi_file, pose_file, pose_out, wifi_out, is_debuge=False):
    """

    :param wifi_file: wifi文件（包含地址）（已经转化为格式： 时间 mac1（强度） mac2（强度） 。。。）
    :param pose_file: pose文件（包含地址）
    :param pose_out: 去除时间，
    :param wifi_out: 去除时间，和pose对齐。
    :param is_debuge:默认为false,调试参数。
    """
    fp = open(wifi_file, 'rb')
    wifi_list = fp.readlines()
    fp.close()

    fp = open(pose_file, 'rb')
    pose_list = fp.readlines()
    fp.close()

    wifi_out = open(wifi_out, 'w')
    pose_out = open(pose_out, 'w')

    # 获取pose文件中所有时间值的数组
    pose_time_array = numpy.zeros(len(pose_list))
    for pose_data in pose_list:
        pose_data_tmp = pose_data.split(' ')
        pose_time_array[pose_list.index(pose_data)] = pose_data_tmp[0]
    #输出 pose 时间序列的数组
    print 'the pose_time_array:', pose_time_array

    for wifi_data in wifi_list:
        if wifi_data == '\n':
            continue
        wifi_data = wifi_data.split(' ')
        if len(wifi_data) < 4:
            continue
        wifi_time = wifi_data[0]

        print 'wifi_time:', wifi_data
        min_time_diff = 10000
        time_diff_min_index = 0  #设置一个极大的不可能值
        for i in range(0, len(pose_time_array)):
            time_diff = ((float(wifi_time)- (pose_time_array[i]))*1.0)
            if time_diff < 0:
                time_diff = time_diff * (-1.0)
            if time_diff < min_time_diff:
                min_time_diff = time_diff
                time_diff_min_index = i
        #根据得到的序号i分别输出 pose，和wifi
        pose_out_tmp = pose_list[time_diff_min_index]
        pose_out_tmp = pose_out_tmp.split(' ')
        pose_out.write(str(pose_out_tmp[1]) + ' '+ str(pose_out_tmp[2]))
        pose_out.write('\n')
        for i in range(1,len(wifi_data)):
            wifi_out.write(str(wifi_data[i]) + ' ')
        wifi_out.write('\n')

    print '时间轴同步wifi和pose数据成功'
    return