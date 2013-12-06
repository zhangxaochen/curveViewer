#coding=utf-8

'''
2. 写个程序(语言不限), 命令行读入混合驾驶数据xml和一个txt文件, 输入的txt里只有一行, 里面有空格分隔的两个数值, 表示对应xml文件的驾驶的起始和结束时间. 输出txt文件, 多行, 每行3个值, 空格分隔, 分别是label, begin time, end time. label有2种, 0表示加/减速, 1表示转弯. 要求把所有加/减速和转弯区间找出来, 不同类别的区间之间允许(注意是允许, 但不要求一定能检测出所有重叠区间, 这个条件是为了降低编程难度)重叠, 即加速的同时可以转弯. 方法是用加速度和陀螺仪阈值, 阈值自己手工调. 要求找出的区间尽可能正确, 即宁缺毋滥. 使用阈值找区间必然会遇到不连续的问题, 比如某个加速过程中某个时间点上的值小于阈值, 但是周围都是大于阈值的, 这种情况自己想办法处理. 尽量周一前弄好. 这个程序我也会自己写一个版本, 因为没有ground truth, 所以只好写两个程序对拍下. 程序在命令行的调用形式为: your-exe-or-py-file input-xml-path input-txt-path output-txt-path

我觉得不需要 input-txt-path？
目前调用形式:	your-exe-or-py-file input-xml-path output-txt-path
'''

import glob
import os, sys
import random
import time
import numpy as np
#import xml.etree.ElementTree as ET
from lxml import etree
from scipy.interpolate import interp1d
from getopt import getopt
from pylab import *

from utils import *
from xmlBackCompat import *
# from scUtils import *

#加（减）速：
labelAcc=0
#转弯：
labelTurn=1
debug=False

def labelData(data, label, winsz, th, debug):
	start=False
	left=right=-1
	lines=[]
	
	if debug:
		plot(data, 'b')
	for i in range(len(data)):
		if i+winsz>len(data):
			break
		win=data[i: i+winsz]
		delta=(win[-1]-win[0])/winsz
		if debug:
			scatter(i, delta*100, s=20, c='m')
		if delta>th and not start:
			start=True
			#若 i 不在上一段 (left, right) 区间：
			if i>right:
				# 若 right 非初始状态，即赋过值了:
				if right!=-1:
					if debug:
						axvline(right, c='y', lw=2)
					lines.append('%d %d %d\n'%(label, left, right) )
				
				left=i
				if debug:
					axvline(left, c='r', lw=2)
				
			# axvline(left, c='r')
		elif delta<th and start:
			start=False
			right=i+winsz
			# axvline(right, c='y')
	if lines==[] and right>left:
		if debug:
			axvline(right, c='y')
		lines.append('%d %d %d\n'%(label, left, right) )
	return lines
	pass

def main():
	# print(sys.argv)
	# assert len(sys.argv)>2
	fname=sys.argv[1] if len(sys.argv)>1 else None
	outfname=sys.argv[2] if len(sys.argv)>2 else None
	if fname==None:
		fname=r'D:\Administrator\Desktop\=huaweiproj-driving\taxi1011_a2_0.xml'
	if outfname==None:
		outfname='shit.x'
	
	outf=open(outfname, 'w')
	
	#获得旧xml格式tree， 截取自 xmlBackCompat.py：
	psr=etree.XMLParser(remove_blank_text=True)
	tree=etree.parse(fname, parser=psr, )
	root=tree.getroot()
	data=loadNewXmlTree(root)
	rate=30
	interpKind='linear'
	#先线性插值成 30fps ：
	interpData=getInterpData(data, rate)
	tree=getOldStyleElementTree(interpData)
	
	#获得数据dict， 截取自 scUtils.py：
	rt=tree.getroot()
	nodeNode=rt[0][0]
	dic={}
	for dataNode in nodeNode:
		for k, v in dataNode.attrib.items():
			if not dic.get(k):
				dic[k]=[]
			dic[k].append(v)
	#to np.ndarray:
	for k, v in dic.items():
		dic[k]=np.array([float(i) for i in v])
	
	# print(dic[Keys.kTs][-1])
	
	#获得 accWf, vWF， gyroWF, angleWF..., 截取自 main2.py:
	accWf=getAccWF(dic)
	# print(accWf)
	tsList=dic[Keys.kTs] if dic.get(Keys.kTs) != None else dic[Keys.kTimestamp]
	vWF=getVWF(accWf, tsList)
	gyroWF=getGyroWF(dic)
	angleWF=getAngleWF(gyroWF, tsList)
	
	#滑动窗口设为FPS：
	winsz=rate
	#delta vxy threshold:
	dvTh=0.005
	#根据 vxyWF 判断加减速， 根据窗口内 (win[-1]-win[0])/winsz 大小
	vxyWF=vWF[3]
	lines=labelData(vxyWF, labelAcc, winsz, dvTh, debug)
	print('---------------acc + dec:')
	for l in lines:
		print(l)
	outf.writelines(lines)
		
	#根据 angzwf 判断转弯， 根据窗口内 (win[-1]-win[0])/winsz 大小
	angzwf=abs(angleWF[2])
	if debug:
		plot(angzwf, 'g')

	winsz=rate
	#delta angle threshold
	dAngTh=0.005
	lines=labelData(angzwf, labelTurn, winsz, dAngTh, debug)
	print('---------------turn:')
	for l in lines:
		print(l)
	outf.writelines(lines)
	
	outf.close()
	show()
	pass

if __name__=='__main__':
	main()
	pass
