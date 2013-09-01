# -*- coding: utf-8 -*-

import os, sys, time, glob
from utils import Keys
from lxml import etree

folderPath=raw_input("input the xml files folder:\n")
folderPath=folderPath if folderPath !='' else r'D:\Documents\Desktop\aaa'
if not os.path.isdir(folderPath):
	sys.exit("%s is not a valid path, terminating~~"%folderPath)
os.chdir(folderPath)
print os.getcwd()

import numpy as np

def wrapNdarray(arr):
	return arr if isinstance(arr, np.ndarray) else np.array(arr)

oldRootTag='CaptureSession'
newRootTag='session'

xmlFileList=glob.glob('*.xml')
psr=etree.XMLParser(remove_blank_text=True)
for idx, fname in enumerate(xmlFileList):
	tree=etree.parse(fname, parser=psr)
	root=tree.getroot()
	print(root.tag, fname)
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
		tsList=[]
		fidxList=[]
		for idx, f in enumerate(frameList):
			ts=float(f.find(Keys.kTime).text)
			tsList.append(ts)
			frameIdx=float(f.find(Keys.kIndex).text)
			fidxList.append(frameIdx)
		assert np.argsort(tsList).tolist() == np.argsort(fidxList).tolist()
		print fname, cname, "\tts & frame-index order is correct"
