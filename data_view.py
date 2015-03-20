__author__ = 'Administrator'
# -*- coding:utf-8 -*-

import matplotlib.pyplot as plt
import numpy

import data_transfor

if __name__ == '__main__':
    #pose1 = numpy.loadtxt('data_save/18end_pose.txt')
    pose3 = numpy.loadtxt('data_save/31end_pose.txt')
    fp = open('data_save/18end_pose.txt')
    pose1 = fp.readlines()
    fp.close()
    fp = open('data_save/31end_pose.txt')
    pose2 = fp.readlines()
    fp.close()
    #fp = open('data_save/18end_wifi.txt')
    #wifi1 = fp.readlines()
    #fp.close()
    #fp = open('data_save/31end_wifi.txt')
    #wifi2 = fp.readlines()
    #fp.close()

    wifi1 = numpy.loadtxt('data_save/18end_wifi.txt')
    wifi2 = numpy.loadtxt('data_save/31end_wifi.txt')

    plt.figure(1)

    label, label_dict = data_transfor.pose_to_label(pose3,5)
    last_label_num = 0
    for label_num in label:
        if label_num == last_label_num:
            continue
        else:
            last_label_num = label_num
        #print label_dict[lable_num]
        pose = label_dict[label_num]
        min_index_pose1 = 0
        min_index_pose2 = 0
        min_dis_pose1=1000
        min_dis_pose2 = 1000
        for pose_tmp in pose1:
            pose_tmp_arr = pose_tmp.split(' ')
            dis = ((pose[0] - float(pose_tmp_arr[0]))**(2) +(pose[1] - float(pose_tmp_arr[1]) ) ** (2)) ** (0.5)
            if dis < min_dis_pose1:
                min_dis_pose1 = dis
                min_index_pose1 = pose1.index(pose_tmp)
        for pose_tmp in pose2:
            pose_tmp_arr = pose_tmp.split(' ')
            dis = ((float(pose[0]) - float(pose_tmp_arr[0]))**(2) + (float(pose[1]) - float(pose_tmp_arr[1])) ** (2))** (0.5)
            if dis < min_dis_pose2:
                min_dis_pose2 = dis
                min_index_pose2 = pose2.index(pose_tmp)
        plt.plot(2)
        plt.plot(wifi1[min_index_pose1,:],'o-')
        #plt.subplot(2,2,2)
        plt.plot(wifi2[min_index_pose1,:],'o-')
        plt.show(2)

    plt.show()