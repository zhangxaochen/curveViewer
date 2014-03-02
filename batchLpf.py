#coding=utf-8
import os, sys
from glob import glob
from lxml import etree
import numpy as np
from xmlBackCompat import loadFile, loadNewXmlTree
from utils import Keys, LPF
import batchLpfConfig as cfg

def toNewFile(oldfname, newfname):
	'''
	�� xml �ļ��� �� LPF�� ���
	
	Params
	---------------
	oldfname: Ҫ������ļ��� �����Ǿ���·��
	newfname: Ҫ���ɵ��ļ��� �����Ǿ���·���� ���·���а��������ڵ��ļ��У� ���½�֮
	
	Returns
	---------------
	None
	'''
	
	assert os.path.isfile(oldfname), "'oldfname' must be a existing file name~~~"
	
	# data = loadFile(oldfname)
	
	psr=etree.XMLParser(remove_blank_text=True)
	tree=etree.parse(oldfname, parser=psr, )
	root=tree.getroot()
	data=loadNewXmlTree(root)
	# print '-----', data['g'].shape
	# print np.any(data['g'][:, 4]) #Ӧ�� False, w ȫ��
	lpf=LPF()
	#��ָ���� a,g,m,r �˲��� �� data ԭ�ظ���
	for k in cfg.sensors:
		#transposed data correspond to k, it's a view, not a copy
		dtran=data[k].T
		for i in range(1, 4):
			dtran[i]=lpf.lpfScipy(dtran[i], cfg.winsz)
	
	#�� loadNewXmlTree ��������
	
	threadList=root.find(Keys.kThreads).findall(Keys.kThread)
	#========�ֻ�ֻ��һ���ڵ�
	assert len(threadList) is 1
	thread=threadList[0]
	channelList=thread.find(Keys.kChannels).findall(Keys.kChannel)
	for c in channelList:
		cname=c.find(Keys.kName).text
		if cname not in cfg.sensors:
			continue
		frameList=c.find(Keys.kFrames).findall(Keys.kFrame)
		#������ʱ�ò��� idx:
		for idx, frame in enumerate(frameList):
			v=frame.find(Keys.kValue)
			v.find(Keys.kX).text=str(data[cname][idx][1])
			v.find(Keys.kY).text=str(data[cname][idx][2])
			v.find(Keys.kZ).text=str(data[cname][idx][3])
	
	# ntree=etree.ElementTree(root)
	xmlStr=etree.tostring(tree, pretty_print=True, xml_declaration=True, encoding='utf-8')#.decode()
	
	#�����½�·����
	dir=os.path.dirname(newfname)
	if not os.path.exists(dir):
		os.makedirs(dir)
		
	with open(newfname, 'w') as nf:
		nf.write(xmlStr)
		
	pass


# loadFile()


def toNewDir(olddir, newdir):
	'''
	Params
	---------------
	olddir: Ҫ�������·���� Ӧ�ú����ֻ��ɼ����˶����� xml ����
	newdir: ���ɵ��ļ��ı���·���� �������ڣ� ���½�֮
	
	Returns
	---------------
	None
	'''
	assert os.path.isdir(olddir), "'olddir' must be an existing directory"
	os.chdir(olddir)
	# xmlfiles=os.path.join(olddir, '*.xml')
	xmlfiles=glob('*.xml')
	for fname in xmlfiles:
		toNewFile(fname, os.path.join(newdir, fname))
	pass
#




# ====================test=================
def tests():
	print('~~~~~~~testing toNewFile')
	ofn=r'D:\Documents\Desktop\t\ZC_a0_3.xml'
	nfn=r'D:\Documents\Desktop\t\shit.xml'
	toNewFile(ofn, nfn)

	print('~~~~~~~testing toNewDir')
	od=r'D:\Documents\Desktop\t'
	nd=r'D:\Documents\Desktop\t/shit'
	toNewDir(od, nd)
#
# tests()


if __name__=="__main__":
	toNewDir(cfg.olddir, cfg.newdir)
