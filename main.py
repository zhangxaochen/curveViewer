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
import xml.etree.ElementTree as ET
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
		
		ranNums=random.sample(range(100), 100)
		self.ui.mplWidget.canvas.ax.clear()
#		self.ui.mplWidget.canvas.ax.plot(ranNums)
#		self.ui.mplWidget.canvas.draw()
		
		self.xml=self.XmlStuff()

		#==================================xml test
		fname='E:/workspace/PyCeshi/curveViewer/ttt.xml'
		self.parseXmlFile(fname)
				
		#===================================信号槽
#		self.ui.listWidgetNode.itemChanged.connect(lambda x:print('the args: ', x))
#		self.ui.listWidgetNode.itemActivated.connect(lambda x:print('itemActivated, the args: ', x))	#要双击
#		self.ui.listWidgetNode.itemSelectionChanged.connect(lambda : print('isc========'))
#		self.ui.listWidgetNode.currentItemChanged.connect(lambda x: print('cic, x+++', x))
		self.ui.listWidgetNode.itemClicked.connect(self.onNodeItemClicked)
		self.ui.listWidgetFile.currentItemChanged.connect(self.onFileItemClicked)
		
	def onFileItemClicked(self, item):
		print('onFileItemClicked')
		baseName=item.text()
		absPath=self.dirName+os.sep+baseName
		self.parseXmlFile(absPath)
		
		
		
	def onNodeItemClicked(self, item):
		print('itemClicked, the args: ', item, item.text())
		t=item.text()
		idx=int(t[len(t)-1])-1
		print('idx', idx)
		eNode=self.xml.eNodeList[idx]
		eDataList=eNode.findall(Keys.kData)
		#========================xmlDataList is [ {[]...[]}, ..., {[]...[]} ]
		#扩充 xmlDataList，如果必要
		llen=len(self.xmlDataList)
		if llen<idx+1:
			for i in range(idx+1-llen):
				self.xmlDataList.append({})	#append empty dict
		dic=self.xmlDataList[idx]
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
		
		self.ui.mplWidget.canvas.ax.clear()
		self.ui.mplWidget.canvas.ax.plot(axList)
		self.ui.mplWidget.canvas.draw()
					

	
	@QtCore.pyqtSlot()
	def on_actionOpen_triggered(self):
		print("on_actionOpen_triggered")
#		fname=QFileDialog.getOpenFileName(
#											parent=self, caption='打开 XML 文件', directory=os.path.abspath(''), 
#											filter='XML文件 (*.xml)')
#		self.parseXmlFile(fname)
		self.dirName=QFileDialog.getExistingDirectory(parent=self, caption='', directory=os.path.abspath(''), options=QFileDialog.ShowDirsOnly)
#		print('dirName', self.dirName)
		
		self.ui.labelDirOpened.setText(self.dirName)
		xmlFileList=glob.glob(self.dirName+os.sep+'*.xml')
#		print(xmlFileList)
		xmlFileList=[os.path.basename(i) for i in xmlFileList]
		print(xmlFileList)
		
		self.ui.listWidgetFile.clear()
		for fname in xmlFileList:
			self.ui.listWidgetFile.addItem(fname)
	
	@QtCore.pyqtSlot()
	def on_actionExit_triggered(self):
		print("on_actionExit_triggered")
		
	#解析xml， 左上角窗口填 item	
	def parseXmlFile(self, fname):
		if(fname==''):
			return
		tree=ET.ElementTree(file=fname)
#		print(dir(tree))

		self.xml.elemRoot=tree.getroot()	#captureSession
#		for child in self.xml.elemRoot:
#			print('child:tab&attrib:', child.tag, child.attrib,)
		self.xml.elemNodes=self.xml.elemRoot.find(Keys.kNodes)
		self.xml.eNodeList=self.xml.elemNodes.findall(Keys.kNode)	#list
		self.ui.listWidgetNode.clear()
		for i in range(len(self.xml.eNodeList)):
			self.ui.listWidgetNode.addItem('node %d'%(i+1))
		
		self.xmlDataList.clear()
		

def main():
	app=QApplication(sys.argv)
	win=MyWindow()
	win.show()
	sys.exit(app.exec())

if __name__ == '__main__':
	main()
	
	