__author__ = 'Administrator'
# -*- coding:utf-8 -*-

import numpy as np
import matplotlib as plt
import scipy as sp

import pybrain.structure.networks.network
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet

#最简单的神经网络


class label_choice:

    def __init__(self, input_n, output_n):
        print input_n, '   ', output_n
        self.data = SupervisedDataSet(input_n,output_n)
        self.net = buildNetwork(input_n,int((input_n*output_n)**0.5),5,1)
        self.trainer = BackpropTrainer(self.net,self.data)
    def add_data(self,input_arr,output_arr):
        self.data.addSample(input_arr,output_arr)
    def train_model(self):

        index_num =0
        last_ans = 0
        this_ans = 100000

        ##while abs(this_ans-last_ans)>0.001:
         #  save_fiel = open('save_the_train.txt','a')
         #  last_ans = this_ans
         #  this_ans = self.trainer.train()
         #  print 'this:', this_ans
         #  save_fiel.write('index_num '+str(index_num) )
         #  save_fiel.write(' this ans:'+str(this_ans))
         #  save_fiel.write('params:'+str(self.net.params))
         #  save_fiel.closed
        # 'netparame:',self.net.params

        #save_fiel.closed
        self.trainer.trainUntilConvergence()
        print self.net

        return self.net

    def test_model(self, in_arr):
        return self.net.activate(in_arr)






if __name__ == '__main__':
    in_arr_tmp = np.loadtxt(str('label_save/'+str(1)+'out'))
    out_arr_tmp = np.loadtxt(str('label_save/'+str(1)+'pose'))
    choic_model = label_choice(len(in_arr_tmp[1,:]),1)
    #读入数据集，然后训练
    for i in range(0,6):
        in_arr = np.loadtxt(str('label_save/'+str(i)+'out'))
        out_arr = np.loadtxt(str('label_save/'+str(i)+'pose'))
        for j in range(len(in_arr[:,1])):
            choic_model.add_data(in_arr[j,:],out_arr[j])
    #加载数据完毕开始训练
    out_net = choic_model.train_model()

    print out_net
    print '开始测试数据集：'
    err = np.zeros(600000)
    err_index = 0
    for i in range(0,6):
        in_arr = np.loadtxt(str('label_save/'+str(i)+'out'))
        out_arr = np.loadtxt(str('label_save/'+str(i)+'pose'))
        for j in range(len(in_arr[:,1])):
            out = choic_model.test_model(in_arr[j])
            err[err_index] = abs(out-out_arr[j])
            if err[err_index] == 0:
                err[err_index] = 0.0001
            err_index +=1
    print err
    np.savetxt('err_for_ann', err)




