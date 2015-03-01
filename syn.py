__author__ = 'steve'
# -*- coding:utf-8 -*-

import os, sys

def syn_data(pose_file ,wifi_file, pose_out, wifi_out)
    fp = open(wifi_file,'rb')
    wifi_list = fp.readlines()
    fp.close()

    fp = open(pose_file,'rb')
    laser_list = fp.readlines()
    fp.close()
    wifiout = open(wifi_out,'w')
    poseout = open(pose_out,'w')
    for wifi in wifi_list:
        print wifi_list.index(wifi), ' summ', len(wifi_list)

        wifi = wifi.split(' ')
        for laser in laser_list:
            laser = laser.split(' ')
            if wifi[0] < laser[0]:
                for i in range(1, len(wifi)-1):
                    wifiout.write((wifi[i] + ' '))
                poseout.write(laser[1] +' ' + laser[2] + '\n')
                wifiout.write('\n')
                break
    wifiout.close()
    poseout.close()
    return
