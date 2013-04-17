#coding=utf-8
'''
Created on Apr 8, 2013

@author: zhangxaochen
'''
#from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from curveViewer_ui import *
import glob
import os
import random
import sys
import time
import xml.etree.ElementTree as ET
from lxml import etree
from xml.dom import minidom
import traceback
#from xml.etree.ElementTree import ElementTree

class Keys:
	kRoot='CaptureSession'
	kNodes='Nodes'
	kNode='Node'
	kData='Data'
	
	kTs='timestamp'
	
	kAx='Ax'
	kAy='Ay'
	kAz='Az'
	
	kGx='Gx'
	kGy='Gy'
	kGz='Gz'
	
	kMx='Mx'
	kMy='My'
	kMz='Mz'
	
	kRw='Rw'
	kRx='Rx'
	kRy='Ry'
	kRz='Rz'
	
#	xmlKeyList=[kTs, kAx, kAy, kAz, kGx, kGy, kGz, kMx, kMy, kMz, kRw, kRx, kRy, kRz]
	

class MyWidgetCurveView(QWidget):
	dataDictList=[]
	def __init__(self):
		super().__init__()
#		self.setMinimumWidth(1111)
#		print(self.width())
#		self.resize(self.width()*2, self.height())	#没用啊。尽管 width 变了
#		print(self.width())
		
	
	def paintEvent(self, event):
		print('paintEvent()', self.width())
		
		qp=QPainter(self)
		dLen=len(self.dataDictList)
		if(dLen==0):
			#qp.setPen(QColor(222,222,222,222).red())	#QtCore.Qt.red
			qp.setPen(QColor(Qt.red))
			qp.setFont(QFont('Decorative', 10))
			#qp.drawText(event.rect(), "str")
			size=self.size()
			for i in range(1000):
				x=random.randint(1, size.width()*2-1)
				y=random.randint(1, size.height()-1)
				qp.drawPoint(QPoint(x, y))
			
#			qp.drawPath()
			qp.drawEllipse(0, 0, 200, 100)	#左上角 0,0
		else:
#			print('dLen:=', dLen)
			axList=self.getAttribListFromKey(Keys.kAx)
#			tsList=self.getAttribListFromKey(Keys.kTs)
#			tsStart=tsList[0]
#			for i in range(len(tsList)):
#				tsList[i]-=tsStart
			
			
		
	def getAttribListFromKey(self, key):
		l=self.dataDictList
		res=[]
		for ddic in l:
			val=float(ddic[key])
			res.append(val)
		
		return res
	
	def drawPathUseList(self, lx, ly):
		
		pass
		
class MyWindow(QMainWindow):
	class XmlStuff(object):pass
	xmlDataList=[]
	
	def __init__(self, parent=None):
		super().__init__(parent)
		self.ui=Ui_MainWindow()
		self.ui.setupUi(self)

		self._canvas=self.ui.mplWidget.canvas
		self._canvas.resetAxis()
		
		self.fileItemMarkBg=Qt.green
		self.nodeItemMarkBg=Qt.yellow
#		ranNums=random.sample(range(100), 100)
#		self._canvas.ax.plot(ranNums)

		self._canvas.draw()
		
		self.xml=self.XmlStuff()

		#==================================xml test
		fname='E:/workspace/PyCeshi/curveViewer/ttt.xml'
		self.parseXmlFile(fname)
				
		#===================================信号槽
#		self.ui.listWidgetNode.itemChanged.connect(lambda x:print('the args: ', x))
#		self.ui.listWidgetNode.itemActivated.connect(lambda x:print('itemActivated, the args: ', x))	#要双击
#		self.ui.listWidgetNode.itemSelectionChanged.connect(self.onNodeItemSelectionChanged)
		self.ui.listWidgetNode.currentItemChanged.connect(self.onCurrentNodeItemChanged)
		self.ui.listWidgetFile.currentItemChanged.connect(self.onCurrentFileItemChanged)

		self._canvas.areaSelected.connect(self.onAxisAreaSelected)
	
	def onCurrentFileItemChanged(self, item):
		print('onCurrentFileItemChanged')
		baseName=item.text()
#		print(baseName)
#		absPath=self.dirName+os.sep+baseName	#√, 别手动拼接
		absPath=os.path.realpath(baseName)
		st=time.time()
		self.parseXmlFile(absPath)
		et=time.time()
		print('et-st:', et-st)		
		
		#顺便选中 node1
		node1=self.ui.listWidgetNode.item(0)
#		print('node1:', node1, node1.text())
#		self.ui.listWidgetNode.setItemSelected(node1, True)
		self.ui.listWidgetNode.setCurrentItem(node1)
		
