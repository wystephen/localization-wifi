__author__ = 'steve'
# -*- coding:utf_8 -*-

import os, sys, time, numpy

def file_trance(file, year, month, day, hours, minutes):
    fp = open(file, 'rb')
    wifi = fp.readlines()
    fp.close()
    fp = open('mac_list.txt','rb')
    mac_list = fp.readlines()
    fp.close()
    fout = open('out_wifi.txt', 'w')
    all_instance = numpy.zeros(165)
    first = True
    print mac_list
    for line in wifi:
        if line[0] == '@':
            continue
        if line[0] == '#':
            if not first:
                for i in range(164):
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







file_trance('sourcedata/wifi.txt',year='2015', month='01', day='28', hours='18', minutes='11')