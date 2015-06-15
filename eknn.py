__author__ = 'Administrator'
# -*- coding:utf-8 -*-

import numpy as np
import scipy as sp


class eknn:
    def __init__(self,n_neighbors=3):
        self.save_in = list()
        self.save_out = list()
        self.n_neighbors = n_neighbors
        self.last_y=0


    def fit(self ,X ,Y):
        self.save_in = X
        self.save_out = Y

    def distance(self,x1,x2):
        #x1=(x1-x2)**2
        #dis = sum(x1)
        #dis = dis ** 0.5
        #return dis
        up = 0
        up = np.sum(x1*x2)


        dis = -up/np.sum(x1)/np.sum(x2)


        return dis




    def search(self,x):
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
        return Y,Y_dis





    def predict(self,X):
        out_Y = list()

        for i in range(len(X)):
            Y, Y_dis = self.search(X[i])
            stp = 0
            #if self.last_y  <1909:
            #    Y.append(self.last_y)
            #    stp =1
            #    print ' new'
            Y = np.asarray(Y)
            wy = list()
            for i in range(len(Y)):
                tmp = 1.5 **(-abs(Y[i]-self.last_y)*1.0)
                if 1>tmp >  0.5:
                    tmp = 0.9
                wy.append(tmp)
            wy = np.asarray(wy)
            #out_Y.append(int(sum(Y)/1.0/(self.n_neighbors+stp)))
            out_Y_tmp = int(sum(wy*Y)/1.0/sum(wy))
            out_Y.append(out_Y_tmp)
            self.last_y = out_Y[-1]
            #print out_Y[i]
            if i /100.0==i/100:
                sss=1
                print '1111111111'


        return np.asarray(out_Y)





