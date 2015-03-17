__author__ = 'steve'
# -*- coding:utf_8 -*-
import numpy
import matplotlib.pyplot as plt
import data_transfor

plt.figure(1)

pose1= numpy.loadtxt('sourcedata/201503141218/end_pose.txt')
pose2= numpy.loadtxt('sourcedata/201503141231/end_pose.txt')

plt.plot(pose1[:,0],pose1[:,1])
plt.plot(pose2[:,0],pose2[:,1])
pose_label, pose_lable_dict = data_transfor.pose_to_label(pose1, 3)
label_array = numpy.zeros([len(pose_lable_dict),2])
for (point,lable) in pose_lable_dict.items():
    print 'key:' , point , 'value:' , lable
    label_array[point,0] = lable[0]
    label_array[point,1] = lable[1]

plt.plot(label_array[:,0],label_array[:,1],'or')

plt.show()