__author__ = 'steve'
# -*- coding:utf-8 -*-

import numpy

import matplotlib.pyplot as plt
from sklearn.cluster import MiniBatchKMeans, KMeans, AffinityPropagation

import data_transfor
import svm


half_pose_test = numpy.loadtxt('data_save/20153221517end_pose.txt')
half_pose = numpy.loadtxt('data_save/20153221517end_pose.txt')

half_wifi_test = numpy.loadtxt('data_save/20153221517end_wifi.txt')
half_wifi = numpy.loadtxt('data_save/20153221517end_wifi.txt')

# half_pose_test, half_wifi_test = data_transfor.half_data_trans('data_save/18end_pose.txt',
#                                                               'data_save/18end_wifi.txt')
#half_pose, half_wifi = data_transfor.half_data_trans('data_save/31end_pose.txt',
#                                             'data_save/31end_wifi.txt')
numpy.random.seed(0)
plt.figure(10)
plt.plot(half_pose_test[:, 0], half_pose_test[:, 1], 'or')
plt.plot(half_pose[:, 0], half_pose[:, 1], 'ob')
print '数据读取完毕'
K_means_type_num = 100
K_means = KMeans(init='random', n_clusters=K_means_type_num, n_init=10)
K_means.fit(half_wifi)

print 'kmeans end'
K_means_label = K_means.labels_
print K_means_label
ans, label, clf = svm.svm_quick(half_wifi, K_means_label)

print 'train over'

plt.figure(1)
plt.plot(K_means_label, 'o')
plt.grid(1)

plt.figure(3)
landmark = numpy.zeros([K_means_type_num, 2])
#把自然聚类的每个类别第一个
for i in range(0, len(label)):
    if label[i] != label[i - 1]:
        landmark[label[i], :] = half_pose[i, :]
plt.plot(landmark[:, 0], landmark[:, 1], 'o')
####显示提取出来的特殊点

print 'begin to get error'
error = numpy.zeros(len(half_wifi_test))
small_error = 0
biggest_error = 0
error_pose_num = 0
error_pose = numpy.zeros([10000, 2])
##用另一组数据测试 ，看差值
for i in range(0, len(half_wifi_test)):
    error[i] = ((landmark[(clf.predict(half_wifi_test[i, :])), 0] - half_pose_test[i, 0]) * \
                (landmark[(clf.predict(half_wifi_test[i, :])), 0] - half_pose_test[i, 0]) \
                + (landmark[clf.predict(half_wifi_test[i, :]), 1] - half_pose_test[i, 1]) * \
                (landmark[clf.predict(half_wifi_test[i, :]), 1] - half_pose_test[i, 1])) ** (0.5)
    #print error[i]
    if error[i] < 5.0:
        small_error += 1
    if error[i] > 5.0 and error[i] < 10.0:
        error_pose[error_pose_num, :] = half_pose_test[i, :]
        error_pose_num += 1
    if error[i] > 10.0:
        biggest_error += 1
print 'small:', small_error, 'biggest:', biggest_error, 'acc:', small_error * 1.0 / (len(error) - biggest_error)
plt.figure(4)
plt.plot(error, 'o')
plt.grid(4)

plt.figure(5)
plt.plot(error_pose[:, 0], error_pose[:, 1], 'o')

plt.show()