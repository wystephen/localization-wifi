__author__ = 'steve'
# -*- coding:utf_8 -*-

import numpy

def read_data():
    fp = open('wifi_end.txt','rb')
    wifi_list = fp.readlines()
    fp.close()
    fp= open('pose.txt','rb')
    pose_list = fp.readlines()
    fp.close()

    wifi_array = numpy.zeros([len(wifi_list), 165])
    for line in wifi_list:
        li = line.split(' ')
        for i in range(0,164):
            wifi_array[wifi_list.index(line), i] = int(li[i])/10
    pose_array = numpy.zeros([len(pose_list), 2])
    for line in pose_list:
        li = line.split(' ')
        pose_array[pose_list.index(line),0] = (li[0])
        pose_array[pose_list.index(line),1] = (li[1])
    return wifi_array, pose_array