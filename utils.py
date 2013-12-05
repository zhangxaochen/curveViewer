#coding=utf-8
'''
Created on May 21, 2013

@author: zhangxaochen
'''
import math
import scipy
from scipy import signal
import numpy as np

class LPF:
	
	WINSZ=10
	
	# newCurVal=p*oldVal+(1-p)*curVal
	# def myLpf(self, data, p):
		# res=[]
		# for i, v in enumerate(data):
			# if i==0:
				# res.append(v)
			# else:
				# res.append(data[i-1]*p+v*(1-p))
		# return res
	
	#http://stackoverflow.com/questions/17833119/lowpass-filter-in-python
	def lpfScipy(self, data, numtaps=WINSZ, cutoff=40, nyq=800):
		h=scipy.signal.firwin(numtaps=numtaps, cutoff=cutoff, nyq=nyq)
		return scipy.signal.lfilter(h, 1.0, data)
		pass
	pass
	
	# http://upload.wikimedia.org/math/b/9/5/b95a89c2b2957b11c2ba624680c8ffe1.png
	# http://en.wikipedia.org/wiki/Finite_impulse_response
	# zh.wikipedia.org/zh-cn/有限脉冲响应
	def lpfMine(self, data, numtaps=WINSZ, cutoff=40, nyq=800):
		'''
		手写lpf，同 lpfScipy 一样
		'''
		h=scipy.signal.firwin(numtaps=numtaps, cutoff=cutoff, nyq=nyq)
		
		N=len(h)
		res=[]
		for n, v in enumerate(data):
			y=0
			for i in range(N):
				if n<i:
					break
				y+=h[i]*data[n-i]
			res.append(y)
		return np.asanyarray(res)
		pass
		
	#开始 numtaps 一段不要太低
	def lpfTest(self, data, numtaps=WINSZ, cutoff=40, nyq=800):
		res=self.lpfScipy(data, numtaps, cutoff, nyq)
		# res[:numtaps]=[data[:i]/(i+1) for i in range(numtaps)]
		tmp=numtaps-1 if numtaps-1<len(res) else len(res)
		res[:tmp]=[np.mean(data[:i+1]) for i in range(tmp)]
		return res
		pass
	
	#感觉不好
	def lpfButter(self, data, N=8, Wn=0.125):
		b, a=signal.butter(N, Wn)
		y=signal.filtfilt(b, a, data, )
		return y

