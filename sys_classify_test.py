__author__ = 'Administrator'
# -*- coding:utf-8 -*-

import numpy

import matplotlib.pyplot as plt
from sklearn.cluster import MiniBatchKMeans, KMeans, AffinityPropagation
from sklearn.multiclass import OneVsRestClassifier
from sklearn.multiclass import OneVsOneClassifier
import data_transfor
import classify_use_test
import data_preprocessing
import data_manage
import multi_layer_class

import D_value_class


def pose_test_func(half_pose,half_wifi,half_pose_test,half_wifi_test):

    half_wifi = data_preprocessing.rss_dis(half_wifi)
    half_wifi_test = data_preprocessing.rss_dis(half_wifi_test)
    half_wifi = data_preprocessing.data_transform(half_wifi)
    half_wifi_test = data_preprocessing.data_transform(half_wifi_test)


    print 'len train:',len(half_wifi), 'len test:', len(half_wifi_test)
    # half_pose_test, half_wifi_test = data_transfor.half_data_trans('data_save/18end_pose.txt',
    # 'data_save/18end_wifi.txt')
    #half_pose, half_wifi = data_transfor.half_data_trans('data_save/31end_pose.txt',
    #                                             'data_save/31end_wifi.txt')

    #numpy.random.seed(0)
    #plt.figure(10)
    #plt.plot(half_pose_test[:, 0], half_pose_test[:, 1], 'or')
    #plt.plot(half_pose[:, 0], half_pose[:, 1], 'ob')
    print '数据读取完毕'
    #K_means_type_num = 250
    #K_means = KMeans(init='random', n_clusters=K_means_type_num, n_init=10)
    #K_means.fit(half_wifi)
    pose_label = numpy.loadtxt('tmp_pose_landmark')
    K_means_label = numpy.zeros(len(half_wifi))
    for i in range(len(half_pose[:,1])):
        for j in range(len(pose_label)):
            if ((pose_label[j,0] - half_pose[i,0])**(2)+(pose_label[j,1]-half_pose[i,1])**2)**(0.5)<3.0:
                K_means_label[i] = j

    print 'kmeans end'
    #numpy.savetxt('save_pose_label_new',K_means_label)
    #numpy.savetxt('save_wifi_label_new',half_wifi)

    #print K_means_label
    #支持向量机的语句，过得去 0.6（5m），0.1-0.2（5-7m）--disige--ok---第五个化成 rbf--效果不好
    ans, label, clf = classify_use_test.svm_quick(half_wifi, K_means_label)#), kernel='linear')
    #随机森林，有问题？
    #ans, label, clf = classify_use_test.randomforest_quick(half_wifi_test,K_means_label)
    #LDA 效果很差。
    #ans, label, clf = classify_use_test.LDA_quick(half_wifi,K_means_label)
    #one vs one classifier--dierge
    #ans, label, clf = classify_use_test.onevsone_quick(half_wifi,K_means_label)
    #one_vs_rest---效果不行
    #ans, label, clf = classify_use_test.onevsrest_quick(half_wifi,K_means_label)
    #adaboost--disange--不太稳定。
    #ans, label, clf = classify_use_test.adaboost_quick(half_wifi,K_means_label)
    #knn 不错 ， 同 支持向量机
    #ans, label, clf = classify_use_test.knn_quick(half_wifi, K_means_label)
    #bayes--disange--效果差
    #ans, label, clf = classify_use_test.bayes_quick(half_wifi,K_means_label)

    #自己写的多个层次分开分类的分类器
    #clf = multi_layer_class.multilayer(half_wifi,K_means_label,type_num=10)
    print 'train over'


    plt.figure(3)
    landmark = pose_label
    #把自然聚类的每个类别第一个
    #for i in range(0, len(label)):
    #    if label[i] != label[i - 1]:
    #        landmark[label[i], :] = half_pose[i, :]
    #plt.plot(landmark[:, 0], landmark[:, 1], 'o')
    ####显示提取出来的特殊点

    print 'begin to get error'
    error = numpy.zeros(len(half_wifi_test))
    small_error = 0
    biggest_error = 0
    error_pose_num = 0
    error_pose = numpy.zeros([50000, 2])
    ##用另一组数据测试 ，看差值
    predict_ans = clf.predict(half_wifi_test)
    plt.figure('show train_ans')
    plt.plot(K_means_label,'o')
    plt.figure('show predict_ans')
    plt.plot(predict_ans)

    test_in_train =0
    for i in range(len(half_wifi_test)):
        if half_wifi_test[i,:] in half_wifi:
            test_in_train+=1
    print 'testJ_in_train',test_in_train
    #predict_ans = K_means.predict(half_wifi_test)
    for i in range(0, len(half_wifi_test)):
        error[i] = ((landmark[predict_ans[i], 0] - half_pose_test[i, 0]) * \
                    (landmark[predict_ans[i], 0] - half_pose_test[i, 0]) \
                    + (landmark[predict_ans[i], 1] - half_pose_test[i, 1]) * \
                    (landmark[predict_ans[i], 1] - half_pose_test[i, 1])) ** (0.5)
        #print error[i]
        if error[i] <= 3.0:
            small_error += 1
        if error[i] > 3.0 and error[i] < 5.0:

            error_pose_num += 1
        if error[i] > 7.0:
            biggest_error += 1
            error_pose[biggest_error, :] = half_pose_test[i, :]
    small_acc = small_error * 1.0 / (len(error))
    big_acc = error_pose_num*1.0/(len(error))
    print 'small:', small_error, 'biggest:', biggest_error, 'acc:', small_error * 1.0 / (len(error) )
    print 'biggest acc:', big_acc + small_acc
    plt.figure('error_show')
    plt.plot(error, 'o')


    #out_wifi_test = numpy.loadtxt('out_wifi.txt',dtype='int')

    out_wifi_file = open('out_wifi.txt','r')
    out_wifi_file = out_wifi_file.readlines()
    out_wifi_test = numpy.zeros([len(out_wifi_file),62])
    for i in range(len(out_wifi_file)):
        wifi_line = out_wifi_file[i]
        if len(wifi_line) > 10:
            wifi_line = wifi_line.split(' ')
            for j in range(1,len(wifi_line)-1):
                out_wifi_test[i,j] = float(wifi_line[j])



    out_wifi_test = data_preprocessing.data_transform(data_preprocessing.rss_dis(data_preprocessing.pre_process(out_wifi_test[:,1:len(out_wifi_test)])))
    plt.figure('test_wifi_out')
    plt.plot(clf.predict(out_wifi_test))



    #plt.figure(5)
    #plt.plot(error_pose[:, 0], error_pose[:, 1], 'o')


    #plt.show()
    return small_acc, big_acc+small_acc

