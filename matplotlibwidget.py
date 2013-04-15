#coding=utf-8
'''
Created on Apr 11, 2013

@author: zhangxaochen
'''
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PyQt4 import QtGui
from symbol import if_stmt

class MplCanvas(FigureCanvasQTAgg):
	def __init__(self):
		self.fig=Figure()
		super().__init__(self.fig)
		
		self.ax=self.fig.add_subplot(111)
#		self.fig.add_subplot(211)
		
#		print('type(self.ax): ', type(self.ax))	#<class 'matplotlib.axes.AxesSubplot'>
#		self.fig.add_subplot(212)	#一个 fig 可以有多个 ax
		
		self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
		self.updateGeometry()
		
		#mpl 信号槽， 处理鼠标
		self.mpl_connect('button_press_event', self.on_press)
		self.mpl_connect('button_release_event', self.on_release)
		self.mpl_connect('motion_notify_event', self.on_motion)
		
		self.mousePressX=None
#		self.mouseReleaseX=None
		
		self.rect=None

	def on_press(self, e):
		if not(e.inaxes is self.ax and e.button is 1):
		#若非 axes 内左键 
			return
		print('on_press')
		self.mousePressX=e.xdata
		
	def on_release(self, e):
		if not (e.inaxes is self.ax and self.mousePressX):
			return
		print('on_release')
		
		self.selectedLR=(self.mousePressX, e.xdata) if self.mousePressX<e.xdata else (e.xdata, self.mousePressX)
		self.mousePressX=None
		
	def on_motion(self, e):
		if not (self.mousePressX and e.inaxes is self.ax):
#		if not self.mousePressX:	#×
			#若非 press 过了，且鼠标仍在 axes 内 
			return
#		print('on_motion')
		yBottom, yTop=self.ax.get_ylim()
		axHeight=yTop-yBottom
		width=e.xdata-self.mousePressX
		if self.rect:		#切换 node 时候，导致 ValueError: list.remove(x): x not in list
#			print(self.rect.get_axes())
#			print(self.rect.get_figure())
			self.rect.remove()
#			print(self.rect)
		self.rect, =self.ax.bar(self.mousePressX, axHeight, width, yBottom)
		self.rect.set_alpha(.5)
		self.draw()
	
	def resetAxis(self, title=None):
		if self.rect:
			self.rect=None
		
		self.ax.clear()
		self.ax.grid()
		self.setAxisLabels(title)
		
	def setAxisLabels(self, title=None):
		#xy label
		self.ax.set_xlabel('Sequential Data')
		self.ax.set_ylabel('Acceleration(m/s^2)')
		
		#title=fname
		self.ax.set_title(title)
		
	
class MatplotlibWidget(QtGui.QWidget):

	def __init__(self, parent=None):
		super().__init__(parent)
		self.canvas=MplCanvas()
		self.vbl=QtGui.QVBoxLayout()
		self.vbl.addWidget(self.canvas)
		self.setLayout(self.vbl)
		
		