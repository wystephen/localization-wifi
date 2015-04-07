__author__ = 'Administrator'
# -*- coding:utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import  scipy as sp

from sklearn import svm

import data_manage
import data_preprocessing
import data_transfor

#这个类基本需要重新写过，思路如下
'''
    n组数据训练n个分类器，
    对每一个结果由n个分类器分类，取众数或者平均数（若取平均数必须剔除误差特别大的结果）.

'''

if __name__ == '__main__':
    data =  data_manage.data_manage()
    type_size = data.how_many()-2
    clf_list = list()
    pose_landmark_label = np.loadtxt('tmp_pose_landmark')
    for i in range(0,type_size):
        pose, wifi = data.get_data(i)

        pose_label = np.zeros(len(wifi))
        wifi = data_preprocessing.rss_dis(wifi)
        wifi = data_preprocessing.data_transform(wifi)
        #把pose 转换成 标签
        for k in range(len(pose[:,1])):
            for  j in range(len(pose_landmark_label)):
                if ((pose_landmark_label[j,0] - pose[k,0])**(2.0) + (pose_landmark_label[j,1]-pose[k,1])**2)**0.5<1.5:
                    pose_label [k] = j
        clf = svm.SVC(kernel = 'linear')
        clf.fit(wifi,pose_label)
        clf_list.append(clf)
    for i in range(0,type_size):
        pose, wifi = data.get_data(i)
        wifi = data_preprocessing.rss_dis(wifi)
        wifi = data_preprocessing.data_transform(wifi)
        err = np.zeros(len(wifi))
        for j in range(len(pose)):
            pose_label_tmp_arr = np.zeros(len(clf_list))
            for k in range(len(clf_list)):
                the_clf = clf_list[k]
                pose_label_tmp_arr[k]=the_clf.predict(wifi[j,:])
            #pose_label_tmp = pose_label_tmp / 1.0 / len(clf_list)
            #加上更加复杂的规则处理输出的训练结果
            pose_label_tmp = 0
            avg_label = 0
            for k in range(len(pose_label_tmp_arr)):
                avg_label += pose_label_tmp_arr[k]
            avg_label = avg_label / 1.0 / len(pose_label_tmp_arr)
            err_num = 0
            r_avg_label = 0
            for k in range(len(pose_label_tmp_arr)):
                if abs(pose_label_tmp_arr[k] - avg_label) > 3.0 :
                    err_num += 1
                else:
                    r_avg_label += pose_label_tmp_arr[k]
            if err_num < len(pose_label_tmp_arr) - 2 :
                pose_label_tmp = r_avg_label /(len(pose_label_tmp_arr) - err_num)
            else:
                dis_label = np.zeros([len(pose_label_tmp_arr), len(pose_label_tmp_arr)])
                for k in range(len(pose_label_tmp_arr)):
                    for kj in range(len(pose_label_tmp_arr)):
                        dis_label[k,kj] = abs(pose_label_tmp_arr[k] - pose_label_tmp_arr[kj])
                label_dis = np.zeros([len(pose_label_tmp_arr),2])
                for k in range(len(pose_label_tmp_arr)):
                    label_dis[k,0] = pose_label_tmp_arr[k]
                    label_dis[k,1] = sum(dis_label[k,:])
                sorted_index = np.argsort(label_dis,axis=0)
                for k in range(len(pose_label_tmp_arr)):
                    if sorted_index[k,1] < 5:
                        pose_label_tmp +=pose_label_tmp_arr[k] / 5.0




            err[j] = ((pose[j,0]-pose_landmark_label[int(pose_label_tmp),0])**(2.0) +
                      (pose[j,1] - pose_landmark_label[int(pose_label_tmp),1])**(2.0))**(0.5)
            print 'err', err[j]
        plt.figure(j)
        plt.plot(err)
        #plt.show(j)

    plt.show()




