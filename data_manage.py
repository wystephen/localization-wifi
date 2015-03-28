__author__ = 'Administrator'
# -*- coding:utf-8 -*-

import os
import re

import numpy
import matplotlib
import sklearn

#完全独立的一个类，（机器学习数据提取与保存）

class data_manage:
    pattern_all = re.compile('')
    pose = list()
    wifi = list()
    def __init__(self,the_dir='data_save'):
        self.dir = the_dir
        if os.path.isdir(self.dir):
            print os.listdir(self.dir)
            file_list = os.listdir(self.dir)
            #self.pose = list()
            #self.wifi = list()

            self.pose.append(numpy.loadtxt('data_save/20153141231end_pose.txt') )
            self.pose.append(numpy.loadtxt('data_save/20153221517end_pose.txt') )
            self.pose.append(numpy.loadtxt('data_save/2015325155end_pose.txt')  )
            self.pose.append(numpy.loadtxt('data_save/20153141218end_pose.txt') )
            self.pose.append(numpy.loadtxt('data_save/20153221527end_pose.txt') )


            self.wifi.append(numpy.loadtxt('data_save/20153141231end_wifi.txt') )
            self.wifi.append(numpy.loadtxt('data_save/20153221517end_wifi.txt') )
            self.wifi.append(numpy.loadtxt('data_save/2015325155end_wifi.txt')  )
            self.wifi.append(numpy.loadtxt('data_save/20153141218end_wifi.txt') )
            self.wifi.append(numpy.loadtxt('data_save/20153221527end_wifi.txt') )
            #以上只包含单组数据，接下来尝试多组数据并行
            #sum = len(self.wifi)
            #for i in range(sum):
            #    for j in range(sum):
            #        if j == i:
            #            continue
            #        tmp_pose = self.pose[0]
            #        tmp_wifi = self.wifi[0]
            #        t_pose = self.pose[i]
            #        t_wifi = self.wifi[i]
            #
            #        pose_sum = numpy.append(tmp_pose,t_pose,axis = 0)
            #        wifi_sum = numpy.append(tmp_wifi,t_wifi,axis =0)
            #        #print 'wifi:',wifi_sum,'pose_sum:',pose_sum
            #        self.pose.append(pose_sum)
            #        self.wifi.append(wifi_sum)
            sum = len(self.wifi)
            tmp_pose = self.pose[0]
            tmp_wifi = self.wifi[0]
            for i in range(sum-1):

                t_pose = self.pose[i]
                t_wifi = self.wifi[i]

                tmp_pose = numpy.append(tmp_pose,t_pose,axis = 0)
                tmp_wifi = numpy.append(tmp_wifi,t_wifi,axis =0)
                #print 'wifi:',wifi_sum,'pose_sum:',pose_sum
            self.pose.append(tmp_pose)
            self.wifi.append(tmp_wifi)



        else:
            print '目录:',self.dir,'不存在'

    def get_data(self,index):
        if index > (len(self.wifi) - 1 ):
            print 'index 越界，index 最大为',len(self.wifi)
        return self.pose[index],self.wifi[index]


    def how_many(self):
        '''
        :return:
        '''
        return len(self.wifi)


if __name__ == '__main__':
    dm = data_manage()
