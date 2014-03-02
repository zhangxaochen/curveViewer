#coding=utf-8

r'''
	Created on Aug 9, 2013
	@author: zhangxaochen

	xml 格式向后兼容
	时间戳对齐，固定采样频率，并输出两种格式xml：
	用法：
		python <thisScriptPath>\xmlBackCompat.py <xmlFolderPath> [rate] [kind: linear | cubic] [style: old | new]
		<xmlFolderPath>	存放新格式xml数据的文件夹
		rate			插值频率，数值型，默认 30(Hz)
		kind			插值方法，字符串型，可选 linear 或 cubic，默认 linear
		style			输出格式，字符串型，可选 old 或 new，默认 old
		
		e.g.
			python C:\xmlBackCompat.py C:\xmlFolder 100 cubic new

	输出位置：
		<xmlFolderPath>\<style>-<kind>
		e.g.
			C:\xmlFolder\new-cubic
		
'''

import glob
import os, sys
import random
import time
import numpy as np
#import xml.etree.ElementTree as ET
from lxml import etree
from scipy.interpolate import interp1d
from pylab import *

from utils import Keys


oldRootTag=Keys.kRoot
newRootTag=Keys.kSession

strOld='old'
strNew='new'

strLinear='linear'
strCubic='cubic'

rate=30
interpKind=strLinear
style=strOld

def main():
	global rate
	global interpKind
	global style
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
	if len(sys.argv)>4:
		style=sys.argv[4]

	if not os.path.isdir(folder):
		sys.exit("%s is not a valid path, terminating~~"%folder)
	if interpKind != strLinear and interpKind != strCubic:
		sys.exit('interpKind must be *%s* or *%s*, terminating~~'%(strLinear, strCubic) )
	if style != strOld and style != strNew :
		sys.exit('style must be *%s* or *%s*, terminating~~'%(strOld, strNew) )

	
	os.chdir(folder)
	xmlFileList=glob.glob("*.xml")
	print(xmlFileList)
	
	#----------------对每个文件：
	for idx, fname in enumerate(xmlFileList):
		print('================fname:', fname)

		begTiming=time.time()
		data=loadFile(fname)
		if data==None:
			continue
		# print('data,', data)
		print('[[[loadFile() takes: %f'%(time.time()-begTiming))
		
		#-----------------interpData shape is {t:[], a:[ array([...]),[],[] ], g:[ [],[],[] ], m.. r.. }
		begTiming=time.time()
		interpData=getInterpData(data, rate)
		print('[[[getInterpData() takes: %f'%(time.time()-begTiming))

		if style == strOld:
			begTiming=time.time()
			tree=getOldStyleElementTree(interpData)
			print('[[[getOldStyleElementTree() takes: %f'%(time.time()-begTiming))
		elif style == strNew:
			# assert False	#还没实现
			begTiming=time.time()
			tree=getNewStyleElementTree(interpData)
			print('[[[getNewStyleElementTree() takes: %f'%(time.time()-begTiming))
		else:
			print('Holy shit! What happened?? ')
			


		newFolder=folder+os.sep+style+'-'+interpKind
		if not os.path.exists(newFolder):
			os.makedirs(newFolder)
		newPath=newFolder+os.sep+fname

		begTiming=time.time()
		# tree.write(newPath, pretty_print=True, xml_declaration=True, encoding='utf-8')
		#为避免 tree.write 再把乱码转为汉字， 直接用 file.write：
		xmlStr=etree.tostring(tree, pretty_print=True, xml_declaration=True, encoding='utf-8').decode()
		ff=open(newPath, 'w')
		ff.write(xmlStr)
		ff.close()
		
		print('[[[tree.write() takes: %f'%(time.time()-begTiming))


def getOldStyleElementTree(interpData):
	'''
	PARAMS
		interpData: a dict,  shape is {t:[], a:[ array([...]),[],[] ], g:[ [],[],[] ], m.. r.. }
	RETURN 
		tree: an OLD style etree.ElementTree instance
	'''

	newTimeList=interpData[Keys.kTime]
	oldRoot=etree.Element(Keys.kRoot)
	childNodes=etree.SubElement(oldRoot, Keys.kNodes)
	childNode=etree.SubElement(childNodes, Keys.kNode, 
						attrib={Keys.kFrames:'%d'%len(newTimeList), Keys.kPhyId:'1'})
	for idx, ts in enumerate(newTimeList):
		attribs={}
		
		#转换为毫秒：
		attribs[Keys.kTs]=str(ts*1000)
		
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
	
	return etree.ElementTree(oldRoot)


#
def getNewStyleEtreeFromNewData(data):
	'''
	与 getNewStyleElementTree 参数不同， 接收参数与 loadFile 的返回值一致
	
	Params
	---------------
	data:  shape is {Keys.kA:np.ndarray([[t, x,y,z], ..., [t, x,y,z]]), Keys.kG:...,  Keys.kM:...,  Keys.kR:...}, if not data xml, return None
	
	Returns
	---------------
	tree: a NEW style etree.ElementTree instance
	'''
	
	pass

