__author__ = 'Administrator'
# -*- coding:utf-8 -*-

import numpy

import data_transfor
import data_preprocessing
import matplotlib.pyplot as plt


def pose_of_max_rssi(pose, wifi, max_rssi):
    '''
    找到某个ap达到最大值的第一个pose的序号
    :param pose:
    :param wifi:
    :param max_rssi:
    :return:
    '''
    max_rssi_index = numpy.zeros(len(max_rssi))
    for i in range(len(wifi[:, 1])):
        for j in range(len(max_rssi)):
            if max_rssi[j] == wifi[i, j]:
                max_rssi_index[j] = i
    print 'max_rssi_index_len:', len(max_rssi_index)
    pose_array = numpy.zeros([len(max_rssi_index), 2])
    for i in range(len(max_rssi_index)):
        pose_array[i, :] = pose[max_rssi_index[i], :]
    return max_rssi_index, pose_array


def simple_location(pose, wifi, pose_array):
    '''
    根据信号最强的三个ap估计自己的位置
    :param pose: 实际上貌似没用到，以后再改
    :param wifi: 输入wifi的特征数组
    :param pose_array: 有多少个ap就有多少个点，保存的是距这个ap（理想是最近）较近的点
    :return:输出估计的坐标
    '''
    out_pose = numpy.zeros([len(pose[:, 1]), 2])
    max_rssi_tmp = numpy.zeros(2)
    for i in range(len(pose[:, 1])):
        #find max 4 index in the wifi
        max_rssi = numpy.zeros([4, 2])
        for j in range(len(wifi[i, :])):
            if wifi[i, j] > max_rssi[3, 1]:
                max_rssi[3,0] = j
                max_rssi[3,1] = wifi[i,j]
            for k in range(0,2):
                k = 2-k
                if max_rssi[k+1,1] > max_rssi[k,1]:
                    max_rssi_tmp[:] = max_rssi[k,:]
                    max_rssi[k,:] = max_rssi[k+1,:]
                    max_rssi[k+1,:] = max_rssi_tmp[:]
        out_pose[i,0] = pose_array[max_rssi[0,0],0]/4.0 +\
            pose_array[max_rssi[1,0],0]/4.0+\
            pose_array[max_rssi[2,0],0]/4.0+\
            pose_array[max_rssi[3,0],0]/4.0
        out_pose[i,1] = pose_array[max_rssi[0,0],1]/4.0 +\
            pose_array[max_rssi[1,0],1]/4.0+\
            pose_array[max_rssi[2,0],1]/4.0+\
            pose_array[max_rssi[3,0],1]/4.0
    return out_pose


if __name__ == '__main__':
    pose, wifi = data_preprocessing.read_end_data('20153221527end_wifi.txt', '20153221527end_pose.txt')
    pose2, wifi2 = data_preprocessing.read_end_data('20153141218end_wifi.txt', '20153141218end_pose.txt')
    pose3, wifi3 = data_preprocessing.read_end_data('20153141231end_wifi.txt', '20153141231end_pose.txt')
    pose4, wifi4 = data_preprocessing.read_end_data('20153221517end_wifi.txt', '20153221517end_pose.txt')

    max_rssi = data_preprocessing.find_ap_pose(pose, wifi)
    max_rssi2 = data_preprocessing.find_ap_pose(pose2, wifi2)
    max_rssi3 = data_preprocessing.find_ap_pose(pose3, wifi3)
    max_rssi4 = data_preprocessing.find_ap_pose(pose4, wifi4)

    max_rssi_index, pose_array = pose_of_max_rssi(pose, wifi, max_rssi)
    max_rssi_index2, pose_array2 = pose_of_max_rssi(pose2, wifi2, max_rssi2)
    max_rssi_index3, pose_array3 = pose_of_max_rssi(pose3, wifi3, max_rssi3)
    max_rssi_index4, pose_array4 = pose_of_max_rssi(pose4, wifi4, max_rssi4)

    # print pose_array
    plt.figure(1)
    #plt.axis([-50, 200, -50, 200])
    #plt.plot(pose_array[:,0],pose_array[:, 1], 'o')
    plt.plot(pose_array2[:, 0], pose_array2[:, 1], 'o')
    plt.plot(pose_array3[:, 0], pose_array3[:, 1], 'o')
    #plt.plot(pose_array4[:,0],pose_array4[:,1], 'o')
    plt.grid(1)
    plt.figure(2)
    source_pose_array = pose_array/4.0+pose_array2/4.0+pose_array3/4.0+pose_array4/4.0
    #source_pose_array = pose_array3
    out_pose1 = simple_location(pose,wifi,source_pose_array)
    err1 = data_preprocessing.pose_dis(out_pose1,pose)
    plt.plot(err1,'r')
    out_pose2 = simple_location(pose2,wifi2,source_pose_array)
    err2 = data_preprocessing.pose_dis(out_pose2,pose2)
    plt.plot(err2,'b')
    out_pose3 = simple_location(pose3,wifi3,source_pose_array)
    err3 = data_preprocessing.pose_dis(out_pose3,pose3)
    plt.plot(err3,'y')
    out_pose4 = simple_location(pose4,wifi4,source_pose_array)
    err4 = data_preprocessing.pose_dis(out_pose4,pose4)
    plt.plot(err4,'g')
    plt.grid(2)
    plt.figure(3)
    ok_times = 0
    for i in range(len(err1)):
        if err1[i] < 5:
            ok_times+=1
    print 'acc:', ok_times*1.0/len(err1)
    plt.show()
