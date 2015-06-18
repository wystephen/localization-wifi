__author__ = 'Administrator'
# -*- coding:utf-8 -*-
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import os

import random

import data_manage
import time
import timer
def distance(x1,x2):
    x1=(x1-x2)**2
    dis = sum(x1)
    dis = dis ** 0.5
    return dis









def pose2label(pose):
    pose_label = np.loadtxt('tmp_pose_landmark')
    label = np.zeros(len(pose))
    for i in range(len(pose[:,1])):
        for j in range(len(pose_label)):
            if ((pose_label[j,0] - pose[i,0])**(2)+(pose_label[j,1]-pose[i,1])**2)**(0.5)<3.0:
                label[i] = j
    return label,pose_label


class newKNN:
    def __init__(self,n_neighbors=3):
        self.n_neighbors = n_neighbors

    def distance(self,x1,x2):
        x1=(x1-x2)**2
        dis = sum(x1)
        dis = dis ** 0.5
        return dis


    def search(self,x):
        '''
        找K个最邻近点
        :param x:
        :return:
        '''
        dis = list()
        for i in range(len(self.save_in)):
            dis.append(self.distance(x,self.save_in[i,:]))
        dis = np.asarray(dis)
        sordis = np.argsort(dis)
        Y = list()
        Y_dis = list()
        for i in range(self.n_neighbors):
            Y.append(self.save_out[sordis[i]])
            Y_dis.append(dis[sordis[i]])
        #print 'len Y',len(Y)
        return Y,Y_dis

    def fit(self,X,Y):
        self.save_in = X
        self.save_out = Y
        # np.max(Y),np.min(Y)
        self.prob = np.zeros([np.max(Y),np.max(Y)])
        #self.prob_get()
        if os.path.exists(r'./prob_m'):
            self.prob=np.loadtxt('prob_m')
        #for i in range(len(self.prob)):
        #    sum_l = sum(self.prob[i,:])
        #self.prob[i,:] = self.prob[i,:]/1.0/sum_l
        #self.prob[y,x]   y代表临近点钟出现序号为ylabel，x在表真实坐标为x，
        # 既真是坐标为x，出现近点中出现y的概率

    def prob_get(self):
        #print 'o1'
        for i in range(len(self.save_in)):
            #print 'ooo'

            near_Y,Y_dis = self.search(self.save_in[i,:])
            #print near_Y
            near_Y = np.asarray(near_Y)
            #计算概率，
            for j in range(len(near_Y)):
                #print 'i:',i
                #print 'de',near_Y[j]
                y = int(near_Y[j])
                self.prob[y-1,int(self.save_out[i])-1]+=1
        print self.prob
        np.savetxt('prob_m',self.prob)



    def predict(self,X):
        '''

        :param X:
        :return:
        '''
        #print '改变概率'
        out_Y = list()
        print self.prob
        last_y = 0
        last_y_list = list()
        last_y_p = list()

        for i in range(len(X)):
            near_Y,near_Y_dis = self.search(X[i,:])
            p = np.zeros(np.max(self.save_out)+1)
            for j in near_Y:
                p[j] = 1.0 * 1.5**(-abs(last_y-j))
                for k in range(len(near_Y)):
                    p[j] = p[j] * self.prob[near_Y[k]-1,j-1]





            sor = np.argsort(p)
                #print 'sort',sor
            if abs(sor[-1]-last_y) < 4 and sor[-1] >= last_y:
                last_y = sor[-1]
            else:
                last_y = last_y
            #print 'p',p[sor[-1]],p[sor[-2]]
            #print last_y,sor[-1]
            out_Y.append(last_y)


        return out_Y

    def cal_prob(self,near_Y,x):

        prob = 1.0
        for i in range(len(near_Y)):
            #print near_Y,'near_y'
            #print x,'x'
            prob = prob * self.prob[near_Y[i]-1,x-1]
        return prob


    def sir_predict(self,X,p_num):
        random.seed()#初始化随机种子
        out_Y = list()

        last_y_list = list()
        last_y_list.append(1)
        last_y_list.append(1)
        last_y_list.append(1)

        last_y_p = list()
        last_y_p.append(1)
        last_y_p.append(1)
        last_y_p.append(1)
        last_y = 0
        #p_num =30
        print 'p_num5:',p_num
        for index in range(len(X)):
            near_Y,near_Y_dis = self.search(X[index,:])
            #print near_Y
            y_list_tmp = list()
            y_p_tmp = list()
            #矫正阶段~修正权值
            #每个原来的种子循环一次
            for i in range(len(last_y_list)):
                #原来每个种子撒p_num个种子
                for step in range(0,p_num):
                    #种子改成高斯分布随机撒看看
                    s = 1000
                    while s < -30 or s > 30:
                        s = random.gauss(0,5)
                        s = int(s)
                    step = step -int(p_num/2.0)
                    step = s
                    if (last_y_list[i]+step > np.max(self.save_out)):
                        last_y_list = last_y_list
                        step = 0
                    if (last_y_list[i]+step < np.min(self.save_out)):
                        #print 'sss'
                        step = 0

                    y_list_tmp.append(last_y_list[i]+step)
                    y_p_tmp.append(self.cal_prob(near_Y,last_y_list[i]+step)*\
                                   1.0 * 1.5**(-abs((step))/5.0))#*last_y_p[i])

            #对新的种子排序 重采样
            sor =np.argsort(np.asarray(y_p_tmp))
            y_p_tmp = np.asarray(y_p_tmp)
            y_list_tmp = np.asarray(y_list_tmp)
            last_y_list = list()
            last_y_p = list()
            y_p_tmp = y_p_tmp/1.0/sum(y_p_tmp)
            for best_i in range(1,int(p_num/2.0),1):
                last_y_list.append(y_list_tmp[sor[-best_i]])
                last_y_p.append(y_p_tmp[sor[-best_i]])

            last_y= y_list_tmp[sor[-1]]

            #print last_y

            out_Y.append(last_y)
        return out_Y