#

def getNewStyleElementTree(interpData):
	'''
	PARAMS
		interpData: a dict,  shape is {t:[], a:[ array([...]),[],[] ], g:[ [],[],[] ], m.. r.. }
	RETURN 
		tree: a NEW style etree.ElementTree instance
	'''
	
	#newTimeList:
	ts=interpData[Keys.kTime]

	root=etree.Element(Keys.kSession)
	#---------------root's children
	begTimeNode=etree.SubElement(root, Keys.kBeginTime)
	begTimeNode.text=str(ts[0])
	
	endTimeNode=etree.SubElement(root, Keys.kEndTime)
	endTimeNode.text=str(ts[-1])
	
	threadCountNode=etree.SubElement(root, Keys.kThreadCount)
	threadCountNode.text=str(1)	#手机只算一个节点
	
	threadsNode=etree.SubElement(root, Keys.kThreads)
	
	#------------------threadsNode' children
	threadNode=etree.SubElement(threadsNode, Keys.kThread)
	
	#------------------threadNode' children
	threadNameNode=etree.SubElement(threadNode, Keys.kName)
	threadNameNode.text='1'	#namely, phyID
	
	channelCountNode=etree.SubElement(threadNode, Keys.kChannelCount)
	channelCountNode.text='4'	#a, g, m, r
	
	channelsNode=etree.SubElement(threadNode, Keys.kChannels)
	
	#------------------channelsNode' children
	ckeys=[Keys.kA, Keys.kG, Keys.kM, Keys.kR]
	for cname in ckeys:
		channelNode=etree.SubElement(channelsNode, Keys.kChannel)
		#------------------channelNode' children
		channelNameNode=etree.SubElement(channelNode, Keys.kName)
		channelNameNode.text=cname
		
		frameCountNode=etree.SubElement(channelNode, Keys.kFrameCount)
		frameCountNode.text=str(len(ts))
		
		framesNode=etree.SubElement(channelNode, Keys.kFrames)
		
		#------------------framesNode' children
		chanData=interpData[cname]
		for i in range(len(ts)):
			frameNode=etree.SubElement(framesNode, Keys.kFrame)
			
			#------------------frameNode' children
			indexNode=etree.SubElement(frameNode, Keys.kIndex)
			indexNode.text=str(i)
			
			timeNode=etree.SubElement(frameNode, Keys.kTime)
			timeNode.text=str(ts[i])
			
			valueNode=etree.SubElement(frameNode, Keys.kValue)
			
			#------------------valueNode' children
			xNode=etree.SubElement(valueNode, Keys.kX)
			xNode.text=str(chanData[0][i])
			
			yNode=etree.SubElement(valueNode, Keys.kY)
			yNode.text=str(chanData[1][i])
			
			zNode=etree.SubElement(valueNode, Keys.kZ)
			zNode.text=str(chanData[2][i])
			
			if cname == Keys.kR:
				wNode=etree.SubElement(valueNode, Keys.kW)
				wNode.text=str(chanData[3][i])
			
	tree=etree.ElementTree(root)
	return tree
	
def loadOldXmlTree(root):
	'''
		PARAMS
			root: root of the xml tree
		RETURN 
			data:  shape is {Keys.kA:np.ndarray([[t, x,y,z], ..., [t, x,y,z]], Keys.kG:...,  Keys.kM:...,  Keys.kR:...}, t is in seconds
	'''

	#对手机传感器只有一个node：
	nodeNode=root[0][0]
	dic={}
	for dataNode in nodeNode:
		for k, v in dataNode.attrib.items():
			if not dic.get(k):
				dic[k]=[]
			dic[k].append(v)
	for k, v in dic.items():
		dic[k]=np.array([float(val) for val in v])
		
	res={}
	res[Keys.kA]=[]
	res[Keys.kG]=[]
	res[Keys.kM]=[]
	res[Keys.kR]=[]
	
	ts=[t/1000. for t in dic[Keys.kTs] ]
	ax=dic[Keys.kAx]
	ay=dic[Keys.kAy]
	az=dic[Keys.kAz]
	res[Keys.kA]=np.array([ts,ax, ay, az]).T
	
	gx=dic[Keys.kGx]
	gy=dic[Keys.kGy]
	gz=dic[Keys.kGz]
	res[Keys.kG]=np.array([ts, gx, gy, gz]).T
	
	mx=dic[Keys.kMx]
	my=dic[Keys.kMy]
	mz=dic[Keys.kMz]
	res[Keys.kM]=np.array([ts, mx, my, mz]).T
	
	rx=dic[Keys.kRx]
	ry=dic[Keys.kRy]
	rz=dic[Keys.kRz]
	rw=dic[Keys.kRw]
	res[Keys.kR]=np.array([ts, rx, ry, rz, rw]).T
	
	return res
	pass

