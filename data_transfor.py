__author__ = 'steve'
# -*- coding:utf_8 -*-
#

import os
import sys
import numpy, scipy, time

def pose_to_label(pose, distance):
    last_i = 0
    label = numpy.zeros(len(pose))
    label_dict = dict()
    label_dict[0] = [pose[0, 0], pose[0, 1]]
    label[0] = 0
    print label[0]
    for i in xrange(len(pose)):
        if (pose[i,0]-pose[last_i,0])*(pose[i,0]-pose[last_i,0]) + \
                        (pose[i, 1]-pose[last_i, 1])* (pose[i, 1]-pose[last_i, 1])< distance * distance:
            label[i] = label[last_i]

        else:
            label[i] = label[last_i] + 1
            label_dict[label[i]] = [pose[i, 0], pose[i, 1]]
            last_i = i
    print 'lable_in' , label
    return label, label_dict

def get_mac_list(wifi_file,blue_file='null'):
    fp = open(wifi_file,'rb')
    read = fp.readlines()
    fp.close()
    mac_list = list()
    for line in read:
        if (len(line.split(':')) > 4):
            mac_tmp = line.split(' ')
            if mac_tmp[0] not in mac_list:
                mac_list.append(mac_tmp[0])
    fp = open('mac_list.txt', 'w')
    for mac in mac_list:
        fp.write((mac + '\n'))

    if blue_file != 'null':
        f = open(blue_file, 'rb')
        read = f.readlines()
        f.close()
        blist = list()
        for line in read:
            if(len(line.split(':'))>4):
                blue_tmp = line.split(' ')
                if blue_tmp[0] not in blist:
                    blist.append(blue_tmp[0])
        for mac in blist:
            fp.write((mac + '\n'))
        print blist
        fp.close()
    fp = open('mac_list.txt','rb')
    mac_list = fp.readlines()
    fp.close()
    return  mac_list


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
#输入wifi文件，和mac——list文件，并且处理
def file_trance(file, year, month, day, hours, minutes):
    fp = open(file, 'rb')
    wifi = fp.readlines()
    fp.close()
    fp = open('mac_list.txt','rb')
    mac_list = fp.readlines()
    fp.close()
    fout = open('out_wifi.txt', 'w')
    all_instance = numpy.zeros(mac_list.count())
    first = True
    print mac_list
    for line in wifi:
        if line[0] == '@':
            continue
        if line[0] == '#':
            if not first:
                for i in range(mac_list.count()):
                    fout.write((str(int(all_instance[i])) + ' '))
            fout .write('\n')
            line = line.split(' ')
            line = line[1]
            line = line.split('-')
            thetime = time.mktime([int(year), int(month), int(day), int(hours), int(line[0]), int(line[1]), 0, 0, 0])
            print thetime
            thetime = thetime + float(line[2])/1000
            print 'thetime: ' , thetime
            fout.write(str(thetime))
            fout.write(' ')
            first = False
        else:
            line = line.split(' ')
            num = mac_list.index(str(line[0]) + '\n')
            all_instance[num] =line[1]


    return
#file_trance('sourcedata/wifi.txt',year='2015', month='01', day='28', hours='18', minutes='11')