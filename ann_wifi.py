__author__ = 'steve'
# -*- coding: utf_8 -*-

from pybrain.structure import  FeedForwardNetwork, LinearLayer, SigmoidLayer, TanhLayer, FullConnection, MotherConnection
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.datasets import  SupervisedDataSet
#建立神经网络
n = FeedForwardNetwork()
#确定神经网络形式
inLayer = LinearLayer(100)
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

print n.sortModules()
#数据加载方法——数据集
data = SupervisedDataSet(50,2)#  (输入数据个数，输出数据个数）
#添加数据到数据集用方法：data.addSample(inp,target)

#添加划分训练集和测试集：
testdata, traindata = data.splitWithProportion(0.25)
#testdata.
#设置训练方法 采用BP
trainer = BackpropTrainer(n,dataset=traindata,learningrate=0.01, irdecacy = 1.0, momentum=0.0,verbose=False, batchlearning= False,wigh)