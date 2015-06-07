__author__ = 'Administrator'
# -*- coding:utf-8 -*-

import os
import re

import numpy
import matplotlib
import sklearn

import data_preprocessing

import D_value_class

#完全独立的一个类，（机器学习数据提取与保存）

class data_manage:
    pattern_all = re.compile('')
    pose = list()
    wifi = list()
    def __init__(self,the_dir='data_save'):
        '''

        :param the_dir:
        :return:
        '''
        self.dir = the_dir
        if os.path.isdir(self.dir):
            print os.listdir(self.dir)
            file_list = os.listdir(self.dir)
            #self.pose = list()
            #self.wifi = list()

           # self.pose.append(numpy.loadtxt('data_save/20153141231end_pose.txt') )
           # self.pose.append(numpy.loadtxt('data_save/20153221517end_pose.txt') )
           # self.pose.append(numpy.loadtxt('data_save/2015325155end_pose.txt')  )
           # self.pose.append(numpy.loadtxt('data_save/20153141218end_pose.txt') )
           # self.pose.append(numpy.loadtxt('data_save/20153221527end_pose.txt') )
           # self.pose.append(numpy.loadtxt('data_save/2015331116end_pose.txt'))
           # self.pose.append(numpy.loadtxt('data_save/20153311044end_pose.txt'))
           # self.pose.append(numpy.loadtxt('data_save/20153311115end_pose.txt'))
           #
           #
           # self.wifi.append(data_preprocessing.pre_process(numpy.loadtxt('data_save/20153141231end_wifi.txt')) )
           # self.wifi.append(data_preprocessing.pre_process(numpy.loadtxt('data_save/20153221517end_wifi.txt')) )
           # self.wifi.append(data_preprocessing.pre_process(numpy.loadtxt('data_save/2015325155end_wifi.txt'))  )
           # self.wifi.append(data_preprocessing.pre_process(numpy.loadtxt('data_save/20153141218end_wifi.txt')) )
           # self.wifi.append(data_preprocessing.pre_process(numpy.loadtxt('data_save/20153221527end_wifi.txt')) )
           # self.wifi.append(data_preprocessing.pre_process(numpy.loadtxt('data_save/2015331116end_wifi.txt')))
           # self.wifi.append(data_preprocessing.pre_process(numpy.loadtxt('data_save/20153311044end_wifi.txt')))
           # self.wifi.append(data_preprocessing.pre_process(numpy.loadtxt('data_save/20153311115end_wifi.txt')))


#           新数据
            self.wifi.append(data_preprocessing.pre_process(numpy.loadtxt('data_save/20154241516n_end_wifi.txt')))
            self.pose.append(numpy.loadtxt('data_save/20154241516n_end_pose.txt'))

            self.wifi.append(data_preprocessing.pre_process(numpy.loadtxt('data_save/2015424151n_end_wifi.txt')))
            self.pose.append(numpy.loadtxt('data_save/2015424151n_end_pose.txt'))

            self.wifi.append(data_preprocessing.pre_process(numpy.loadtxt('data_save/20154241432n_end_wifi.txt')))
            self.pose.append((numpy.loadtxt('data_save/20154241432n_end_pose.txt')))

            self.wifi.append(data_preprocessing.pre_process(numpy.loadtxt('data_save/20154241415n_end_wifi.txt')))
            self.pose.append((numpy.loadtxt('data_save/20154241415n_end_pose.txt')))

            self.wifi.append(data_preprocessing.pre_process(numpy.loadtxt('data_save/20154241346n_end_wifi.txt')))
            self.pose.append((numpy.loadtxt('data_save/20154241346n_end_pose.txt')))

            #以上只包含单组数据，接下来尝试多组数据并行
            #sumt = len(self.wifi)
            #for i in range(sumt):
            #    for j in range(sumt):
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
            #sumt = len(self.wifi)
            #tmp_pose = self.pose[0]
            #tmp_wifi = self.wifi[0]
            #for i in range(sumt-3):
            #
            #    t_pose = self.pose[i]
            #    t_wifi = self.wifi[i]
            #
            #    tmp_pose = numpy.append(tmp_pose,t_pose,axis = 0)
            #    tmp_wifi = numpy.append(tmp_wifi,t_wifi,axis =0)
            #    #print 'wifi:',wifi_sum,'pose_sum:',pose_sum
            #self.pose.append(tmp_pose)
            #self.wifi.append(tmp_wifi)



        else:
            print '目录:',self.dir,'不存在'

    def get_data(self,index):
        '''

        :param index:
        :return:
        '''
        if index > (len(self.wifi) - 1 ):
            print 'index 越界，index 最大为',len(self.wifi)
        wifi, pose =D_value_class.D_value_trans(self.wifi[index],self.pose[index])
        return pose, wifi

    def get_full_test_data(self,index,full_num):
        '''
        这里的index代表不包含的数据集，返回其他所有的数据集
        :param index:
        :return:
        '''
        if index > (len(self.wifi) ):
            print 'index 越界，index 最大为',len(self.wifi)-1
        else:
            sum = len(self.wifi)
            tmp_pose = self.pose[0]
            tmp_wifi = self.wifi[0]
            for i in range(sum):
                if i == index or i > full_num :
                    continue

                else:
                    print 'i:',i,'index',index
                    t_pose = self.pose[i]
                    t_wifi = self.wifi[i]

                    tmp_pose = numpy.append(tmp_pose,t_pose,axis = 0)
                    tmp_wifi = numpy.append(tmp_wifi,t_wifi,axis =0)
                #print 'wifi:',wifi_sum,'pose_sum:',pose_sum
            return tmp_pose,tmp_wifi, self.pose[index], self.wifi[index]


    def how_many(self):
        '''
        :return:
        '''

        return len(self.wifi)
    def test_all_data(self):

        return



if __name__ == '__main__':
    dm = data_manage()
