#coding=utf-8
'''
Created on Apr 17, 2013

@author: zhangxaochen
'''
from glob import glob
#import xml.etree.ElementTree as et
import os
from lxml import etree

def main():
	pathTo='./segmented/'
	testFile='ttt.xml'
	testOut='pretty-ttt.xml'
	
	if not os.path.exists(pathTo):
		return
	os.chdir(pathTo)
	
	parser = etree.XMLParser(remove_blank_text=True)
	tree=etree.parse(testFile, parser)
	root=tree.getroot()	#不用
	print(str(etree.tostring(tree, pretty_print=True)))
	fout=open(testOut, 'wb')
	fout.write(etree.tostring(root, pretty_print=True))
	fout.close()
	
	
	fileList=glob('*.xml')
	

if __name__ == '__main__':
	main()