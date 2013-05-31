#coding=utf-8
'''
之前数据采集程序存的 xml 包含多个node， 
实际一个node 本应代表一个物理传感器节点，
此脚本用于将含有多个node的xml分割为多个只含一个node的xml

Usage: python splitXml folderPath
'''

import os, sys
from lxml import etree
from macpath import basename


helpInfo="""
Usage: python splitXml folderPath
"""

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
	pathTo='afterSplit'
	os.makedirs(pathTo, exist_ok=True)
	
	import glob
	fileList=glob.glob("*.xml")
	for fname in fileList:
		basename, ext=os.path.splitext(fname)
		
		tree=etree.parse(source=fname)
		eRoot=tree.getroot()
		eNodes=eRoot[0]
		
		newRoot=etree.Element('CaptureSession')
		newNodes=etree.SubElement(newRoot, 'Nodes')		
		
		for nodeId, eNode in enumerate(eNodes):
			newFilename=pathTo+os.path.sep+basename+'_%d'%nodeId+ext
			newFile=open(newFilename, 'w')
			
			newNodes.append(eNode)
			newFile.write(bytes.decode(etree.tostring(newRoot, pretty_print=True)))
			newFile.close()
			
			#清掉准备下一个 Node：
			newNodes.remove(eNode)
		
	
if __name__=="__main__":
	main()