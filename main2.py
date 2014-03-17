#coding=utf-8

'''
Created on 2013-11-1 17:48:31
@author: zhangxaochen

说明：	之前写的太烂了，重构;
'''

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from glob import glob
import os, sys, random, time
from lxml import etree
import traceback
# from utils import Utils, Keys, LPF
from utils import *
import math
import numpy as np

#curveViewer_ui.py 导入了 MatplotlibWidget
from curveViewer_ui import *

#colors
co=('r', 'g', 'b', 'm', 'c', 'b', 'gray')

class MyWindow(QMainWindow):
	#全局
	psr = etree.XMLParser(remove_blank_text=True)
	
	#标记 canvas 是否 plot 过：
	emptyCanvas=True
	
	#空壳
	class DataObj:
		pass
	
	#k: 当前加载的文件名；	v: DataObj， 挂靠了 xmlDic, accX,Y,Z, ....
	fileDict={}
	
	accBfKeys=['AxBF', 'AyBF', 'AzBF', 'AxyzBF', 'AxyzBF_LPF']
	accWfKeys=['AxWF', 'AyWF', 'AzWF', 'AxyWF', 'AzWF_LPF', 'AxyzWF', 'AxyDir[arctan(ay/ax)]']
	velKeys=['Vx', 'Vy', 'Vz', 'Vxy', ]
	
	gbfKeys=['GxBF', 'GyBF', 'GzBF', 'GxyzBF', 'GxyzBF_LPF']
	gwfKeys=['GxWF', 'GyWF', 'GzWF', ]
	#旋转角：
	angWfKeys=['AngXWF', 'AngYWF', 'AngZWF', 'AngZWF_lpf']
	
	magBfKeys=['MxBF', 'MyBF', 'MzBF']
	
	disKeys=['Displacement']
	
	rotKeys=[Keys.kRx, Keys.kRy, Keys.kRz, Keys.kRw, ]
	
	channelsToShow=accBfKeys+accWfKeys+velKeys+gbfKeys+gwfKeys+angWfKeys+magBfKeys+disKeys+rotKeys

	#channelsToShow 改成 dict
	channelDict={}
	for i, k in enumerate(channelsToShow):
		channelDict[k]=i
	print(channelDict)
	
	debugMode=True
	
	def __init__(self, parent=None):
		super(MyWindow, self).__init__(parent)
		self.ui=Ui_MainWindow()
		self.ui.setupUi(self)
		
		self.canvas=self.ui.mplWidget.canvas
		self.canvas.resetAxis()
		
		#??
		self.fileItemMarkBg=Qt.green
		# self.nodeItemMarkBg=Qt.yellow
		
		#??
		# self.canvas.draw()
		
		self.ui.listWidgetChannel.addItems(self.channelsToShow)
		
		#默认显示 accBF
		self.ui.actionAccBodyFrame.trigger()
		#隐藏 listWidgetNode
		self.ui.listWidgetNode.hide()
		
		#===================================信号槽
		self.canvas.areaSelected.connect(self.onAxisAreaSelected)
		
		pass
		
	def onAxisAreaSelected(self, lrTuple):
		print('onAxisAreaSelected', lrTuple)
		
		curFileItem=self.ui.listWidgetFile.currentItem()
		obj=self.fileDict[str(curFileItem.text())]
		# if not hasattr(obj, 'rectLR'):
		obj.rectLR=lrTuple
		self.ui.listWidgetFile.currentItem().setBackgroundColor(self.fileItemMarkBg)
		
	def plotCurves(self, fname):
		self.canvas.resetAxis(fname)
		ax=self.canvas.ax

		# print('plotCurves, item:', item, id(item) )
		#fps:
		obj=self.fileDict[fname]
		dic=obj.xmlDic
		if not hasattr(obj, 'tsList'):
			obj.tsList=dic[Keys.kTs] if dic.get(Keys.kTs) != None else dic[Keys.kTimestamp]
		tsList=obj.tsList
		# print('tsList:',tsList)
		fps=len(tsList)*1000/(tsList[-1]-tsList[0])
		ax.text(.05, .05, '%.1f FPS'%fps, fontsize=16, transform=ax.transAxes, label='shit') #transAxes 00左下，11右上角

		channelItems=self.ui.listWidgetChannel.selectedItems()
		for ci in channelItems:
			t=str(ci.text())
			idx=self.channelDict[t]
			self.plotByIndex(fname, idx)
		
		#绘制鼠标选定的区域
		if hasattr(obj, 'rectLR'):
			rectLR=obj.rectLR
			# if rectLR:
			self.canvas.drawRectArea(rectLR[0], rectLR[1])
			# self.ui.listWidgetFile.currentItem().setBackgroundColor(self.fileItemMarkBg)
		
		if self.ui.actionLegend.isChecked() and len(channelItems) !=0:
			ax.legend()
		self.canvas.draw()
		pass
		
	def plotByIndex(self, fname, idx):
		# print('plotByIndex, idx:', idx)
		self.emptyCanvas=False
		
		ax=self.canvas.ax
		obj=self.fileDict[fname]
		dic=obj.xmlDic
		
		#accBF x,y,z, xyz, xyz_lpf
		if not hasattr(obj, 'accBF'):
			obj.accBF=getAccBF(dic)
		#accWF x,y,z, AxyWF, azWF_LPF
		if not hasattr(obj, 'accWF'):
			obj.accWF=getAccWF(dic)
		if not hasattr(obj, 'vWF'):
			# tsList=dic[Keys.kTs] if dic.get(Keys.kTs) != None else dic[Keys.kTimestamp]
			tsList=obj.tsList
			obj.vWF=getVWF(obj.accWF, tsList)
		#displacement	位移：
		if not hasattr(obj, 'dWF'):
			obj.dWF=getDWF(obj.vWF, tsList)
		#gyroBF x,y,z, gxyz, gxyz_lpf
		if not hasattr(obj, 'gyroBF'):
			obj.gyroBF=getGyroBF(dic)
		#gyroWF x,y,z
		if not hasattr(obj, 'gyroWF'):
			obj.gyroWF=getGyroWF(dic)
		if not hasattr(obj, 'angleWF'):
			obj.angleWF=getAngleWF(obj.gyroWF, obj.tsList)
		
		#magBF x,y,z
		if not hasattr(obj, 'magBF'):
			obj.magBF=getMagBF(dic)
		
		#rotation vector x, y, z, w
		if not hasattr(obj, 'rotVec'):
			obj.rotVec=getRotationVector(dic)
		
		
			
		#-----------------plot
		#AccBF
		for i, k in enumerate(self.accBfKeys):
			if idx==self.channelDict[k]:
				lw=1 if i !=4 else 2
				ax.plot(obj.accBF[i], co[i], label=k, lw=lw)
		#AccWF
		for i, k in enumerate(self.accWfKeys):
			if idx==self.channelDict[k]:
				ax.plot(obj.accWF[i], co[i], label=k, ls='--', lw=2)
		#vWF
		for i, k in enumerate(self.velKeys):
			if idx==self.channelDict[k]:
				ax.plot(obj.vWF[i], co[i], label=k, lw=2)
			
		#gyro in BF:
		for i, k in enumerate(self.gbfKeys):
			if idx==self.channelDict[k]:
				lw=1 if i !=4 else 2
				ax.plot(obj.gyroBF[i], co[i], label=k, lw=lw)
		#gyro in WF:
		for i, k in enumerate(self.gwfKeys):
			if idx==self.channelDict[k]:
				ax.plot(obj.gyroWF[i], co[i], label=k, )
		#angle in WF:
		for i, k in enumerate(self.angWfKeys):
			if idx==self.channelDict[k]:
				ax.plot(obj.angleWF[i], co[i], label=k, lw=2)
		
		for i, k in enumerate(self.magBfKeys):
			if idx==self.channelDict[k]:
				ax.plot(obj.magBF[i], co[i], label=k, )
		
		#displacement:
		if idx==self.channelDict['Displacement']:
			axd=self.axDis
			#?? 没重置
			
			dx=obj.dWF[0]
			dy=obj.dWF[1]
			print ('dx.shape', dx.shape, dy.shape)
			axd.plot(dx, dy, co[3], label='displacement')
			axd.plot(dx[0], dy[0], 'bo')
			axd.plot(dx[-1], dy[-1], 'bo')
			for k, v in {0:'startPoint', -1:'endPoint'}.items():
				axd.annotate(v, xy=(dx[k], dy[k]), xycoords='data', xytext=(20,-20), textcoords='offset points', 
				bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5),
				fontsize=12, arrowprops=dict(arrowstyle='->', connectionstyle='arc3, rad=.2'))
		
		#rotation vector x, y, z, w
		for i, k in enumerate(self.rotKeys):
			if idx==self.channelDict[k]:
				ax.plot(obj.rotVec[i], co[i], label=k)

		
		pass

	#必须有 previous， 否则不自动connect
	@pyqtSlot(QListWidgetItem, QListWidgetItem)
	def on_listWidgetFile_currentItemChanged(self, item, prev):
		# print('on_listWidgetFile_currentItemChanged', id(item), prev)
		if not item:
			return 
		baseName=str(item.text())
		# print 'baseName', baseName, type(baseName)
		absPath=os.path.realpath(baseName)
		st=time.time()
		# if not hasattr(item, 'xmlDic'):
			# item.xmlDic=self.parseXmlFile(absPath)
		# self.ui.listWidgetFile.currentItem().xmlDic
		
		if self.fileDict.get(baseName) is None:
			obj=self.DataObj()
			obj.xmlDic=self.parseXmlFile(absPath)
			self.fileDict[baseName]=obj
			
		et=time.time()
		print('[[[parseXmlFile:', et-st)
		
		self.plotCurves(baseName)
		pass
	
	@pyqtSlot()
	def on_listWidgetNode_currentItemChanged(self, item):
		print('on_listWidgetNode_currentItemChanged')
		pass
	
	@pyqtSlot()
	def on_listWidgetChannel_itemSelectionChanged(self):
		# print('on_listWidgetChannel_itemSelectionChanged')
		selectedKeys= set([str(item.text()) for item in self.ui.listWidgetChannel.selectedItems()])
		
		self.ui.actionAccBodyFrame.setChecked(selectedKeys >= set(self.accBfKeys) )
		self.ui.actionAccWorldFrame.setChecked(selectedKeys >= set(self.accWfKeys) )
		self.ui.actionVelocity.setChecked(selectedKeys >= set(self.velKeys) )
		self.ui.actionDisplacement.setChecked(selectedKeys >= set(self.disKeys) )
		self.ui.actionGyro_in_BF.setChecked(selectedKeys >= set(self.gbfKeys) )
		
		curFileItem=self.ui.listWidgetFile.currentItem()
		# print( 'curFileItem', curFileItem, id(curFileItem) )
		if curFileItem:
			self.plotCurves(str(curFileItem.text()))
		pass
	
	@pyqtSlot()
	def on_actionOpen_triggered(self):
		print('on_actionOpen_triggered')
		#清掉挂靠的数据：
		self.fileDict.clear()
		
		self.dirName=QFileDialog.getExistingDirectory(
		parent=self, caption=u'打开文件夹', directory=os.path.curdir,
			options=QFileDialog.ShowDirsOnly)
		
		# print(type(self.dirName))	#py2, <class 'PyQt4.QtCore.QString'>
		if sys.version_info[0] ==3:
			#py3 QString 直接自动成为 str
			# self.dirName=str(self.dirName)
			pass
		elif sys.version_info[0]==2:
			print (self.dirName.toUtf8() )	#√ for py2, to QByteArray
			#py2 这里需要用 unicode object， not str
			self.dirName=unicode(self.dirName.toUtf8(), 'utf', 'strict')
		
		if self.dirName=='':
			return
		self.ui.labelDirOpened.setText(self.dirName)
		os.chdir(self.dirName)
		xmlFiles=glob('*.xml')
		print(xmlFiles)
		
		self.ui.listWidgetFile.clear()
		self.ui.listWidgetFile.addItems(xmlFiles)
		
		pass
		
	@pyqtSlot()
	def on_actionExit_triggered(self):
		print('on_actionExit_triggered')
		pass
	
	@pyqtSlot()
	def on_actionSave_triggered(self):
		print('on_actionSave_triggered+++++++++')
		pathTo='./segmented'
		if not os.path.exists(pathTo):
			os.makedirs(pathTo)
		fileSelectedList=self.ui.listWidgetFile.selectedItems()
		#转成 str list
		# fileSelectedList=[str(f.text()) for f in fileSelectedList]
		
		if len(fileSelectedList) is 0:
			self.ui.statusbar.showMessage('No file item selected!!!')
			return
		
		for fileItem in fileSelectedList:
			fname=str(fileItem.text())
			obj=self.fileDict[fname]
			#检查选中的 fileItem 是否都分割过了	
			if not hasattr(obj, 'rectLR'):
				msg='selected file "%s" not finished segmentation'%fileItem.text()
				print(msg)
				self.ui.statusbar.showMessage(msg)
				return
			
			# mainFname=os.path.splitext(fname)[0]
			
			#=================分割， 存到 segmented：
			tree=etree.parse(fname, parser=self.psr)
			rt=tree.getroot()
			nodeNode=rt[0][0]
			left, right=obj.rectLR
			
			#先从右边移除：
			for data in nodeNode[right:]:
				nodeNode.remove(data)
			for data in nodeNode[:left]:
				nodeNode.remove(data)
			absPath=os.path.join(pathTo, fname)
			#会把乱码转为正常：
			# tree.write(absPath, encoding='utf-8', pretty_print=True, xml_declaration=True)
			
			#为避免 tree.write 再把乱码转为汉字， 直接用 file.write：
			xmlStr=etree.tostring(tree, pretty_print=True, xml_declaration=True, encoding='utf-8').decode()
			# ff=open(absPath, 'w')
			with open(absPath, 'w') as ff:
				ff.write(xmlStr)
			# ff.close()
			
			#config filename, or [label, startTime, endTime] file:
			cfgFname=os.path.splitext(fname)[0]+'.txt'
			
			with open(cfgFname, 'w') as ft:
				sts=float(nodeNode[0].attrib[Keys.kTs])/1e3
				ets=float(nodeNode[-1].attrib[Keys.kTs])/1e3
				ft.write('%s %s'%(sts, ets))
			
		
		
		pass
	
	@pyqtSlot(bool)
	def on_actionAccBodyFrame_triggered(self, checked=None):
		print('on_actionAccBodyFrame_triggered')
		self.selectItemsByKeys(self.accBfKeys, checked)
		pass
	
	@pyqtSlot(bool)
	def on_actionAccWorldFrame_triggered(self, checked):
		print('on_actionAccWorldFrame_triggered')
		self.selectItemsByKeys(self.accWfKeys, checked)
		pass
	
	@pyqtSlot(bool)
	def on_actionVelocity_triggered(self, checked):
		print('on_actionVelocity_triggered')
		self.selectItemsByKeys(self.velKeys, checked)
		pass
	
	@pyqtSlot(bool)
	def on_actionDisplacement_triggered(self, checked):
		print('on_actionDisplacement_triggered')
		self.selectItemsByKeys(self.disKeys, checked)
		pass
	
	#调用链末端：
	@pyqtSlot(bool)
	def on_actionDisplacement_toggled(self, checked):
		print('on_actionDisplacement_toggled')
		#??
		self.canvas.fig.delaxes(self.canvas.ax)
		if checked:
			self.canvas.ax=self.canvas.fig.add_subplot(211)
			#ax for displacement
			self.axDis=self.canvas.fig.add_subplot(234)
		else:
			self.canvas.fig.delaxes(self.axDis)
			self.canvas.ax=self.canvas.fig.add_subplot(111)
		self.canvas.draw()
		pass
	
	@pyqtSlot(bool)
	def on_actionGyro_in_BF_triggered(self, checked):
		print('on_actionGyro_in_BF_triggered')
		
		#别用 [12:15]， 因为可能再添别的channel，导致改变索引号：
		# gbfKeys=self.channelsToShow[12:15]
		self.selectItemsByKeys(self.gbfKeys, checked)
		pass
	
	@pyqtSlot(bool)
	def on_actionLegend_triggered(self, checked):
		print('on_actionLegend_triggered')
		if self.emptyCanvas:
			return
		leg=self.canvas.ax.legend()
		if leg != None:
			leg.set_visible(checked)
		self.canvas.draw()
		pass
	
	# .ui 文件中custom slot， 参见evernote笔记
	def testSlot(self):
		# print('testSlot')
		pass
	
	#解析 xml， 返回 xmlDic
	def parseXmlFile(self, fname):
		print('parseXmlFile()')
		if not os.path.exists(fname):
			print('if not os.path.exists(fname)')
			return
		
		
		tree=etree.parse(fname, self.psr)
		rt=tree.getroot()
		#旧格式
		if rt.tag==Keys.kRoot:
			#对手机传感器只有一个node：
			nodeNode=rt[0][0]
			dic={}
			for dataNode in nodeNode:
				for k, v in dataNode.attrib.items():
					if not dic.get(k):
						dic[k]=[]
					dic[k].append(v)
			
			#[] to np.ndarray, str to float
			for k, v in dic.items():
				#dic[k]=np.array(map(float, v))
				dic[k]=np.asanyarray([ float(val) for val in v])
				
			return dic
		pass
	
	#根据传入 keys 选择/取消选择 listWidgetChannel 的 items
	def selectItemsByKeys(self, keys, doSelect):
		wid=self.ui.listWidgetChannel
		for k in keys:
			idx=self.channelDict[k]
			item=wid.item(idx)
			item.setSelected(doSelect)
		pass
	pass
	

def main():
	app=QApplication(sys.argv)
	win=MyWindow()
	win.show()
	sys.exit(app.exec_())

if __name__=='__main__':
	main()
