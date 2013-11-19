#coding=utf8
from lxml import etree
import os, sys
sys.path.append('..')
from utils import Utils, Keys, LPF
from pylab import *

#parse old styled xml file, returns a dict whose keys in utils.Keys
def parseXml2dic(fname):
	psr = etree.XMLParser(remove_blank_text=True)
	tree=etree.parse(fname, psr)
	rt=tree.getroot()
	#旧格式
	if rt.tag==Keys.kRoot :
		nodeNode=rt[0][0]
		dic={}
		for dataNode in nodeNode:
			for k, v in dataNode.attrib.items():
				if not dic.get(k):
					dic[k]=[]
				dic[k].append(v)
		#to np.ndarray:
		for k, v in dic.items():
			dic[k]=np.array(map(float, v))
		return dic
	return None
	pass

#由dic计算world frame acc
def getAccWf(dic):
	dataCnt=len(dic[Keys.kAx])
	#print('dataCnt:', dataCnt)
	accWfList=[]
	for i in range(dataCnt):

		rotationVector=[
			dic[Keys.kRx][i],
			dic[Keys.kRy][i],
			dic[Keys.kRz][i]
			]
		
		#in body frame
		accVector=[
			dic[Keys.kAx][i],
			dic[Keys.kAy][i],
			dic[Keys.kAz][i]
			]
		
		rotationMatrix=Utils.getRotationMatrixFromVector(rotationVector)
		accWfVector=Utils.preMultiplyMV3(rotationMatrix, accVector)		
		accWfList.append(accWfVector)

	accWfList=np.array(accWfList).T
	return accWfList
	pass

#pub数据做测试时， 解析 groundtruth 文件， 返回dic
def getGroundtruth(fname):
	res={}
	with open(fname) as f:
		lines=[l.strip() for l in f.readlines()]
		for line in lines:
			if line == '':
				continue
			k, v=line.split()
			v=int(v)
			res[k]=v
	return res
	pass

#PARAMS gfname: groundtruth 配置文件， stepsDic: 算法得到的计步 dict
def printError(gfname, stepsDic):
	gtdic=getGroundtruth(gfname)
	#print gtdic
	errors=[]
	for k, v in stepsDic.items():
		eid=k.split('_')[0]
		if gtdic.get(eid) != None:
			gtv=gtdic[eid]
		else:
			gtv=1000000
		err=abs(gtv-v)*100./gtv
		#99.9% 不输出：
		if err<99:
			print '%s\t\t%d\t%d\t%.2f%%'%(k, gtv, v, err)
			errors.append(err)
	print "average error:%.2f%%"%average(array(errors))
	pass
