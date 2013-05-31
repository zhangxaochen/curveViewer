#coding=utf-8

'''
使用 GMM 训练并预测驾驶数据
'''

import os, sys, glob
import numpy as np

from sklearn.cross_validation import StratifiedKFold
from sklearn.mixture import GMM

class Driving:
	label=np.array([])
	feature=np.array([])
	
	#accelerate, decelerate, turn:
	actType=np.array([])
	
	_cnt=-1
	
	#generator 其实更方便， iterator 太蠢： 
	def __init__(self):
		self.next=self.__next__
		
	def __iter__(self):
		return self
	
	def __next__(self):
		self._cnt+=1
		if self._cnt == self.label.size:
			raise StopIteration
		return self.label[self._cnt], self.feature[self._cnt], self.actType[self._cnt] 
	
	def __getitem__(self, npArray):
		assert isinstance(npArray, np.ndarray) and npArray.dtype == bool
		
		res=Driving()
		res.label=self.label[npArray]
		res.feature=self.feature[npArray]
		res.actType=self.actType[npArray]
		return res
	
def loadFeatures():
	configFname='D:/Documents/Desktop/huaweiproj-data-20130517/afterSplit/config_features.txt'
	configFile=open(configFname)
	featureDic={}
	for idx, line in enumerate(configFile.readlines()):
		if idx % 2 == 0:
			#line 带换行符
			tag=line.split('\n')[0]
		else:
			if not featureDic.get(tag):
				featureDic[tag] = list(map(float, line.split()))
	#print('=============featureDic:', featureDic)
	
	label=[]
	feature=[]
	actType=[]
	for k, v in sorted(featureDic.items()):
		info=k.split('_')
		#d1, d2, l1, l2:
		name=info[1]
		if name.startswith('d'):
			label.append(0)
		elif name.startswith('l'):
			label.append(1)
		feature.append(v)
		actType.append(info[3])
	
	driving=Driving()
	driving.label=np.array(label)			#label 即 person 编号
	driving.feature = np.array(feature)
	driving.actType=np.array(actType)
	
	return driving

def trainAndPredWithCovars(data, covars):
	assert isinstance(data, Driving)
	assert isinstance(covars, list)
	
	#多次赋值，并不会多次取随机数，挺有趣：	
	skf=StratifiedKFold(data.label, n_folds=4)
	
	#2 classes:
	n_classes=len(np.unique(data.label))
	
	#4 classifiers:
	classifiers=dict((covar_type, GMM(n_components=n_classes,
					covariance_type=covar_type, init_params='wc', n_iter=20))
					#for covar_type in ['spherical', 'diag', 'tied', 'full'])
					for covar_type in covars)
	
	for idx, (name, classifier) in enumerate(sorted(classifiers.items())):
#		train_index, test_index=next(iter(skf))
#		print('======================================')
		train_res=[]
		test_res=[]
		for train_index, test_index in skf:
			x_train=data.feature[train_index]
			y_train=data.label[train_index]
			x_test=data.feature[test_index]
			y_test=data.label[test_index]

			#2D, [2*115]:
			classifier.means_=np.array([x_train[y_train==i].mean(axis=0) for i in range(n_classes)])
			classifier.fit(x_train)
			
			train_pred=classifier.predict(x_train)
			train_accuracy=np.mean(train_pred==y_train)*100
			train_res.append(train_accuracy)
#			print('---------------train_accuracy +%s:'%name, train_accuracy)

			test_pred=classifier.predict(x_test)
			test_accuracy=np.mean(test_pred==y_test)*100
			test_res.append(test_accuracy)
#			print('------------test_accuracy:', test_accuracy)
		train_meanAccuracy=np.array(train_res).mean()
		test_meanAccuracy=np.array(test_res).mean()
		print('train_meanAccuracy, test_meanAccuracy\t\t +%s\t\t'%name, train_meanAccuracy, test_meanAccuracy)


def main():
	dri=loadFeatures()
#	print(type(dri))	#outputs: <type 'instance'> 奇怪
	#print(dri.label)
	#print(dri.feature)
#	print(dri.actType)
	
	covars=['spherical', 'diag', 'tied', 'full']
	trainAndPredWithCovars(data=dri, covars=covars)

	actTypes=np.unique(dri.actType)
#	driAcc=
#	for label, feature, type in dri:
#		print('label, feature, type:', label, feature, type)
#		if type is actTypes[0]:
	
	#目前 3种：
	for i in range(actTypes.size):
		print('============================'+actTypes[i])
		driSubType=dri[dri.actType==actTypes[i]]
#		print('driSubType:', driSubType.label, driSubType.feature, driSubType.actType)
		trainAndPredWithCovars(driSubType, covars)



if __name__=='__main__':
	main()
	
	