#		self._canvas.fig.suptitle(absPath)
		
	def onCurrentNodeItemChanged(self, item):
		if not item:
			return
		print('onCurrentNodeItemChanged:', item, item.text())
		
		eNode=self.xml.eNodeList[item.idx]
		eDataList=eNode.findall(Keys.kData)
		#========================xmlDataList is [ {[]...[]}, ..., {[]...[]} ]
		#扩充 xmlDataList，如果必要
		llen=len(self.xmlDataList)
		if llen<item.idx+1:
			for i in range(item.idx+1-llen):
				self.xmlDataList.append({})	#append empty dict
		dic=self.xmlDataList[item.idx]
		if not dic:	#dic is empty
#			for i in range(len(eDataList[0].attrib)):
				
			for eData in eDataList:
				for k, v in eData.attrib.items():
					if not dic.get(k):
						dic[k]=[]
					dic[k].append(v)
#		print(dic)
		axList=dic[Keys.kAx]
		print(axList)
		ayList=dic[Keys.kAy]
		azList=dic[Keys.kAz]
		
		print(type(self._canvas.ax))
		
		#重置 ax
		curFileItem=self.ui.listWidgetFile.currentItem()
		fname=curFileItem.text() if curFileItem else None
		self._canvas.resetAxis(fname)
		
		#绘制三条曲线
		xl=self._canvas.ax.plot(axList, 'r', label='Ax')	#'o' 散点图
		yl=self._canvas.ax.plot(ayList, 'g', label='Ay')
		zl=self._canvas.ax.plot(azList, 'b', label='Az')

#		xl,=self._canvas.ax.plot(axList, 'r')	#'o' 散点图
#		yl,=self._canvas.ax.plot(ayList, 'g')
#		zl,=self._canvas.ax.plot(azList, 'b')
#		axis=self._canvas.fig.gca()
#		print(xl, yl, zl, )
		
		self._canvas.ax.legend(loc='upper left')
		
		#绘制鼠标选定的区域
		rectLR=item.areaSelected
		if rectLR:
			self._canvas.drawRectArea(rectLR[0], rectLR[1])

		#canvas 横向拉伸，避免太拥挤
#		self._canvas.ax.autoscale()
		xleft, xright=self._canvas.ax.get_xlim()
		xspan=xright-xleft
		self._canvas.setMinimumWidth(xspan*2)
#		self._canvas.ax.set_xlim(xleft, xright*2)
#		self._canvas.ax.set_xscale('log')
		import numpy as np
		if xspan>200:
			self._canvas.ax.set_xticks(np.arange(xleft, xright+1, 25))
		
		print(self._canvas.ax.get_xaxis())
		
		self._canvas.draw()
		
#	def onNodeItemSelectionChanged(self):				
#		print('onNodeItemSelectionChanged')
	
	def onAxisAreaSelected(self, t):
		'''
		t: self._canvas.selectedLR tuple
		'''
		print('onAxisAreaSelected', t)
		curNodeItem=self.ui.listWidgetNode.currentItem()
		if not curNodeItem:
			return		
		
		curFileItem=self.ui.listWidgetFile.currentItem()
		#如果 listWidgetFile 里面有选中的 item
		if curFileItem:
			#若第一次在node上框选
			if not curNodeItem.areaSelected:
				curFileItem.nodeProcessed+=1
				#如果当前 file 的 node 都处理过了
				if curFileItem.nodeProcessed is self.ui.listWidgetNode.count():
					curFileItem.finishSeg=True
					curFileItem.setBackgroundColor(self.fileItemMarkBg)
			
			atl=curFileItem.areaTupleList
#			num=self.ui.listWidgetNode.count()-len(atl)
#			if num>0:	#应该只执行一次
#				atl.append([None]*num)
			
#			if not atl:
#				atl.append([None]*self.ui.listWidgetNode.count())
			
			atl[curNodeItem.idx]=t
			print(atl)
			
		curNodeItem.areaSelected=t
		#node 变色
		curNodeItem.setBackgroundColor(self.nodeItemMarkBg)
		
	
	@QtCore.pyqtSlot()
	def on_actionOpen_triggered(self):
		print("on_actionOpen_triggered")
#		fname=QFileDialog.getOpenFileName(
#											parent=self, caption='打开 XML 文件', directory=os.path.abspath(''), 
#											filter='XML文件 (*.xml)')
#		self.parseXmlFile(fname)
		self.dirName=QFileDialog.getExistingDirectory(
#													parent=self, caption='', directory=os.path.abspath(''), 
													parent=self, caption='', directory=os.path.curdir, 
													options=QFileDialog.ShowDirsOnly)