def loadNewXmlTree(root):
	'''
		PARAMS
			root: root of the xml tree
		RETURN 
			data:  shape is {Keys.kA:np.ndarray([[t, x,y,z], ..., [t, x,y,z]], Keys.kG:...,  Keys.kM:...,  Keys.kR:...}
	'''
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
		# print('===========', len(frameList))
		valList=[]
		for idx, f in enumerate(frameList):
			ts=float(f.find(Keys.kTime).text)
			if idx is 0:
				# print('ts:', ts, type(ts))
				pass
				# continue
			# if idx in [i for i in range(10)]:	#学傻了
			# if idx in range(10):
				# continue	#去掉前十帧
			v=f.find(Keys.kValue)
			vx=float(v.find(Keys.kX).text)
			vy=float(v.find(Keys.kY).text)
			vz=float(v.find(Keys.kZ).text)
			
			#vw 不一定有意义，也不一定存在：
			if v.find(Keys.kW) is not None:
				vw=float(v.find(Keys.kW).text)
				valList.append([ts, vx, vy, vz, vw])
			else:
				# print('valList.append([ts, vx, vy, vz, ])')
				valList.append([ts, vx, vy, vz, ])
			# valList.append([ts, vx, vy, vz, vw])
			# data[cname]=np.array(valList)	#×, 低效， 应在循环外
		data[cname]=np.array(valList)
	return data
	pass
	
def loadFile(fname):
	'''
	PARAMS
		fname: xml file name
	RETURN 
		data:  shape is {Keys.kA:np.ndarray([[t, (w), x,y,z], ..., [t, (w), x,y,z]]), Keys.kG:...,  Keys.kM:...,  Keys.kR:...}, if not data xml, return None
	'''
	psr=etree.XMLParser(remove_blank_text=True)
	tree=etree.parse(fname, parser=psr, )
	root=tree.getroot()
	#print(root.tag, root.tag is oldRootTag, type(root.tag))
	print(root.tag)
	if root.tag == oldRootTag :
		print('++++++++old style xml (CaptureSession)')
		data=loadOldXmlTree(root)
		return data
	elif root.tag == newRootTag :
		data=loadNewXmlTree(root)
		return data
	else:
	# if root.tag != newRootTag :
		# assert False, '-----------probably wrong xml folder'
		print('-----------probably wrong xml folder')
		return None
	

def getInterpData(data, rate):
	'''
	PARAMS
		data:  shape is {Keys.kA:np.ndarray([[t, x,y,z], ..., [t, x,y,z]], Keys.kG:...,  Keys.kM:...,  Keys.kR:...}
	RETURN
		interpData: a dict,  shape is {t:[], a:[ array([...]),[],[] ], g:[ [],[],[] ], m.. r.. }
	'''
	# global rate
	startTime=max(float(v[0][0]) for _,v in data.items())
	stopTime=min(float(v[-1][0]) for _,v in data.items())
	print('startTime:', startTime, [float(v[0][0]) for _,v in data.items()], )
	print('stopTime:', stopTime, [float(v[-1][0]) for _,v in data.items()], )
	
	newTimeList=np.arange(startTime, stopTime, 1.0/rate)

	interpData={Keys.kTime:[], Keys.kA:[], Keys.kG:[], Keys.kM:[], Keys.kR:[]}
	interpData[Keys.kTime]=newTimeList
	for k, v in data.items():
		for i in range(1, 4):
			#插值前时间戳&数据：
			oldTime=v[:, 0]
			# print('oldTime, newTimeList:', oldTime[-1], newTimeList[-1])
			# print('oldTime:', oldTime.shape, data[Keys.kA].shape)
			oldData=v[:, i]
			#print('oldData:', oldData)
			f=interp1d(oldTime, oldData, kind=interpKind)
			
			newData=f(newTimeList)
			#print('newData:', newData)
			interpData[k].append(newData)
		

	#计算 Rw, 放在第四行：
	d=interpData[Keys.kR]
	tmp=1-(d[0]**2+d[1]**2+d[2]**2)
	# tmp=tmp**0.5 if (tmp>0).all() else np.zeros(tmp.shape)		#×	别全 zeros
	tmp=np.array([i**0.5 if i>0 else 0  for i in tmp])
	interpData[Keys.kR].append(tmp)
	
	#DEBUG: 画 Rw， 发现因第一帧导致龙格现象
	# key=Keys.kR
	# v=data[key]
	# rz=interpData[key][2]
	# cut=300
	# plot(newTimeList[:cut], rz[:cut], v[:cut,0], v[:cut, 3], 'go')
	# show()
	return interpData
	
	
if __name__=="__main__":
	main()
