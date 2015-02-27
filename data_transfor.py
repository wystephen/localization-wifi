__author__ = 'steve'
# -*- coding:utf_8 -*-
#

import os
import sys
import numpy, scipy

def pose_to_label(pose, distance):
    last_i = 0
    label = numpy.zeros(len(pose))
    label_dict = dict()
    label_dict[0] = [pose[0, 0], pose[0, 1]]
    label[0] = 0
    print label[0]
    for i in xrange(len(pose)):
        if (pose[i,0]-pose[last_i,0])*(pose[i,0]-pose[last_i,0]) + \
                        (pose[i, 1]-pose[last_i, 1])* (pose[i, 1]-pose[last_i, 1])< distance * distance:
            label[i] = label[last_i]

        else:
            label[i] = label[last_i] + 1
            label_dict[label[i]] = [pose[i, 0], pose[i, 1]]
            last_i = i
    print 'lable_in' , label
    return label, label_dict

'''
infile = open('pose.txt')
laser_list = infile.readlines()
infile.close()
label_list = list
step = 0
pose_array = numpy.zeros((len(laser_list),2))
for line in laser_list:
    line =  line.split(' ')
    pose_array[step, 0] = line[0]
    pose_array[step, 1] = line[1]
    step += 1

print len(pose_array), step

a, adict = pose_to_label(pose_array, 1.5)

fout = open('poselabel.txt','w')
for i in range(0,len(pose_array)-1):
    fout.write(str(int(a[i])) + '\n')
fout.close()
'''