def err(out_Y,pose,landmark):
    err = list()
    for i in range(len(out_Y)):
        err.append(distance(landmark[int(out_Y[i-1])],pose[i,:]))
    return err


if __name__ == '__main__':
    print 'new prob for every one'
    data = data_manage.data_manage()
    err5 = list()
    err3 = list()
    start_time = time.clock()
    for kk in range(5):
        kk = 3
        pose, wifi, test_pose, test_wifi = data.get_full_test_data(kk,5)
        #先用pose wifi 作为训练，test_pose 作为测试
        print 'data_inpu_end'

        label,landmark = pose2label(pose)
        test_label,landmark = pose2label(test_pose)
        n_ne=3
        KNN = newKNN(n_neighbors=n_ne)

        KNN.fit(wifi,label)
        #KNN.prob_get()

        #out_Y=KNN.predict(test_wifi)
        out_Y = KNN.sir_predict(test_wifi,50)

        the_err = err(out_Y,test_pose,landmark)

        np.savetxt('prob_err'+str(kk),the_err)
        #统计一下 err
        err_step = list()
        err_all = list()
        for i in range(0,150,1):
            i = i/10.0
            count = 0
            for j in range(len(the_err)):
                if the_err[j] < i:
                    count+=1
            err_step.append(i)
            err_all.append(count/1.0/len(the_err))
            if i == 5.0:
                err5.append(count/1.0/len(the_err))
                print '5.0:',count/1.0/len(the_err)
            if i==3.0:
                err3.append(count/1.0/len(the_err))
                print '3.0:',count/1.0/len(the_err)
        err_step = np.asarray(err_step)
        err_all = np.asarray(err_all)
        np.savetxt('err_step',err_step)
        np.savetxt('err_all_prob'+str(kk),err_all)
        plt.figure(2)
        plt.grid()
        plt.plot(err_step,err_all)



        plt.figure(1)
        plt.plot(the_err)
        plt.grid()

    err5= np.asarray(err5)
    err3 = np.asarray(err3)
    print n_ne
    for i in range(len(err5)):
        print '[',err3[i],',',err5[i],']'
    end_time = time.clock()
    print 'start:',start_time,'end:',end_time
    print 'use time:',end_time -start_time
    plt.show()




































