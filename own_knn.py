__author__ = 'Administrator'
# -*- coding:utf-8 -*-

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt

import sys


class own_knn:
    def __init__(self):
        self.save_label_X = list()
        self.save_label_Y = list()

    def train(self,X,Y):
        X = np.asarray(X)
        Y = np.asarray(Y)

        for i in range(len(X)):
            self.save_label_X.append(X[i,:])
            self.save_label_Y.append(Y[i])

    def distance(self,w1,w2):
        w1 = np.asarray(w1)
        w2 = np.asarray(w2)
        dis = 0
        for j in range(len(w1)):
            dis += abs(w1[j] -w2[j])

        return dis



    def predict_easy(self,X):
        min_dis = 100000
        label = 0

        for i in range(len(self.save_label_X)):
            if self.distance(self.save_label_X[i],X) < min_dis:
                min_dis = self.distance(self.save_label_X[i],X)
                label = self.save_label_Y[i]

        return label

    def predict(self,X):
        Y =list()
        for i in range(len(X)):
            Y.append(self.predict_easy(X[i,:]))
        Y = np.asarray(Y)

        return Y



def own_knn_test(X,Y):
    X = np.asarray(X)
    Y = np.asarray(Y)

    clf = own_knn()
    clf.train(X,Y)
    return clf.predict(X), Y, clf