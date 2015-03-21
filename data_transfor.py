__author__ = 'steve'
# -*- coding:utf_8 -*-
#

import os
import sys
import numpy
import scipy
import time

import data_preprocessing


def pose_to_label(pose, distance):
    last_i = 0
    label = numpy.zeros(len(pose))
    label_dict = dict()
    label_dict[0] = [pose[0, 0], pose[0, 1]]
    label[0] = 0

    print label[0]
    for i in xrange(len(pose)):
        if (pose[i, 0] - pose[last_i, 0]) * (pose[i, 0] - pose[last_i, 0]) + \
                        (pose[i, 1] - pose[last_i, 1]) * (pose[i, 1] - pose[last_i, 1]) < distance * distance:
            label[i] = label[last_i]
        else:
            label[i] = label[last_i] + 1
            label_dict[label[i]] = [pose[i, 0], pose[i, 1]]
            last_i = i
    print 'lable_in', label
    return label, label_dict


def get_mac_list(wifi_file, blue_file='null'):
    fp = open(wifi_file, 'rb')
    read = fp.readlines()
    fp.close()
    mac_list = list()
    if (os.path.exists(r'mac_list.txt')) == True:
        fp = open('mac_list.txt', 'rb')
        mac_list = fp.readlines()
        fp.close()
    for line in read:
        if (len(line.split(':')) > 4):
            mac_tmp = line.split(' ')
            tmp = mac_tmp[0] + '\n'
            if mac_tmp[0] not in mac_list:
                mac_list.append(mac_tmp[0])
                print 'add mac'
    # mac——list 去重

    fp = open('mac_list.txt', 'w')
    mac_list_new = list()
    for mac in mac_list:
        if mac not in mac_list_new:
            if mac != '':
                mac_list_new.append(mac)
    for mac in mac_list_new:
        fp.write(mac + '\n')
    fp.close()
    if blue_file != 'null':
        f = open(blue_file, 'rb')
        read = f.readlines()
        f.close()
        blist = list()
        for line in read:
            if (len(line.split(':')) > 4):
                blue_tmp = line.split(' ')
                if blue_tmp[0] not in blist:
                    blist.append(blue_tmp[0])
        for mac in blist:
            fp.write((mac + '\n'))
        print blist
        fp.close()
    fp = open('mac_list.txt', 'rb')
    mac_list = fp.readlines()
    fp.close()
    return mac_list


def syn_data(pose_file, wifi_file, pose_out, wifi_out):
    fp = open(wifi_file, 'rb')
    wifi_list = fp.readlines()
    fp.close()

    fp = open(pose_file, 'rb')
    laser_list = fp.readlines()
    fp.close()
    wifiout = open(wifi_out, 'w')
    poseout = open(pose_out, 'w')
    for wifi in wifi_list:
        # print wifi_list.index(wifi), ' in sum of ', len(wifi_list)

        wifi = wifi.split(' ')
        if len(wifi) < 10:
            print wifi
            continue
        for laser in laser_list:
            laser = laser.split(' ')
            if ((wifi[0] < laser[0]) and (wifi[0] > 14444.0)):
                for i in range(1, len(wifi)):
                    wifiout.write((wifi[i] + ' '))
                wifiout.write('\n')
                poseout.write(laser[1] + ' ' + laser[2] + '\n')

                break
    wifiout.close()
    poseout.close()
    return


# 输入wifi文件，和mac——list文件，并且处理
def file_trance(file, year, month, day, hours):
    fp = open(file, 'rb')
    wifi = fp.readlines()
    fp.close()

    if (os.path.exists(r'mac_list.txt')) == True:
        fp = open('mac_list.txt', 'rb')
        mac_list = fp.readlines()
        fp.close()
    fout = open('out_wifi.txt', 'w')
    all_instance = numpy.zeros(len(mac_list) + 1)
    first = True
    print mac_list
    for line in wifi:
        if line[0] == '@':
            continue
        if line[0] == '#':
            if not first:
                for i in range(len(mac_list) + 1):
                    fout.write((str(int(all_instance[i])) + ' '))
            fout.write('\n')
            line = line.split(' ')
            line = line[1]
            line = line.split('-')
            thetime = time.mktime([int(year), int(month), int(day), int(hours), int(line[0]), int(line[1]), 0, 0, 0])
            # print thetime
            thetime = thetime + float(line[2]) / 1000
            #print 'thetime: ' , thetime
            fout.write(str(thetime))
            fout.write(' ')
            first = False
        else:
            line = line.split(' ')
            if str(line[0]) + '\n' in mac_list:
                num = mac_list.index(str(line[0]) + '\n')
                all_instance[num] = line[1]
            if str(line[0]) in mac_list:
                num = mac_list.index(str(line[0]))
                all_instance[num] = line[1]
    return


def half_data_trans(end_pose, end_wifi):
    fp = open(end_pose)
    pose_list = fp.readlines()
    fp.close()
    fp = open(end_wifi)
    wifi_list = fp.readlines()
    fp.close()

    pose_array = numpy.loadtxt(end_pose)
    wifi_array = numpy.loadtxt(end_wifi)

    save_i = 0

    for i in range(0, len(pose_list)):
        if ((pose_array[i, 0] - 43.0) * (pose_array[i, 0] - 43.0) + (pose_array[i, 1] + 54.0) * (
                    pose_array[i, 1] + 54.0) ) < 2.0:
            save_i = i
            break

    half_pose = numpy.zeros([save_i, 2])
    half_wifi = numpy.zeros([save_i, len(wifi_array[12, :])])

    for i in range(0, save_i):
        half_pose[i, :] = pose_array[i, :]
        half_wifi[i, :] = wifi_array[i, :]

    return half_pose, half_wifi

# file_trance('sourcedata/wifi.txt',year='2015', month='01', day='28', hours='18', minutes='11')
if __name__ == '__main__':
    print '输入文件目录：'
    data_dir = raw_input()
    print '输入laser保存pose 的文件'
    laser_file = raw_input()
    laser_file = data_dir + laser_file
    print '输入保存wifi信号的文件'
    wifi_file = raw_input()
    wifi_file = data_dir + wifi_file
    print '生成mac_list文件中'
    #mac_list = get_mac_list(wifi_file)
    #print 'len mac_list' , len(mac_list)
    print '转变wifi 为 向量形式'
    print 'year'
    year = raw_input()
    print 'month'
    month = raw_input()
    print 'day'
    day = raw_input()
    print 'hours'
    hours = raw_input()
    print 'minutes'
    minutes = raw_input()
    file_trance(wifi_file, year, month, day, hours)
    print '成功，保存转化后的wifi数据到文件 out_wifi.txt'
    print '开始下一步，同步时间轴'
    #syn_data(laser_file, wifi_file='out_wifi.txt', pose_out=data_dir + 'end_pose.txt',
    # wifi_out=data_dir + 'end_wifi.txt')
    data_save_dir = 'data_save/'

    data_preprocessing.sync_timeline(wifi_file='out_wifi.txt', pose_file=laser_file, pose_out=str(
        data_save_dir + year + month + day + hours + minutes + 'end_pose.txt'),
                                     wifi_out=str(
                                         data_save_dir + year + month + day + hours + minutes + 'end_wifi.txt'))
    print '完成数据转化，保存结果到 end_pose.txt 和 end_wifi.txt'
