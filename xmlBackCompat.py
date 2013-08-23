#coding=utf-8

'''
Created on Aug 9, 2013

@author: zhangxaochen

xml 格式向后兼容
输出旧格式xml：./oldStyle/*.xml
'''
import glob
import os
import sys
import random
import time
import numpy as np
#import xml.etree.ElementTree as ET
from lxml import etree
from scipy.interpolate import interp1d


from utils import Keys
from test.test_iterlen import len

oldRootTag='CaptureSession'
newRootTag='session'

rate=30
interpKind='linear'

def main():
	folder=None
	print(len(sys.argv), )
	if len(sys.argv)>1 :
		folder=sys.argv[1]
	print(folder)
	if folder is None:
		folder=input("input xml data containing folder:")
	if len(sys.argv)>2:
		rate=int(sys.argv[2])
	if len(sys.argv)>3:
		interpKind=sys.argv[3]
	
	os.chdir(folder)
	xmlFileList=glob.glob("*.xml")
	print(xmlFileList)
	
	psr=etree.XMLParser(remove_blank_text=True)
	#----------------对每个文件：
	for idx, fname in enumerate(xmlFileList):
		print('================fname:', fname)
		tree=etree.parse(fname, parser=psr, )
		root=tree.getroot()
#		print(root.tag, root.tag is oldRootTag, type(root.tag))
		print(root.tag)
		if root.tag == oldRootTag :
			print('++++++++old style xml (CaptureSession)')
			continue
		if root.tag != newRootTag :
			print('-----------probably wrong xml folder')
			continue
		
		threadList=root.find(Keys.kThreads).findall(Keys.kThread)
		#========手机只算一个节点
		assert len(threadList) is 1
		thread=threadList[0]
		channelList=thread.find(Keys.kChannels).findall(Keys.kChannel)
		assert len(channelList) is 4
		
		#data=dict(a=[], g=[], m=[], r=[])
		data={Keys.kA:[], Keys.kG:[], Keys.kM:[], Keys.kR:[]}
		#--------对每个传感器，目前 a, g, m, r：
		for c in channelList:
			cname=c.find(Keys.kName).text
			frameList=c.find(Keys.kFrames).findall(Keys.kFrame)
			#-------------对每一帧：
			valList=[]
			for idx, f in enumerate(frameList):
				time=float(f.find(Keys.kTime).text)
				if idx is 0:
					print('time:', time, type(time))
				v=f.find(Keys.kValue)
				vx=float(v.find(Keys.kX).text)
				vy=float(v.find(Keys.kY).text)
				vz=float(v.find(Keys.kZ).text)
				#vw 不一定有意义：
				vw=float(v.find(Keys.kW).text)
				
				valList.append([time, vx, vy, vz, vw])
				data[cname]=np.array(valList)
			
		startTime=max(float(v[0][0]) for _,v in data.items())
		stopTime=min(float(v[-1][0]) for _,v in data.items())
		print('startTime:', startTime, [float(v[0][0]) for _,v in data.items()], )
		print('stopTime:', stopTime, [float(v[-1][0]) for _,v in data.items()], )
		
		newTimeList=np.arange(startTime, stopTime, 1.0/rate)
		
		#-----------------interpData shape is {t:[], a:[ [],[],[] ], g:[ [],[],[] ], m.. r.. }
		interpData={Keys.kTime:[], Keys.kA:[], Keys.kG:[], Keys.kM:[], Keys.kR:[]}
		interpData[Keys.kTime]=newTimeList
		for k, v in data.items():
			for i in range(1, 4):
				#插值前时间戳&数据：
				oldTime=v[:, 0]
#				print('oldTime:', oldTime)
				oldData=v[:, i]
#				print('oldData:', oldData)
				f=interp1d(oldTime, oldData, kind=interpKind)
				
				newData=f(newTimeList)
#				print('newData:', newData)
				interpData[k].append(newData)
			
			#计算 Rw, 放在第四行：
			if k==Keys.kR:
				d=interpData[k]
				tmp=(1-(d[0]**2+d[1]**2+d[2]**2))**0.5
				interpData[k].append(tmp)
		
		oldRoot=etree.Element(Keys.kRoot)
		childNodes=etree.SubElement(oldRoot, Keys.kNodes)
		childNode=etree.SubElement(childNodes, Keys.kNode, 
							attrib={Keys.kFrames:'%d'%len(newTimeList), Keys.kPhyId:'1'})
		for idx, time in enumerate(newTimeList):
			attribs={}
			
			attribs[Keys.kTs]=str(time*1000)
			
			attribs[Keys.kAx]=str(interpData[Keys.kA][0][idx])
			attribs[Keys.kAy]=str(interpData[Keys.kA][1][idx])
			attribs[Keys.kAz]=str(interpData[Keys.kA][2][idx])
			
			attribs[Keys.kGx]=str(interpData[Keys.kG][0][idx])
			attribs[Keys.kGy]=str(interpData[Keys.kG][1][idx])
			attribs[Keys.kGz]=str(interpData[Keys.kG][2][idx])
			
			attribs[Keys.kMx]=str(interpData[Keys.kM][0][idx])
			attribs[Keys.kMy]=str(interpData[Keys.kM][1][idx])
			attribs[Keys.kMz]=str(interpData[Keys.kM][2][idx])
			
			attribs[Keys.kRx]=str(interpData[Keys.kR][0][idx])
			attribs[Keys.kRy]=str(interpData[Keys.kR][1][idx])
			attribs[Keys.kRz]=str(interpData[Keys.kR][2][idx])
			attribs[Keys.kRw]=str(interpData[Keys.kR][3][idx])
			
			childData=etree.SubElement(childNode, Keys.kData, attrib=attribs)
		
		tree=etree.ElementTree(oldRoot)
		newFolder=folder+os.sep+'oldStyle'
		if not os.path.exists(newFolder):
			os.makedirs(newFolder)
		newPath=newFolder+os.sep+fname
		tree.write(newPath, pretty_print=True)
		
				
			
		if idx is 0 :
			print(root)
		
		


if __name__=="__main__":
	main()