#		print('self.dirName', self.dirName)
		if(self.dirName is ''):
			return
		self.ui.labelDirOpened.setText(self.dirName)
		os.chdir(self.dirName)	#这样可使下次open的时候记住目录
		xmlFileList=glob.glob('*.xml')
#		xmlFileList=glob.glob(self.dirName+os.sep+'*.xml')
#		xmlFileList=[os.path.basename(i) for i in xmlFileList]
		print(xmlFileList)
		
		self.ui.listWidgetFile.clear()
		for fname in xmlFileList:
			fileItem=QListWidgetItem(fname)
			fileItem.nodeProcessed=0
			fileItem.finishSeg=False
			fileItem.areaTupleList=[]
			self.ui.listWidgetFile.addItem(fileItem)
		
	
	@QtCore.pyqtSlot()
	def on_actionExit_triggered(self):
		print("on_actionExit_triggered")
		
	@QtCore.pyqtSlot()
	def on_actionSave_triggered(self):
		print('on_actionSave_triggered+++++++++')
		pathTo='./segmented'
		if not os.path.exists(pathTo):
			os.makedirs(pathTo)
		fileSelectedList=self.ui.listWidgetFile.selectedItems()
		if len(fileSelectedList) is 0:
			self.ui.statusbar.showMessage('No file item selected!!!')
			return
			
		for fileItem in fileSelectedList:
			if not fileItem.finishSeg:
				msg='selected file "%s" not finished segmentation'%fileItem.text()
				print(msg)
				self.ui.statusbar.showMessage(msg)
				return
		#对每个 file
		psr = etree.XMLParser(remove_blank_text=True)
		for fileItem in fileSelectedList:
			fname=fileItem.text()
#			tree=etree.ElementTree(file=fname, parser=psr)
			tree=etree.parse(fname, parser=psr)
			elemRoot=tree.getroot()
			elemNodes=elemRoot[0]
			#对每个 node
			for i in range(len(elemNodes)):
				left, right=fileItem.areaTupleList[i]
				elemNode=elemNodes[i]
				elemNode.set('frames', str(right-left))
				print('left, right:', left, right)
				#对每个选中的 data
#				for j in range(left, right+1):
				#先从右边移除：
				for data in elemNode[right:]:
					elemNode.remove(data)
				for data in elemNode[:left]:
					elemNode.remove(data)
			absPath=pathTo+os.path.sep+fname
#			absPathPretty=pathTo+os.path.sep+'pretty-'+fname
#			newTree.write(absPath, encoding='utf-8', pretty_print=True, xml_declaration=True)
			tree.write(absPath, encoding='utf-8', pretty_print=True, xml_declaration=True)
#			file=open(absPathPretty, 'w')
##			prettyxml=minidom.parseString(etree.tostring(element=newRoot, encoding='utf-8')).toprettyxml()	#shit minidom
#			prettyxml=etree.tostring(newRoot, pretty_print=True).decode('gb18030')	#√
##			print(prettyxml)
#			file.write(prettyxml)
#			file.close()

		
	#解析xml， node 窗口填 item	
	def parseXmlFile(self, fname):
		print('parseXmlFile')
		if not os.path.exists(fname):
			print('if not os.path.exists(fname):')
			return

		tree=ET.ElementTree(file=fname)

#		print(dir(tree))

		self.xml.elemRoot=tree.getroot()	#captureSession
#		for child in self.xml.elemRoot:
#			print('child:tab&attrib:', child.tag, child.attrib,)
		self.xml.elemNodes=self.xml.elemRoot.find(Keys.kNodes)
		self.xml.eNodeList=self.xml.elemNodes.findall(Keys.kNode)	#list
		self.ui.listWidgetNode.clear()
#		for i in self.xml.elemNodes:
#			print('i:', i)
#		print(self.xml.elemNodes[1], )
		
		curFileItem=self.ui.listWidgetFile.currentItem()
		if curFileItem and not curFileItem.areaTupleList:
			print('if curFileItem and not curFileItem.areaTupleList:')
			#若 areaTupleList ==[]
			curFileItem.areaTupleList+=[None]*len(self.xml.eNodeList)
			print(curFileItem.areaTupleList)
		for i in range(len(self.xml.eNodeList)):
			nodeItem=QListWidgetItem('node %d'%(i+1))
			nodeItem.idx=i
#			if curFileItem and curFileItem.areaTupleList:
			if curFileItem:
				nodeItem.areaSelected=curFileItem.areaTupleList[i]
			else:
				nodeItem.areaSelected=None
			if nodeItem.areaSelected:
				nodeItem.setBackgroundColor(self.nodeItemMarkBg)
			self.ui.listWidgetNode.addItem(nodeItem)
		
		self.xmlDataList.clear()
		

def main():
	app=QApplication(sys.argv)
	win=MyWindow()
	win.show()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()
	
	