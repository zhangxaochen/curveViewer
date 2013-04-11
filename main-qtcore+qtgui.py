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
#from xml.etree.ElementTree import ElementTree

class MyWidgetCurveView(QtGui.QWidget):
	def __init__(self):
		super().__init__()
		self.setMinimumWidth(1111)
	
	def paintEvent(self, event):
		qp=QtGui.QPainter(self)
#		qp.setPen(QtGui.QColor(222,222,222,222).red())	#QtCore.Qt.red
		qp.setPen(QtGui.QColor(QtCore.Qt.red))
		qp.setFont(QtGui.QFont('Decorative', 10))
#		qp.drawText(event.rect(), "str")
		size=self.size()
		for i in range(1000):
			x=random.randint(1, size.width()-1)
			y=random.randint(1, size.height()-1)
			qp.drawPoint(QtCore.QPoint(x, y))
			
class MyWindow(QtGui.QMainWindow):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.ui=Ui_MainWindow()
		self.ui.setupUi(self)
		
		widgetCurve=self.ui.scrollAreaWidgetContents
#		widgetCurve.deleteLater()
		self.ui.scrollArea.setWidget(MyWidgetCurveView())

	
	@QtCore.pyqtSlot()
	def on_actionOpen_triggered(self):
		print("on_actionOpen_triggered")
		fname=QtGui.QFileDialog.getOpenFileName(
											parent=self, caption='打开 XML 文件', directory=os.path.abspath(''), 
											filter='XML文件 (*.xml)', options=QtGui.QFileDialog.Option(0))
		if(fname!=''):
			print("fname:",fname)
			import xml.etree.ElementTree as ET
			tree=ET.ElementTree(file=fname)
			
#			print(dir(tree))
			root=tree.getroot()
			print(type(root), root.tag, root.attrib)
			for child in root:
				print(child.tag, child.attrib,)
				
#			print(tree.write(sys.stdout))
		

	
	@QtCore.pyqtSlot()
	def on_actionExit_triggered(self):
		print("on_actionExit_triggered")
		

def main():
	app=QtGui.QApplication(sys.argv)
	win=MyWindow()
	win.show()
	sys.exit(app.exec())

if __name__ == '__main__':
	main()
	
	