__author__ = 'steve'
# -*- coding: utf_8 -*-

import sys, os
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