if __name__ == '__main__':
    data = data_manage.data_manage()
    acc_save = numpy.zeros([data.how_many()*data.how_many(),2])
    num = 0
    #for i in range(data.how_many()):
    #    for j in range(data.how_many()):
    #        if i < j or j>5 or j < data.how_many() -2 or i < data.how_many()-1 :
    #            continue
    #        pose,wifi = data.get_data(i)
    #        pose_test,wifi_test = data.get_data(j)
    #        print 'len:', len(pose),'len_test',len(pose_test)
    #        acc_save[num,0] ,acc_save[num,1] = pose_test_func(pose,wifi,pose_test,wifi_test)
    #        num = num +1
    #        print '完成了：',((i*data.how_many())+(j))/((data.how_many())*(2.0))
    #        print acc_save

    #完整测试代码···
    for i in range(5):
        #test_pose, test_wifi, pose, wifi = data.get_full_test_data(i,7)
        pose, wifi, test_pose, test_wifi = data.get_full_test_data(i,5)
        #wifi, pose = D_value_class.D_value_trans(wifi, pose)
        #test_wifi, test_pose = D_value_class.D_value_trans(test_wifi,test_pose)
        #print 'pose',len(pose),'test_pose',len(test_pose)
        #acc_save[i,0], acc_save[i,1] = pose_test_func(pose,wifi,test_pose,test_wifi)#注意看这一句
        acc_save[i,0], acc_save[i,1] = pose_test_func(test_pose,test_wifi,pose,wifi)
        print '完成度：',i / 1.0/data.how_many()
    #快速测试代码
    #pose, wifi, test_pose, test_wifi = data.get_full_test_data(7,4)
    #print 'pose',len(pose),'test_pose',len(test_pose)
    #acc_save[1,0], acc_save[1,1] = pose_test_func(pose,wifi,test_pose,test_wifi)

    print acc_save
    plt.figure('all_right_acc')
    plt.plot(acc_save[:,0],'ro')
    plt.plot(acc_save[:,1],'bo')
    plt.grid()
    plt.show()
