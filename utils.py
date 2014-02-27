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
		'''返回一维 data， 主要用于处理 加速度， 
		当加速度在 winsz 内稳定非零时， 认为此稳定值其实是静止状态下的偏移误差， 后续帧均减掉此偏移
		'''
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
	
	
# ====================从 main2.py 抽出来的：
#RETURN np.array of shape(4,n), x,y,z, w
def getRotationVector(xmlDic):
	res=[
			xmlDic[Keys.kRx],
			xmlDic[Keys.kRy],
			xmlDic[Keys.kRz],
			xmlDic[Keys.kRw],
			]
	return np.asarray(res)
	pass

#RETURN np.array of shape(5,n), [3]is gxyz, [4] is gxyz_lpf
def getGyroBF(xmlDic):
	gx=xmlDic[Keys.kGx]
	gy=xmlDic[Keys.kGy]
	gz=xmlDic[Keys.kGz]
	gxyz=(gx**2+gy**2+gz**2)**0.5
	lpf=LPF()
	gxyz_lpf=lpf.lpfTest(gxyz)

	res=[]
	res.append(gx)
	res.append(gy)
	res.append(gz)
	res.append(gxyz)
	res.append(gxyz_lpf)
	res=np.asanyarray(res)
	return res
	pass
	
#RETURN np.array of shape (3, n)
def getGyroWF(xmlDic):
	res=[]
	dic=xmlDic
	
	for i in range(len(dic[Keys.kAx])):
		rotationVector=[
			dic[Keys.kRx][i],
			dic[Keys.kRy][i],
			dic[Keys.kRz][i],
			]
		rotationMatrix=Utils.getRotationMatrixFromVector(rotationVector)
		gbfVector=[
			dic[Keys.kGx][i],
			dic[Keys.kGy][i],
			dic[Keys.kGz][i]
			]
		gwfVector=Utils.preMultiplyMV3(rotationMatrix, gbfVector)
		res.append(gwfVector)
	res=np.asanyarray(res).T
	return res
	pass

#gyroWF.shape==(3,n),	tsList is in epoch seconds
#RETURN  res of shape(4, n), [3] is angz_lpf
def getAngleWF(gyroWF, tsList):
	res=[]
	
	sum=np.zeros(3)
	res.append(sum.copy())
	for i in range(len(tsList)-1):
		dt=tsList[i+1]-tsList[i]
		if dt>1000:
			print('=======================dt>1000. dt, i are:', dt, i)
		dt=tsList[-1]-tsList[-2] if dt>1000 else dt
		#i 偏小， i+1 偏大； 
		sum+=gyroWF[:3, i]*dt/1000
		res.append(sum.copy())
	res=np.asanyarray(res).T
	lpf=LPF()
	angz_lpf=lpf.lpfTest(res[2])
	res=np.vstack((res, angz_lpf))
	return res
	pass

#RETURN np.array of shape(5,n), [3] is accXYZ, [4] is accXYZ_LPF
def getAccBF(xmlDic):
	res=[]
	res.append(xmlDic[Keys.kAx])
	res.append(xmlDic[Keys.kAy])
	res.append(xmlDic[Keys.kAz])
	accXYZ=(res[0]**2+res[1]**2+res[2]**2)**0.5
	res.append(accXYZ)
	lpf=LPF()
	accXYZ_LPF=lpf.lpfTest(accXYZ)
	res.append(accXYZ_LPF)
	res=np.asanyarray(res)
	return res
	pass

#RETURN np.array of shape(7, n), arr[3] is axyWF, [4] is azWF_LPF, [5] is axyzWF, [6] is arctan(ay/ax)
def getAccWF(xmlDic):
	res=[]
	dic=xmlDic
	
	for i in range(len(dic[Keys.kAx])):
		rotationVector=[
			dic[Keys.kRx][i],
			dic[Keys.kRy][i],
			dic[Keys.kRz][i],
			]
		rotationMatrix=Utils.getRotationMatrixFromVector(rotationVector)
		accVector=[
			dic[Keys.kAx][i],
			dic[Keys.kAy][i],
			dic[Keys.kAz][i]
			]
		accWfVector=Utils.preMultiplyMV3(rotationMatrix, accVector)
		# accWfVector=Utils.postMultiplyMV3(accVector, rotationMatrix)
		#AxyWF:
		t=accWfVector
		# t.append((t[0]**2+t[1]**2)**0.5)
		res.append(t)
	res=np.asanyarray(res).T
	res[2]-=9.80665
	
	# 这里做一个加速度修正校正补偿：
	for i in range(3):
		res[i]=Utils.calibrate(res[i])
	
	axyWF=(res[0]**2+res[1]**2)**0.5
	# res=np.vstack((res, axyWF))
	
	# AzWF_LPF:
	lpf=LPF()
	azWF_LPF=lpf.lpfTest(res[2])
	# res=np.vstack((res, azWF_LPF))
	
	#AxyzWF:
	axyzWF=(res[0]**2+res[1]**2+res[2]**2)**0.5
	# res=np.vstack((res, axyzWF))
	
	#arctan(y/x)
	arctanYX=np.arctan(1.0*res[1]/res[0])
	
	res=np.vstack((res, axyWF, azWF_LPF, axyzWF, arctanYX))
	
	return res
	pass

# accWF.shape==(6, n);	tsList is in epoch seconds
#RETURN res of shape (4, n), res[3]=vxyWF
def getVWF(accWF, tsList):
	res=[]
	
	# accWF=accWF.T
	print('accWF.shape:', accWF.shape)
	sum=np.zeros(3)
	res.append(sum.copy())
	
	#滑动窗口长：
	winsz=30
	#判定静止阈值：
	stillTh=0.01
	
	#虽然 i 从0开始， 但 res 此时从 1 开始：
	for i in range(len(tsList)-1):
		dt=tsList[i+1]-tsList[i]
		#第一帧时间戳的 bug
		if dt>1000:
			print('=======================dt>1000. dt, i are:', dt, i)
		dt=tsList[-1]-tsList[-2] if dt>1000 else dt
		#i 偏小， i+1 偏大； 
		# sum+=accWF[i][:3]*dt/1000
		sum+=accWF[:3, i]*dt/1000
		#看 axyzWF， 若平稳， 强制校正 v=0：
		if i+1+winsz<len(tsList) and (sum!=np.zeros(3)).any() :
			va=np.var(accWF[5][i+1:i+1+winsz])
			if va<stillTh:
				sum.fill(0)
		res.append(sum.copy())
	res=np.asanyarray(res).T
	# vxyWF:
	vxyWF=(res[0]**2+res[1]**2)**0.5
	res=np.vstack((res, vxyWF))
	return res
	pass

# vWF.shape==(3, n), tsList is in epoch seconds
def getDWF(vWF, tsList):
	res=[]
	sum=np.zeros(3)
	res.append(sum.copy())
	for i in range(len(tsList)-1):
		dt=tsList[i+1]-tsList[i]
		dt=tsList[-1]-tsList[-2] if dt>1000 else dt
		sum+=vWF[:3, i]*dt/1000
		res.append(sum.copy())
	res=np.asanyarray(res).T
	return res
	pass
