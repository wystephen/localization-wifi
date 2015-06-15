__author__ = 'Administrator'
# -*- coding:utf-8 -*-

import numpy as np
import scipy as sp

import matplotlib.pyplot as plt

import data_manage


def distance(x1,x2):
    '''
    两个距离都可以用着同一个函数
    :param x1:
    :param x2:
    :return:
    '''
    x1 = (x1-x2)**2.0

    return sum(x1)**0.5


if __name__ == '__main__':
    data = data_manage.data_manage()



    for i in range(1):
        pose, wifi, test_pose, test_wifi = data.get_full_test_data(i,5)

        print 'len pose:',len(pose),'len test:',len(test_pose)
        #用test测试整体的位置
        plt.figure(1)
        if len(test_pose) != len(test_wifi):
            print '长度不相等~'
        wifi_dis = list()
        print np.max(test_wifi),'max wifi'
        for i in range(len(test_wifi)):
            for j in range(i+1,len(test_wifi)-1):
                if 3.1>distance(test_pose[i,:],test_pose[j,:]) > 2.9:
                    wifi_dis.append(distance(test_wifi[i,:],test_wifi[j,:]))
                    j = len(test_wifi)-1
                    break
    wifi_dis = np.asarray(wifi_dis)
    wifi_dis = wifi_dis /1.0/np.average(test_wifi)
    plt.plot(wifi_dis)
    np.savetxt('out_wifi_dis_3f',wifi_dis)
    plt.show()


    
