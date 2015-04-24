__author__ = 'Administrator'
# -*- coding:utf-8 -*-

from collections import deque

import numpy as np
import matplotlib.pyplot as plt

last_label_q = deque()

def choice_ans(in_arr):
    #不管怎样先求平均值
    avg = np.average(in_arr)
    #print avg
    in_arr_tmp = np.abs(in_arr-avg)
    in_arr_tmp = np.argsort(in_arr_tmp)
    #print in_arr_tmp
    choice_num = 5
    new_avg = 0
    for i in range(len(in_arr_tmp)):
        if in_arr_tmp[i] < 6:
            new_avg+=in_arr[i] /6.0
    the_ans = new_avg

    while len(last_label_q) > 5:
        last_label_q.popleft()

    if len(last_label_q) < 5:
        last_label_q.append(the_ans)
    elif the_ans != last_label_q.__getitem__(-1):#len(last_label_q)-1]:
        last_label_q.append(the_ans)
        #print last_label_q




    return the_ans





if __name__ == '__main__':
    in_arr_tmp = np.loadtxt(str('label_save/'+str(1)+'out_nnr'))
    out_arr_tmp = np.loadtxt(str('label_save/'+str(1)+'pose_nnr'))
    #读入数据集，然后训练
    for i in range(0,6):
        in_arr = np.loadtxt(str('label_save/'+str(i)+'out'))
        out_arr = np.loadtxt(str('label_save/'+str(i)+'pose'))
        err = np.zeros([len(in_arr[:,1])])
        full_right = 0
        for j in range(len(in_arr[:,1])):
            out_ans = choice_ans(in_arr[j,:])
            err[j] = abs(out_arr[j] - out_ans)
            if(err[j]<4):
                full_right+=1
        print 'acc:', full_right / 1.0/len(err)

        plt.figure(i)
        plt.plot(err)
        plt.grid()
    plt.show()






