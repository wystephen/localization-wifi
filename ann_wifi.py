__author__ = 'steve'
# -*- coding: utf_8 -*-

from pybrain.structure import  FeedForwardNetwork, LinearLayer, SigmoidLayer, TanhLayer, FullConnection, MotherConnection
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.datasets import  SupervisedDataSet
import numpy
from pybrain.tools.shortcuts import buildNetwork
from pybrain.utilities import percentError
net = buildNetwork(164,12,2)
#建立神经网络
n = FeedForwardNetwork()
#确定神经网络形式
inLayer = LinearLayer(164)
hiddenLayer = SigmoidLayer(15)
hiddenLayer2 = TanhLayer(10)
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
data = SupervisedDataSet(164, 2)#  (输入数据个数，输出数据个数）
#添加数据到数据集用方法：data.addSample(inp,target)
wifi = numpy.loadtxt('wifi_end.txt')
pose = numpy.loadtxt('pose.txt')
for i in range(0, 2379):
    data.appendLinked((wifi[i,:]),(pose[i,:]))

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
trainer = BackpropTrainer(net, traindata,learningrate=0.02,verbose=False,weightdecay=0.01)
notok = True
while notok:
    the = 5
    if the == 0:
        notok = False
    else:
       print  trainer.trainEpochs(int(the))
       print  trainer.train()
       print trainer.testOnData(testdata)
       if trainer.testOnData(testdata) < 100:
           break

#训练直道收敛
#trainer.trainUntilConvergence()

#从神经网络输出
