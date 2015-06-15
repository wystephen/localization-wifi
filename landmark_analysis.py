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

    pose, wifi, test_pose, test_wifi = data.get_full_test_data(1,5)
    last_pose = test_pose[1,:]
    model_dis = 3.0
    out_data = list()

    for i in range(len(test_pose)):
        if distance(test_pose[i,:],last_pose)<model_dis:
            continue
        else:
            dis_list = list()

            for j in range(len(pose)):
                if distance(pose[j,:],last_pose) < model_dis/2.0:
                    dis_list.append(distance(wifi[j,:],test_wifi[i,:]))
                    print wifi[j,:]
            dis_list = np.asarray(dis_list)
            out_data.append([np.average(dis_list),np.std(dis_list)])
            last_pose = test_pose[i,:]
    out_data = np.asarray(out_data)
    plt.figure(1)
    plt.plot(out_data[:,0])
    plt.figure(2)
    plt.plot(out_data[:,1])
    np.savetxt('dis_of_p_4f',out_data)
    plt.show()


