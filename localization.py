__author__ = 'Administrator'
# -*- coding:utf-8 -*-

import numpy as np
import scipy as sp
import matplotlib as plt

import data_manage
import data_preprocessing
import use_max_rssi_localization
import classify_use_test

class localization:
    def __init__(self):
        print '准备完毕'

    def get_err(self,pose,out_pose):
        '''

        :param pose:
        :param out_pose:
        :return:err, small_err, big_err, large_err
        '''
        if len(pose) != len(out_pose):
            print '两个坐标矩阵大小不同'
        else:
            err = np.zeros([len(pose),1])
            small_err = 0
            big_err = 0
            large_err = 0
            for i in range(len(pose)):
                err[i,0] = ((pose[i,0]-out_pose[i,0])**(2.0)+(pose[i,1]-out_pose[i,1])**(2.0))**(0.5)
                if err[i,0] <5:
                    small_err+=1
                elif err[i,0] <8:
                    big_err += 1
                elif err[i,0] <10:
                    large_err +=1
            return err, small_err, big_err, large_err

