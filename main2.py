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
from utils import Utils, Keys
import math
import numpy as np

#curveViewer_ui.py 导入了 MatplotlibWidget
from curveViewer_ui import *

class MyWindow(QMainWindow):
	#空壳
	class DataObj:
		pass
	
	#k: 当前加载的文件名；	v: DataObj， 挂靠了 xmlDic, accX,Y,Z, ....
	fileDict={}
	
	channelsToShow=[
		#0
		'AxBF',
		'AyBF',
		'AzBF',
		'AxyzBF',
		
		#4
		'AxWF',
		'AyWF',
		'AzWF',
		'AxyWF',
		
		#8
		'Vx',
		'Vy',
		'Vz',
		'Vxy',
		
		#12
		'GxBF',
		'GyBF',
		'GzBF',
		]
	
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
		
		self.fileItemMarkBg=Qt.green
		self.nodeItemMarkBg=Qt.yellow
		
		#??
		# self.canvas.draw()
		
		self.ui.listWidgetChannel.addItems(self.channelsToShow)
		pass
		
	
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

		if self.ui.actionLegend.isChecked() and len(channelItems) !=0:
			ax.legend()
		self.canvas.draw()
		pass
		
	def plotByIndex(self, fname, idx):
		# print('plotByIndex, idx:', idx)
		ax=self.canvas.ax
		obj=self.fileDict[fname]
		dic=obj.xmlDic
		
		accX=dic[Keys.kAx]
		accY=dic[Keys.kAy]
		accZ=dic[Keys.kAz]
		gx=dic[Keys.kGx]
		gy=dic[Keys.kGy]
		gz=dic[Keys.kGz]
		
		if not hasattr(obj, 'accXYZ'):
			obj.accXYZ=(accX**2+accY**2+accZ**2)**0.5
		if not hasattr(obj, 'accWF'):
			obj.accWF=self.getAccWF(dic)
		if not hasattr(obj, 'vWF'):
			# tsList=dic[Keys.kTs] if dic.get(Keys.kTs) != None else dic[Keys.kTimestamp]
			tsList=obj.tsList
			obj.vWF=self.getVWF(obj.accWF, tsList)
		
		#-----------------plot
		#AccBF
		if idx==self.channelDict['AxBF']:
			ax.plot(accX, 'r', label='AxBF')
		elif idx==self.channelDict['AyBF']:
			ax.plot(accY, 'g', label='AyBF')
		elif idx==self.channelDict['AzBF']:
			ax.plot(accZ, 'b', label='AzBF')
		elif idx==self.channelDict['AxyzBF']:
			ax.plot(obj.accXYZ, 'm', label='AxyzBF')
		#AccWF
		elif idx==self.channelDict['AxWF']:
			ax.plot(obj.accWF[0], 'r', label='AxWF', ls='--', lw=2)
		elif idx==self.channelDict['AyWF']:
			ax.plot(obj.accWF[1], 'g', label='AyWF', ls='--', lw=2)
		elif idx==self.channelDict['AzWF']:
			ax.plot(obj.accWF[2], 'b', label='AzWF', ls='--', lw=2)
		elif idx==self.channelDict['AxyWF']:
			ax.plot(obj.accWF[3], 'm', label='AxyWF', ls='--', lw=2)
		#vWF
		elif idx==self.channelDict['Vx']:
			ax.plot(obj.vWF[0], 'r', label='Vx', lw=2)
		elif idx==self.channelDict['Vy']:
			ax.plot(obj.vWF[1], 'g', label='Vy', lw=2)
		elif idx==self.channelDict['Vz']:
			ax.plot(obj.vWF[2], 'b', label='Vz', lw=2)
		elif idx==self.channelDict['Vxy']:
			vxy=(obj.vWF[0]**2+obj.vWF[1]**2)**0.5
			ax.plot(vxy, 'm', label='Vxy', lw=2)
		#gyro in BF:
		elif idx==self.channelDict['GxBF']:
			ax.plot(gx, 'r', label='GxBF')
		elif idx==self.channelDict['GyBF']:
			ax.plot(gy, 'g', label='GyBF')
		elif idx==self.channelDict['GzBF']:
			ax.plot(gz, 'b', label='GzBF')
			
		pass
	
	#RETURN np.array([[...][...][...][...]]), arr[3] is AxyWF
	def getAccWF(self, xmlDic):
		res=[]
		dic=xmlDic
		
		for i in range(len(dic[Keys.kAx])):
			rotationVector=[
				dic[Keys.kRx][i],
				dic[Keys.kRy][i],
				dic[Keys.kRz][i],
				]
			accVector=[
				dic[Keys.kAx][i],
				dic[Keys.kAy][i],
				dic[Keys.kAz][i]
				]
			rotationMatrix=Utils.getRotationMatrixFromVector(rotationVector)
			accWfVector=Utils.multiplyMV3(rotationMatrix, accVector)
			#AxyWF:
			t=accWfVector
			t.append((t[0]**2+t[1]**2)**0.5)
			res.append(accWfVector)
		res=np.array(res).T
		res[2]-=9.80665
		return res
		pass
	
	# accWF.shape==(n, 4);	tsList is in epoch seconds
	def getVWF(self, accWF, tsList):
		res=[]
		#len is n-1
		# accwfDiff=accWF[1:]-accWF[:-1]
		
		accWF=accWF.T
		print('accWF.shape:', accWF.shape)
		sum=np.zeros(3)
		res.append(sum.copy())
		for i in range(len(tsList)-1):
			dt=tsList[i+1]-tsList[i]
			#第一帧时间戳的 bug
			if dt>1000:
				print('=======================dt>1000. dt, i are:', dt, i)
			dt=tsList[-1]-tsList[-2] if dt>1000 else dt
			#i 偏小， i+1 偏大； 
			sum+=accWF[i][:3]*dt/1000
			res.append(sum.copy())
		res=np.array(res).T
		return res
		pass
		
	#必须有 previous， 否则不自动connect
	@pyqtSlot(QListWidgetItem, QListWidgetItem)
	def on_listWidgetFile_currentItemChanged(self, item, prev):
		# print('on_listWidgetFile_currentItemChanged', id(item), prev)
		if not item:
			return 
		baseName=item.text()
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
		print('on_listWidgetChannel_itemSelectionChanged')
		curFileItem=self.ui.listWidgetFile.currentItem()
		print( 'curFileItem', curFileItem, id(curFileItem) )
		if curFileItem:
			self.plotCurves(curFileItem.text())
		
		pass
		
	
	@pyqtSlot()
	def on_actionOpen_triggered(self):
		print('on_actionOpen_triggered')
		#清掉挂靠的数据：
		self.fileDict.clear()
		
		self.dirName=QFileDialog.getExistingDirectory(
		parent=self, caption=u'打开文件夹', directory=os.path.curdir,
			options=QFileDialog.ShowDirsOnly)
		
		# print(type(self.dirName))	#<class 'PyQt4.QtCore.QString'>
		#str() 包裹下， 兼容性，必要：
		self.dirName=str(self.dirName)
		
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
		print('on_actionSave_triggered')
		pass
	
	@pyqtSlot(bool)
	def on_actionAccBodyFrame_triggered(self, checked=None):
		print('on_actionAccBodyFrame_triggered')
		keys=[
			'AxBF',
			'AyBF',
			'AzBF',
			'AxyzBF',
			]
		self.selectItemsByKeys(keys, checked)
		pass
	
	@pyqtSlot(bool)
	def on_actionAccWorldFrame_triggered(self, checked):
		print('on_actionAccWorldFrame_triggered')
		keys=[
			'AxWF',
			'AyWF',
			'AzWF',
			'AxyWF',
			]
		self.selectItemsByKeys(keys, checked)

		pass
	
	@pyqtSlot(bool)
	def on_actionVelocity_triggered(self, checked):
		print('on_actionVelocity_triggered')
		keys=[
			'Vx',
			'Vy',
			'Vz',
			'Vxy',
			]
		self.selectItemsByKeys(keys, checked)
		pass
	
	@pyqtSlot(bool)
	def on_actionDisplacement_triggered(self, checked):
		print('on_actionDisplacement_triggered')
		pass
	
	@pyqtSlot(bool)
	def on_actionGyro_in_BF_triggered(self, checked):
		print('on_actionGyro_in_BF_triggered')
		
		gyroKeys=[
			'GxBF',
			'GyBF',
			'GzBF',
			]
		#别用 [12:15]， 因为可能再添别的channel，导致改变索引号：
		# gyroKeys=self.channelsToShow[12:15]
		self.selectItemsByKeys(gyroKeys, checked)
		
		pass
	
	@pyqtSlot(bool)
	def on_actionLegend_triggered(self, checked):
		print('on_actionLegend_triggered')
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
		
		psr = etree.XMLParser(remove_blank_text=True)
		tree=etree.parse(fname, psr)
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
				dic[k]=np.array([ float(val) for val in v])
				
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
