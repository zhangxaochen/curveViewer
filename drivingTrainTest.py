#coding=utf-8

'''
使用 GMM 训练并预测驾驶数据
'''

#import os, sys, glob
import numpy as np
import pylab as pl
import matplotlib as mpl


from sklearn.cross_validation import StratifiedKFold
from sklearn.mixture import GMM

colors='rg'

def make_ellipses(gmm, ax):
	for n, color in enumerate(colors):
		v, w = np.linalg.eigh(gmm._get_covars()[n][:2, :2])
		u = w[0] / np.linalg.norm(w[0])
		angle = np.arctan2(u[1], u[0])
		angle = 180 * angle / np.pi  # convert to degrees
		v *= 9
		ell = mpl.patches.Ellipse(gmm.means_[n, :2], v[0], v[1],
								  180 + angle, color=color)
		ell.set_clip_box(ax.bbox)
		ell.set_alpha(0.5)
		ax.add_artist(ell)


class Driving:
	label=np.array([])
	labelName=np.array([])
	
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
		res.labelName=self.labelName
		res.feature=self.feature[npArray]
		res.actType=self.actType[npArray]
		return res
	
def loadFeatures():
#	configFname='D:/Documents/Desktop/huaweiproj-data-20130517/afterSplit/config_features.txt'
	configFname='./driving_features.txt'
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
		#acc, dec, turn: 
		actType.append(info[3])
	
	driving=Driving()
	driving.label=np.array(label)			#label 即 person 编号
	driving.labelName=np.array(['Duan', 'Liu'])
	driving.feature = np.array(feature)
	driving.actType=np.array(actType)
	
	return driving

def trainAndPredWithCovars(data, covars, xylim):
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
	n_classifiers=len(classifiers)
	pl.figure(figsize=[3*n_classifiers/2, 6])
	pl.subplots_adjust(bottom=.01, top=.95, hspace=.15, wspace=.05, left=.01, right=.99)
	
	#4 classifiers:
	for idx, (name, classifier) in enumerate(sorted(classifiers.items())):
#		print('======================================')

		h=pl.subplot(2, n_classifiers/2, idx+1)
		
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
		
		make_ellipses(classifier, h)
		#画图：
		for n, color in enumerate(colors):
			testerData=data.feature[data.label==n]
			pl.scatter(testerData[:, 0], testerData[:, 1], s=10, color=color, label=data.labelName[n])
			
		for n, color in enumerate('mb'):
			testerData=x_test[y_test==n]
			pl.plot(testerData[:,0], testerData[:, 1], 'x', color=color)

		pl.text(.05, .9, 'Train mean accuracy: %.1f'%train_meanAccuracy, transform=h.transAxes)
		pl.text(.05, .8, 'Test mean accuracy: %.1f'%test_meanAccuracy, transform=h.transAxes)
		
		pl.title(name)
		pl.xlim(xylim[:2])
		pl.ylim(xylim[2:])
#		pl.xticks(())
#		pl.yticks(())
		

	pl.gcf().canvas.set_window_title(data.actType[0])
	pl.show()


def main():
	dri=loadFeatures()
#	print(type(dri))	#outputs: <type 'instance'> 奇怪
	#print(dri.label)
	#print(dri.feature)
#	print(dri.actType)
	
	covars=['spherical', 'diag', 'tied', 'full']

	actTypes=np.unique(dri.actType)

	#合着训练，虽然结果不太坏，但是这么做不对：
#	trainAndPredWithCovars(data=dri, covars=covars)

	xylims=[
		[-5, 5, -15, 5],
		[-3, 1, -10, -2],
		[-3, 3, -12, 5],
		]
	#目前 3种动作：
	for i in range(actTypes.size):
		print('============================'+actTypes[i])
		driSubType=dri[dri.actType==actTypes[i]]
#		print('driSubType:', driSubType.label, driSubType.feature, driSubType.actType)
		trainAndPredWithCovars(driSubType, covars, xylim=xylims[i])

if __name__=='__main__':
	main()
	
	
