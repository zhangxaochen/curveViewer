#coding=utf-8

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
carID=[1,		#�ɵ�ŷ
			2,		#����˹
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
			fileFramesInfo[fileAndFrame[0]]=[startEndList]	#ע�⣺ ��ά����
		else:
			fileFramesInfo[fileAndFrame[0]].append(startEndList)
	
	print('+++++++++fileFramesInfo is:', fileFramesInfo)
	# return
	
	conn=pyodbc.connect('driver={sql server}; server=10.12.34.98; database=HuaweiProjectSensorDB; uid=zc; pwd=Capg11207')
	cur=conn.cursor()
	
	#��ÿ���ļ���
	for fname in fileList:
		basename=os.path.basename(fname)
		basename=os.path.splitext(basename)[0]
		driveInfo=basename.split('_')
		opId, carId=opAndCar.get(driveInfo[1])
		actId=activityID.get(driveInfo[3])
		
		for nodeID, totalFrames, nodeXml in parseXmlFile(fname):
			#��� config.txt ��û��ĳ fileName�� ˵��û�ָ����� �������ǻ��ļ��� ��������
			if not fileFramesInfo.get(basename):
				print('~~~~~~~break, basename is:', basename)
				break
			startFrame, endFrame=fileFramesInfo[basename][nodeID]
			
			# nodeXml Ҫת�� bytes --> string
			# print('======nodeXml:',nodeXml)
			# nodeXml="<node><data/></node>"
			# cur.execute("insert into dba.pyodbcTest(data) values('%s')"%nodeXml)
			# cur.commit()
			# return
			
			#�������������Ƿ񶼶ԣ�
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
	#��ÿ�� node��
	for nodeId, eNode in enumerate(eNodes):
		# print('==========', idx, eNode, etree.tostring(eNode))
		totalFrames=eNode.get('frames')
		
		yield nodeId, int(totalFrames), bytes.decode(etree.tostring(eNode))
		
		#��ÿ�� Data �ڵ㣺
#		for eData in eNode:
#			pass
			
	


if __name__=='__main__':
	main()
	
	#��Ԫ���ԣ�
#	fname=r'E:\workspace\PyCeshi\curveViewer\ttt.xml'
#	for i in parseXmlFile(fname):
#		print(i)
		
