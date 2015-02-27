__author__ = 'steve'
from sklearn import svm
import read_data
import data_transfor
import numpy
#wifi, pose = read_data.read_data()
wifi = numpy.loadtxt('wifi_end.txt')
pose = numpy.loadtxt('pose.txt')
print 'pose',pose
pose_label, pose_lable_dict = data_transfor.pose_to_label(pose, 1.5)

clf = svm.SVC()
print clf.fit(wifi, pose_label)
print 'wifi', wifi
print 'poselabel', pose_label
dec = clf.decision_function(wifi[55,:])
print dec.shape[1]
print 'predict', clf.predict(wifi[1,:])
err = 0
err_times = 0
ans = numpy.zeros(len(pose_label))
for i in range(0,len(pose_label)-1):
    ans[i] = clf.predict(wifi[i,:])
    err += (ans[i] - pose_label[i]) * (ans[i] * pose_label[i])
    if abs(ans[i] - pose_label[i])>2:
        err_times +=1
        print 'ans:',ans[i],'pose_label: ',pose_label[i]
    #print err,'  ',err_times,' i:',i, 'i-err_times:' , i-err_times
print 'err:',err,'err_times:',err_times
print err_times*100.0/len(pose_label) ,' %'