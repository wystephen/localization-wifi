__author__ = 'steve'
#-*- coding:utf-8 -*-

#

import os
import sys


#先处理wifi数据

fwifi = open('sourcedata/wifi.txt')
wifi_list = fwifi.readlines()
fwifi.close()
fbule = open('sourcedata/bluetooth.txt')
bule_list = fbule.readlines()
fbule.close()

#使用的时间大概是2015 01 28 18点 11分 14秒
wifi_dic =