class Utils:
	@staticmethod
	def calibrate(data):
		# 信号偏移：
		drift=0
		#滑动窗口长：
		winsz=30
		#判定静止阈值：
		stillTh=0.01
		res=[]
		for i in range(len(data)):
			if i<winsz:
				res.append(data[i])
				continue
			va=np.var(data[i-winsz:i])
			if va<stillTh:
				drift=np.mean(data[i-winsz:i])
				# print 'drift', drift
				# break
			res.append(data[i]-drift)
		# res=np.asanyarray(data)-drift
		return np.asanyarray(res)
		pass
	
	@staticmethod
	#等价于 h=firwin(...)	√
	def getHammingWin(n):
		ham=[0.54-0.46*np.cos(2*np.pi*i/(n-1)) for i in range(n)]
		ham=np.asanyarray(ham)
		ham/=ham.sum()
		return ham
		pass
	
	@staticmethod
	# 当前点向前数 numtaps 个，逐帧求var
	# RETURN ndarray
	def getVarPrev(data, numtaps):
		res=[]
		for i in range(len(data)):
			if i<numtaps-1:
				# v=0
				v=np.var(data[:i+1])
			else:
				v=np.var(data[i-(numtaps-1):i+1])
			res.append(v)
		return np.asanyarray(res)
		pass
		
	@staticmethod
	# 当前点向前数 numtaps 个， 分段求var，返回阶梯序列
	# RETURN ndarray
	def getVarPrevStep(data, numtaps):
		assert type(numtaps)==int and numtaps>0, 'type(numtaps)==int and numtaps>0'
		res=[]
		buf=[]
		for i,v in enumerate(data):
			buf.append(v)
			if len(buf)==numtaps:
				va=np.var(buf)
				res.extend([va]*numtaps)
				del buf[:]
		return np.asanyarray(res)
		pass
		
	@staticmethod
	def maxMinVar(buf):
		max=min=buf[0]
		for v in buf:
			if v>max:
				max=v
			elif v<min:
				min=v
		return np.var([max, min])
		pass

	@staticmethod
	#当前点向前 numtaps区间内 max-min 的var，返回阶梯序列
	def getMmvarPrev(data, numtaps=LPF.WINSZ):
		assert type(numtaps)==int and numtaps>0, 'type(numtaps)==int and numtaps>0'
			
		res=[]
		buf=[]
		for i,v in enumerate(data):
			buf.append(v)
			if len(buf)==numtaps:
				va=Utils.maxMinVar(buf)
				res.extend([va]*numtaps)
				del buf[:]
		return np.asanyarray(res)
		pass
	
	@staticmethod
	# 当前点前后数 numtaps/2 个
	# RETURN ndarray
	def getVarMid(data, numtaps):
		res=[]
		winsz=numtaps if numtaps%2==1 else numtaps-1
		halfWin=round(numtaps/2.)
		for i in range(len(data)):
			if i<halfWin-1 or i>len(data)-halfWin:
				v=0
			else:
				v=np.var(data[i-(halfWin-1): i+(halfWin-1)])
			res.append(v)
		return np.asanyarray(res)
		pass
	
	@staticmethod
	def preMultiplyMV3(mat, vector):
		assert len(mat)==9 and len(vector)==3
		#防止list都是字符串list：
		mat=list(map(float, mat))
		vector=list(map(float, vector))
		
		res=[]
		for i in range(3):
			idx=3*i
			res.append(mat[idx] * vector[0] + mat[idx + 1] * vector[1] + mat[idx + 2] * vector[2])
			
		return res
	
	@staticmethod
	def postMultiplyMV3(vector, mat):
		assert len(mat)==9 and len(vector)==3
		#防止list都是字符串list：
		mat=list(map(float, mat))
		vector=list(map(float, vector))
		
		res=[]
		for i in range(3):
			# idx=3*i
			res.append(vector[0] * mat[i]+ vector[1] * mat[i+3]+ vector[2] * mat[i+6])
			
		return res

	@staticmethod
	def getRotationMatrixFromVector(rotationVector):
		'''reference: SensorManager.class & RotationMatrixView.java
		len(rotationVector)==4 is OK
		'''
		#防止list都是字符串list：
		rotationVector=list(map(float, rotationVector))

		q1 = rotationVector[0]
		q2 = rotationVector[1]
		q3 = rotationVector[2]
		if len(rotationVector)==4:
			q0=rotationVector[3]
		else:
			q0 = 1 - q1*q1 - q2*q2 - q3*q3
#			q0 = (q0 > 0) ? (float)Math.sqrt(q0) : 0
			q0=math.sqrt(q0) if q0>0 else 0
		
		sq_q1 = 2 * q1 * q1;
		sq_q2 = 2 * q2 * q2;
		sq_q3 = 2 * q3 * q3;
		q1_q2 = 2 * q1 * q2;
		q3_q0 = 2 * q3 * q0;
		q1_q3 = 2 * q1 * q3;
		q2_q0 = 2 * q2 * q0;
		q2_q3 = 2 * q2 * q3;
		q1_q0 = 2 * q1 * q0;
		
		R=[0]*9
		R[0] = 1 - sq_q2 - sq_q3;
		R[1] = q1_q2 - q3_q0;
		R[2] = q1_q3 + q2_q0;

		R[3] = q1_q2 + q3_q0;
		R[4] = 1 - sq_q1 - sq_q3;
		R[5] = q2_q3 - q1_q0;

		R[6] = q1_q3 - q2_q0;
		R[7] = q2_q3 + q1_q0;
		R[8] = 1 - sq_q1 - sq_q2;
		
		return R

class Keys:
	kRoot='CaptureSession'
	kNodes='Nodes'
	kPhyId='phyId'
	kNode='Node'
	kData='Data'
	
	kTs='ts'
	kTimestamp='timestamp'
	
	kAx='Ax'
	kAy='Ay'
	kAz='Az'
	
	kGx='Gx'
	kGy='Gy'
	kGz='Gz'
	
	kMx='Mx'
	kMy='My'
	kMz='Mz'
	
	kRw='Rw'
	kRx='Rx'
	kRy='Ry'
	kRz='Rz'
	
	#--------------------new style session
	kSession='session'
	kBeginTime='begin-time'
	kEndTime='end-time'
	kThreads='threads'
	kThreadCount='thread-count'
	kThread='thread'
	kName='name'
	kChannels='channels'
	kChannelCount='channel-count'
	kChannel='channel'
	kFrames='frames'
	kFrameCount='frame-count'
	kFrame='frame'
	kIndex='index'
	kTime='time'
	kValue='value'
	kW='w'
	kX='x'
	kY='y'
	kZ='z'
	kA='a'
	kG='g'
	kM='m'
	kR='r'
	
	
	
	
		
