__author__ = 'steve'
# -*- coding:utf-8 -*-

import os, sys

fp = open('out_wifi.txt','rb')
wifi_list = fp.readlines()
fp.close()

fp = open('sourcedata/laser.txt','rb')
laser_list = fp.readlines()
fp.close()
wifiout = open('wifi_end.txt','w')
poseout = open('pose.txt','w')
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
