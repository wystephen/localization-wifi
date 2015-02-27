__author__ = 'steve'
# -*- coding: utf_8 -*-

from pybrain.structure import  FeedForwardNetwork, LinearLayer, SigmoidLayer, TanhLayer, FullConnection, MotherConnection
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.datasets import  SupervisedDataSet
import numpy
from pybrain.tools.shortcuts import buildNetwork
net = buildNetwork(165,20,2)
#建立神经网络
n = FeedForwardNetwork()
#确定神经网络形式
inLayer = LinearLayer(165)
hiddenLayer = SigmoidLayer(20)
hiddenLayer2 = TanhLayer(15)
outLayer = LinearLayer(2)

in_to_hidden = FullConnection(inLayer,hiddenLayer)
hidden_to_hidden2 = FullConnection(hiddenLayer, hiddenLayer2)
hidden2_to_outLayer = FullConnection(hiddenLayer2,outLayer)

n.addInputModule(inLayer)
n.addModule(hiddenLayer)
n.addModule(hiddenLayer2)
n.addOutputModule(outLayer)

n.addConnection(in_to_hidden)
n.addConnection(hidden_to_hidden2)
n.addConnection(hidden2_to_outLayer)

print n
#数据加载方法——数据集
data = SupervisedDataSet(165, 2)#  (输入数据个数，输出数据个数）
#添加数据到数据集用方法：data.addSample(inp,target)
fp = open('wifi_end.txt','rb')
wifi_list = fp.readlines()
fp.close()
fp= open('pose.txt','rb')
pose_list = fp.readlines()
fp.close()

wifi_array = numpy.zeros([len(wifi_list), 165])
for line in wifi_list:
    li = line.split(' ')
    for i in range(0, 164):
        wifi_array[wifi_list.index(line), i] = int(li[i])
pose_array = numpy.zeros([len(pose_list), 2])
for line in pose_list:
    li = line.split(' ')
    pose_array[pose_list.index(line),0] = float(li[0])
    pose_array[pose_list.index(line),1] = float(li[1])
for i in range(0, 2001):
    data.addSample((wifi_array[i,:]), (pose_array[i, :]))
pose_array = numpy.load('pose.txt')
wifi_array=numpy.load('wifi_end.txt')

#添加划分训练集和测试集：
testdata, traindata = data.splitWithProportion(0.25)
#testdata.
#设置训练方法 采用BP
#bp的默认参数
#trainer = BackpropTrainer(n, dataset=traindata,
#                          learningrate=0.01,
#                          irdecacy = 1.0, momentum=0.0,
#                          verbose=False, batchlearning=False,
#                          weightdecay = 0.0)
trainer = BackpropTrainer(n, traindata)
notok = True
while notok:
    print trainer.train()

#训练直道收敛
#trainer.trainUntilConvergence()

#从神经网络输出
outdata = n.activate(testdata)
