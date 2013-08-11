#coding=utf-8
'''
Created on May 21, 2013

@author: zhangxaochen
'''
import math

class Utils:
	@staticmethod
	def multiplyMV3(mat, vector):
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
	
	
	
	
		
