__author__ = 'Administrator'
# -*- coding:utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm
from sklearn.cluster import MiniBatchKMeans, KMeans, AffinityPropagation


import classify_use_test
import data_manage
import data_preprocessing
import data_transfor


class multilayer:
    '''
    先分大类，再在大类里面详细分小类进行分类，目前效果一般。
    '''
    def __init__(self,data,label,type_num=12):
        '''
        初始化multilayer这个类，为了符合之前的那个格式。

        :param data: wifi
        :param label: 输入label
        :param type_num:分成多少个大类
        :return:
        '''
        self.K_means_label, self.k_means_clf = self.big_scale_classfier(data, type_num = type_num)
        self.clf = list()
        type_sum = np.zeros([type_num])
        for i in range(len(data[:,1])):
            type_sum[self.k_means_clf.predict(data[i,:])] +=1
        print type_sum
        clf_te = svm.SVC(kernel = 'linear')#, probability = True)
        clf_te.fit(data,label)
        print 'clf_te:', clf_te
        for i in range(0,type_num):
            tmp_data = np.zeros([type_sum[i]+1,len(data[1,:])])
            tmp_label = np.zeros([type_sum[i]+1])
            index = 0
            for j in range(len(data[:,1])-1):
                if self.k_means_clf.predict(data[j,:]) == i:
                    #print 'i:',i,'len_label:', len(tmp_label),'index:',index
                    #print 'j:',j,'len data[:,1]',len(data[:,1])
                    #print 'label[index',tmp_label[index]
                    tmp_data[index, :] = data[j,:]
                    tmp_label[index] = label[j]
                    index +=1
            clf_tmp = svm.SVC(kernel = 'linear', probability = True)
            clf_tmp.fit(tmp_data, tmp_label)
            self.clf.append(clf_tmp)




    def big_scale_classfier(self, data, type_num = 12):
        '''
        输入一组wifi,自动分大类
        :param data:
        :return:
        '''

        k_means_clf = KMeans(init = 'random', n_clusters=type_num, n_init= 10)
        k_means_clf.fit(data)
        K_means_label = k_means_clf.predict(data)

        return K_means_label, k_means_clf

    def predict(self,data):
        '''
        跟其余分类器的predict一样，输入数据，输出结果
        :param data:
        :return:
        '''
        label = np.zeros([len(data[:,1])])
        for i in range(0,len(data[:,1])-1):
            type_clf = self.k_means_clf.predict(data[i,:])
            label[i] = self.clf[type_clf].predict(data[i,:])
        return label



if __name__ == '__main__':
    own_data = data_manage.data_manage()
    pose, wifi = own_data.get_data(own_data.how_many()-1)
    multilayerquick = multilayer(wifi,pose)
#    K_means_label, k_means_clf = big_scale_classfier(wifi)
#
#    print K_means_label
#    #plt.figure(1111)
#    for i in range(1,10):
#        plt.figure(i)
#        for j in range(len(K_means_label)):
#            if K_means_label[j] == i:
#                plt.plot(pose[j,0],pose[j,1],'or')
#
#    plt.show()
#    print 'k_means_clf', k_means_clf
