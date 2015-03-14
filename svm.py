__author__ = 'steve'
# -*- coding:utf-8 -*-
from sklearn import svm
import data_transfor
import numpy

def svm_test(wifi_file,pose_file):
    #wifi, pose = read_data.read_data()
    wifi = numpy.loadtxt(wifi_file)
    pose = numpy.loadtxt(pose_file)

    print 'pose',pose
    #以1.5m为间隔将数据离散化，
    pose_label, pose_lable_dict = data_transfor.pose_to_label(pose, 1.5)
    clf = svm.SVC()
    print 'wifi', wifi
    print clf.fit(wifi, pose_label)#训练

    print 'poselabel', pose_label#输出，可以看出分了多少各类别
    err = 0
    err_times = 0
    ans = numpy.zeros(len(pose_label))
    for i in range(0,len(pose_label)-1):
        ans[i] = clf.predict(wifi[i, :])
        err += (ans[i] - pose_label[i]) * (ans[i] - pose_label[i])
        if abs(ans[i] - pose_label[i]) > 2:
            err_times  = err_times + 1
            print 'ans:',ans[i],'pose_label: ',pose_label[i]#显示错误分类的结果，和真实类别
        #print err,'  ',err_times,' i:',i, 'i-err_times:' , i-err_times
    print 'err:',err,'err_times:',err_times
    print err_times*100.0/len(pose_label) ,' %'#分类错误率


######################################################################
#
#
#
#######################################################################
if __name__ == '__main__':
    svm_test('end_wifi.txt','end_pose.txt')