__author__ = 'Administrator'
# -*- coding:utf-8 -*-

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt


import data_manage
import data_preprocessing
import data_transfor

def D_value_trans(wifi, pose):
    out_wifi = list()
    out_pose = list()
    for i in range(len(pose)):
        pose_tmp = list()
        wifi_tmp = list()
        for j  in range(len(pose)-i):
            if ((pose[i,0]- pose[i+j,0])**2+(pose[i,1]-pose[i+j,1])**2)**0.5 < 5.0:
                pose_tmp.append(pose[i+j])
                wifi_tmp.append(wifi[i+j])
            else:
                break
        pose_tmp = np.asarray(pose_tmp)
        wifi_tmp = np.asarray(wifi_tmp)

        wifi_despresion = np.zeros(len(wifi[1,:]))
        for k in range(len(wifi[1,:])):

            #wifi_despresion[k] = np.std(wifi_tmp[:,k])/1.0 /(np.average(wifi_tmp[:,k]) + 0.0000001)
            wifi_despresion[k] = wifi[i,k] - np.average(wifi_tmp[:,k])
        out_wifi.append(wifi_despresion)
        out_pose.append(pose[i,:])
    out_wifi = np.asarray(out_wifi)
    out_pose = np.asarray(out_pose)
    #plt.plot(out_wifi[:,20:25],'o')
    #plt.show()
    #return out_wifi, out_pose
    return wifi, pose



