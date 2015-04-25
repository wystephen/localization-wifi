__author__ = 'Administrator'
# -*- coding:utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import  scipy as sp
from sklearn.neighbors import KNeighborsClassifier

from sklearn import svm

import data_manage
import data_preprocessing
import data_transfor

#这个类基本需要重新写过，思路如下
'''
    n组数据训练n个分类器(svm knn)，
    对每一个结果由n个分类器分类，取众数或者平均数（若取平均数必须剔除误差特别大的结果）.

'''

if __name__ == '__main__':
    data =  data_manage.data_manage()
    type_size = 5# data.how_many()-2
    clf_list = list()
    pose_landmark_label = np.loadtxt('tmp_pose_landmark')
    err_pose = np.zeros([100000,2])
    err_pose_index = 0
    pose_label_list = list()
    out_label_list = list()
    for i in range(0,type_size-1):
        #if i == 4:
        #    continue
        pose, wifi = data.get_data(i)
        #pose, wifi = data_transfor.half_data_trans(pose,wifi)

        if len(wifi) < 100:
            #continue
            pose, wifi = data.get_data(i)
        pose_label = np.zeros(len(wifi))
        #对wifi信号的处理过程
        wifi = data_preprocessing.rss_dis(wifi)
        wifi = data_preprocessing.data_transform(wifi)
        wifi = data_preprocessing.least_d(wifi)
        #把pose 转换成 标签
        for k in range(len(pose[:,1])):
            for  j in range(len(pose_landmark_label)):
                if ((pose_landmark_label[j,0] - pose[k,0])**(2.0) + (pose_landmark_label[j,1]-pose[k,1])**2)**0.5<1.5:
                    pose_label [k] = j


        clf = svm.SVC(kernel = 'linear')
        clf2 = KNeighborsClassifier(n_neighbors=5)

        #保存 pose——label 到 list中方便之后训练。
        pose_label_list.append(pose_label)

        clf.fit(wifi,pose_label)
        clf2.fit(wifi,pose_label)
        clf_list.append(clf)
        clf_list.append(clf2)


    for i in range(0,type_size):

        pose, wifi = data.get_data(i)
        #pose, wifi = data_transfor.half_data_trans(pose,wifi)



        if len(wifi) < 100:
            #continue
            pose, wifi = data.get_data(i)

            #保存输出的pose——label的数组
        out_label_arr = np.zeros([len(pose),len(clf_list)])
        wifi = data_preprocessing.rss_dis(wifi)
        wifi = data_preprocessing.data_transform(wifi)
        wifi = data_preprocessing.least_d(wifi)
        err = np.zeros(len(wifi))
        #针对每一wifi信号处理定位结果
        last_label = -100
        small_err = 0
        big_err = 0
        err_n_times = 0
        for j in range(len(pose)):

            pose_label_tmp_arr = np.zeros(len(clf_list))
            #分别用几个训练器训练出结果
            for k in range(len(clf_list)):
                the_clf = clf_list[k]
                pose_label_tmp_arr[k]=the_clf.predict(wifi[j,:])


            #这里实际上就已经得到了每个训练器训练的结果

            out_label_arr[j,:] = pose_label_tmp_arr[:]
            #pose_label_tmp = pose_label_tmp / 1.0 / len(clf_list)
            #加上更加复杂的规则处理输出的训练结果
            pose_label_tmp = 0
            avg_label = 0
            #求取平均值。
            for k in range(len(pose_label_tmp_arr)):
                avg_label += pose_label_tmp_arr[k]
            avg_label = avg_label / 1.0 / len(pose_label_tmp_arr)
            err_num = 0
            r_avg_label = 0
            #选择偏离平均值比较小的值再求平均值再求结果
            for k in range(len(pose_label_tmp_arr)):
                if abs(pose_label_tmp_arr[k] - avg_label) > 3.0 :
                    err_num += 1
                else:
                    r_avg_label += pose_label_tmp_arr[k]
            #看是否满足至少保留了两组数据
            if err_num < len(pose_label_tmp_arr) - 4 :
                pose_label_tmp = r_avg_label /(len(pose_label_tmp_arr) - err_num)
            else:
                #如果保留的数据很少，就换一种方法求真实值
                #用比较集中的3个的平均值作为输出
                dis_label = np.zeros([len(pose_label_tmp_arr), len(pose_label_tmp_arr)])
                for k in range(len(pose_label_tmp_arr)):
                    for kj in range(len(pose_label_tmp_arr)):
                        dis_label[k,kj] = abs(pose_label_tmp_arr[k] - pose_label_tmp_arr[kj])
                label_dis = np.zeros([len(pose_label_tmp_arr),2])
                for k in range(len(pose_label_tmp_arr)):
                    label_dis[k,0] = pose_label_tmp_arr[k]
                    label_dis[k,1] = sum(dis_label[k,:])
                sorted_index = np.argsort(label_dis,axis=0)
                #这里选择相聚比较近的 3 个求平均值
                for k in range(len(pose_label_tmp_arr)):
                    if sorted_index[k,1] < 5:
                        pose_label_tmp +=pose_label_tmp_arr[k] / 5.0

            #对于输出值进行滤波，如果偏差过大选择不变
            if last_label == -100:
                last_label = pose_label_tmp
                err_n_times = 1
            elif err_n_times < 5 and abs(pose_label_tmp-last_label) < 3.0:

                last_label = pose_label_tmp
            elif abs(pose_label_tmp - last_label) > 3.0 * err_n_times / 10.0:
                err_n_times+=1
                pose_label_tmp = last_label
            elif abs(pose_label_tmp - last_label) <= 3.0 * err_n_times / 10.0:
                last_label =  pose_label_tmp
                err_n_times = 1

            err[j] = ((pose[j,0]-pose_landmark_label[int(pose_label_tmp),0])**(2.0) +
                      (pose[j,1] - pose_landmark_label[int(pose_label_tmp),1])**(2.0))**(0.5)
            if err[j] < 5.0:
                small_err += 1
            if err[j] <7.0:
                big_err +=1
            if err[j] > 10:
                err_pose[err_pose_index,:] = pose[j,:]
                err_pose_index += 1
            #print 'err', err[j]
        out_label_list.append(out_label_arr)
        np.savetxt(str('save_err/'+ str(i) + 'new-err.txt'),err)
        print 'err<5:',small_err,'err<7',big_err,'len_wifi',len(wifi)
        print 'err_acc<5',small_err / 1.0 /len(wifi),'err_acc<7:',big_err/1.0/len(wifi)
        plt.figure(j)
        plt.plot(err,'o')
        #plt.show(j)

    #将所有的 pose_label和 out_label保存。
    for k in range(len(pose_label_list)):
        p_label_tmp = pose_label_list[k]
        o_label_tmp = out_label_list[k]
        np.savetxt(str('label_save/'+str(k)+'pose_nnr'),p_label_tmp)
        np.savetxt(str('label_save/'+str(k)+'out_nnr'),o_label_tmp)



    plt.show()
    np.savetxt(str('save_err/') + 'err_pose.txt',err_pose)





