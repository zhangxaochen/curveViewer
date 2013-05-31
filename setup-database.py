#coding=utf-8

'''
输入包含驾驶数据 xml 的 folder 路径，
将数据导入数据库 dbo.drivingData

Usage: python setup-database folderPath
'''

import os, sys
from lxml import etree
import pyodbc

print( sys.argv, len(sys.argv))

helpInfo="""
Usage: python setup-database folderPath
"""

opID=[11,		#Duan Liang
			12	#Liu Bingzhen
			]
carID=[1,		#蒙迪欧
			2,		#福克斯
			]
activityID=dict(
			accelerate=28,
			decelerate=29,
			turn=		30,
			)
			
opAndCar=dict(
			d1=(opID[0], carID[0]),
			d2=(opID[0], carID[0]),
			d10=(opID[0], carID[1]),
			l1=(opID[1], carID[0]),
			l2=(opID[1], carID[1]),
			)


def main():
	if len(sys.argv)<2:
		print('error: len(sys.argv)<2')
		print(helpInfo)
		return
	
	folder=sys.argv[1]
	if not os.path.exists(folder):
		print('error: not os.path.exists(folder)')
		print(helpInfo)
		return
	
	os.chdir(folder)
			
	import glob
	fileList=glob.glob('*.xml')
	print('fileList:', len(fileList), fileList)
	
	fileFramesInfo={}
	configFile=open('config.txt')
	for line in configFile.readlines():
		fileAndFrame=line.split()
		# print(fileAndFrame)
		startEndList=list(map(int, fileAndFrame[1:]))
		if not fileFramesInfo.get(fileAndFrame[0]):
			fileFramesInfo[fileAndFrame[0]]=[startEndList]	#注意： 二维数组
		else:
			fileFramesInfo[fileAndFrame[0]].append(startEndList)
	
	print('+++++++++fileFramesInfo is:', fileFramesInfo)
	# return
	
	conn=pyodbc.connect('driver={sql server}; server=10.12.34.98; database=HuaweiProjectSensorDB; uid=zc; pwd=Capg11207')
	cur=conn.cursor()
	
	#对每个文件：
	for fname in fileList:
		basename=os.path.basename(fname)
		basename=os.path.splitext(basename)[0]
		driveInfo=basename.split('_')
		opId, carId=opAndCar.get(driveInfo[1])
		actId=activityID.get(driveInfo[3])
		
		for nodeID, totalFrames, nodeXml in parseXmlFile(fname):
			#如果 config.txt 里没有某 fileName， 说明没分割它， 可能它是坏文件， 跳过它：
			if not fileFramesInfo.get(basename):
				print('~~~~~~~break, basename is:', basename)
				break
			startFrame, endFrame=fileFramesInfo[basename][nodeID]
			
			# nodeXml 要转换 bytes --> string
			# print('======nodeXml:',nodeXml)
			# nodeXml="<node><data/></node>"
			# cur.execute("insert into dba.pyodbcTest(data) values('%s')"%nodeXml)
			# cur.commit()
			# return
			
			#看看变量类型是否都对：
			# print([nodeXml, actId, opId, carId, startFrame, endFrame, totalFrames, fname, nodeID])
			
			cur.execute("""insert into dbo.drivingData
			(data, activityID, operatorID, carID, startFrame, endFrame, totalFrames, fileName, nodeID) 
			values('%s', %d, %d, %d, %d, %d, %d, '%s', %d)
			"""%(nodeXml, actId, opId, carId, startFrame, endFrame, totalFrames, fname, nodeID) )
		
	# cur.commit()
	conn.commit()
	conn.close()
#		nodeID, nodeXml=parseXmlFile(fname)
#		print(parseXmlFile(fname))
		
			
def parseXmlFile(fname):
	tree = etree.parse(source=fname)
	#captureSession
	eRoot = tree.getroot()
	#nodes NODE
	eNodes = eRoot[0]
	#对每个 node：
	for nodeId, eNode in enumerate(eNodes):
		# print('==========', idx, eNode, etree.tostring(eNode))
		totalFrames=eNode.get('frames')
		
		yield nodeId, int(totalFrames), bytes.decode(etree.tostring(eNode))
		
		#对每个 Data 节点：
#		for eData in eNode:
#			pass
			
	


if __name__=='__main__':
	main()
	
	#单元测试：
#	fname=r'E:\workspace\PyCeshi\curveViewer\ttt.xml'
#	for i in parseXmlFile(fname):
#		print(i)
		
