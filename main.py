#coding=utf-8
'''
Created on Apr 8, 2013

@author: zhangxaochen
'''
#from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from curveViewer_ui import *
import sys
import os
import random
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
			tsList=self.getAttribListFromKey(Keys.kTs)
			tsStart=tsList[0]
			for i in range(len(tsList)):
				tsList[i]-=tsStart
				
				
			
				
				
			
			
			pass
		
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
	
	def __init__(self, parent=None):
		super().__init__(parent)
		self.ui=Ui_MainWindow()
		self.ui.setupUi(self)
		
#		print(self.ui.widgetCurve)
		self.ui.widgetCurve=MyWidgetCurveView()
		self.ui.scrollArea.setWidget(self.ui.widgetCurve)
		
		self.xml=self.XmlStuff()

		#-------------------------------------------------------xml test
		fname='E:/workspace/PyCeshi/curveViewer/ttt.xml'
		tree=ET.ElementTree(file=fname)
#		print(dir(tree))

		self.xml.elemRoot=tree.getroot()	#captureSession
		for child in self.xml.elemRoot:
			print('child:tab&attrib:', child.tag, child.attrib,)
#		print(dir(elemRoot))
#		print(type(elemRoot), elemRoot.tag, elemRoot.attrib)
		self.xml.elemNodes=self.xml.elemRoot.find(Keys.kNodes)
		self.xml.elemsNodeList=self.xml.elemNodes.findall(Keys.kNode)	#list
		for i in range(len(self.xml.elemsNodeList)):
			self.ui.listWidgetNode.addItem('node %d'%(i+1))
		
		#=================信号槽
#		self.ui.listWidgetNode.itemChanged.connect(lambda x:print('the args: ', x))
#		self.ui.listWidgetNode.itemActivated.connect(lambda x:print('itemActivated, the args: ', x))	#要双击
		self.ui.listWidgetNode.itemClicked.connect(self.onNodeItemClicked)
		
		
	def onNodeItemClicked(self, item):
		print('itemClicked, the args: ', item, item.text())
		t=item.text()
		idx=int(t[len(t)-1])-1
		print('idx', idx)
#		self.xml.elemNodes[idx]
		aNode=self.xml.elemsNodeList[idx]
		dataList=aNode.findall(Keys.kData)
		
		wc=self.ui.widgetCurve
		dataDictList=wc.dataDictList
		dataDictList.clear()
		for data in dataList:
			#print(data)
#			print(data.attrib)	#dict
			dataDictList.append(data.attrib)
			
		wc.repaint()
#		wc.resize(wc.width()*2, wc.height())
#		print('wc.width()', wc.width())
		
		

	
	@QtCore.pyqtSlot()
	def on_actionOpen_triggered(self):
		print("on_actionOpen_triggered")
		fname=QFileDialog.getOpenFileName(
											parent=self, caption='打开 XML 文件', directory=os.path.abspath(''), 
#											filter='XML文件 (*.xml)', options=QFileDialog.Option(0))
											filter='XML文件 (*.xml)')
		if(fname==''):
			return
		print("fname:",fname)
		tree=ET.ElementTree(file=fname)
#		print(dir(tree))

		elemRoot=tree.getroot()	#captureSession
#		print(dir(elemRoot))
		print(elemRoot.find(self.kXmlNodes))
		
		
		print(type(elemRoot), elemRoot.tag, elemRoot.attrib)
		for child in elemRoot:
			print(child.tag, child.attrib,)


	
	@QtCore.pyqtSlot()
	def on_actionExit_triggered(self):
		print("on_actionExit_triggered")
		

def main():
	app=QApplication(sys.argv)
	win=MyWindow()
	win.show()
	sys.exit(app.exec())

if __name__ == '__main__':
	main()
	
	