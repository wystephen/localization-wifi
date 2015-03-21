# -*- coding:utf-8 -*-
from __future__ import print_function
# 不能使用，因为数据太少````不能grid search 寻找最优参数
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.svm import SVC
import numpy
import data_transfor

print(__doc__)
# def grid_search(wifi_file,pose_file):
wifi_file = 'end_wifi.txt'
pose_file = 'end_pose.txt'
# wifi, pose = read_data.read_data()
wifi = numpy.loadtxt(wifi_file)
pose = numpy.loadtxt(pose_file)

#以1.5m为间隔将数据离散化，
pose_label, pose_lable_dict = data_transfor.pose_to_label(pose, 1.5)
#wifi_train, wifi_test, pose_label_train, pose_label_test = train_test_split(
#    wifi, pose_label, test_size=0.1, random_state=0)
wifi_train = wifi
wifi_test = wifi
pose_label_train = pose_label
pose_label_test = pose_label
tuned_parameters = [{'kernel': ['rbf'], 'gamma': [1e-3, 1e-4, 1e-5, 1e-2],
                     'C': [1, 5, 10, 50, 100, 300, 700, 1000]},
                    {'kernel': ['linear'], 'C': [1, 10, 100, 1000]}]

scores = ['precision', 'recall']
for score in scores:
    print('# tuning hyper-parameters for %s' % score)
    print()

    clf = GridSearchCV(SVC(), tuned_parameters, cv=5, scoring=score)
    clf.fit(wifi_train, pose_label_train)

    print("Best parameters set found on development set:")
    print()
    print(clf.best_estimator_)
    print
    for params, mean_score, scores in clf.grid_scores_:
        print("%0.5f(+/-%0.03f) for %r" % (mean_score, scores.std() / 2, params))
    print()

    print('Detailed classification report:')
    print()
    print("The model is trained on the full development set.")
    print("The scores are computed on the full evaluation set.")
    print()
    y_true, y_pred = pose_label_test, clf.predict(wifi_test)
    print(classification_report(y_true, y_pred))
    print()




    #if __name__ == '__main__':
    #    grid_search('end_wifi.txt','end_pose.txt')