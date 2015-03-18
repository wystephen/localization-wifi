__author__ = 'steve'
# -*- coding:utf-8 -*-
from sklearn import svm
import data_transfor
import numpy
import matplotlib.pyplot as plt

def svm_quick(data,label):

    clf = svm.SVC()

    print clf.fit(data, label)#训练

    err = 0
    err_times = 0
    ans = numpy.zeros(len(label))
    for i in range(0, len(label)-1):
        ans[i] = clf.predict(data[i, :])
        err += (ans[i] - label[i]) * (ans[i] - label[i])
        if abs(ans[i] - label[i]) > 2:
            err_times  = err_times + 1
            print 'ans:', ans[i],'pose_label: ', label[i]#显示错误分类的结果，和真实类别
        #print err,'  ',err_times,' i:',i, 'i-err_times:' , i-err_times
    print 'err:',err,'err_times:',err_times
    print err_times*100.0/len(label) ,' %'#分类错误率
    return ans,label,clf


def svm_test(wifi_file,pose_file):
    #wifi, pose = read_data.read_data()
    wifi = numpy.loadtxt(wifi_file)
    pose = numpy.loadtxt(pose_file)

    print 'pose',pose
    #以1.5m为间隔将数据离散化，
    pose_label, pose_lable_dict = data_transfor.pose_to_label(pose, 2)
    clf = svm.SVC()
    print 'wifi', wifi
    print clf.fit(wifi, pose_label)#训练

    print 'poselabel', pose_label#输出，可以看出分了多少各类别
    err = 0
    err_times = 0
    ans = numpy.zeros(len(pose_label))
    for i in range(0, len(pose_label)-1):
        ans[i] = clf.predict(wifi[i, :])
        err += (ans[i] - pose_label[i]) * (ans[i] - pose_label[i])
        if abs(ans[i] - pose_label[i]) > 2:
            err_times  = err_times + 1
            print 'ans:', ans[i],'pose_label: ', pose_label[i]#显示错误分类的结果，和真实类别
        #print err,'  ',err_times,' i:',i, 'i-err_times:' , i-err_times
    print 'err:',err,'err_times:',err_times
    print err_times*100.0/len(pose_label) ,' %'#分类错误
	return clf, pose_label_dict


######################################################################
#
#
#
#######################################################################
if __name__ == '__main__':
    clf, pose_label_dict = vm_test('sourcedata/201503141218/end_wifi.txt','sourcedata/201503141218/end_pose.txt')
	#没有尝试过交叉验证
	test_pose = numpy.loadtxt('sourcedata/201503141231/end_pose.txt')
	test_wifi = numpy.loadtxt('sourcedata/201503141231/end_wifi.txt')

	ans_pose_label = numpy.zeros(len(test_wifi))
	errs = numpy.zeros(len(test_wifi))
	error_times = 0
	for i in range(0,len(test_wifi)-1)：
		ans_pose_label[i] = clf.predict(test_wifi[i,:])
		tmp_pose = pose_lable_dict[ans_pose_label[i]]
		errs[i] = ((tmp_pose[0] - test_pose[i,0])*(tmp_pose[0] -
			test_pose[i,0])+(tmp_pose[1] - test_pose[i,1]) *(tmp_pose[1] -
				test_pose[i,1])
		)
		if errs[i] < 5.0:
			error_times +=1

	plt.figure(1)
	print 'acc:‘ error_times * 1.0 / len(test_pose)



