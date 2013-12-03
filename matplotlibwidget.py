#coding=utf-8
'''
Created on Apr 11, 2013

@author: zhangxaochen
'''

from matplotlib import rcParams
#为了anaconda兼容性。 贱人
rcParams['backend.qt4'] = 'PyQt4'

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from PyQt4 import QtGui, QtCore

def zoom_factory(ax,base_scale = 2.):
	def zoom_fun(event):
		# get the current x and y limits
		cur_xlim = ax.get_xlim()
		cur_ylim = ax.get_ylim()
		# set the range
		cur_xrange = (cur_xlim[1] - cur_xlim[0])*.5
		cur_yrange = (cur_ylim[1] - cur_ylim[0])*.5
		xdata = event.xdata # get event x location
		ydata = event.ydata # get event y location
		if event.button == 'up':
			# deal with zoom in
			scale_factor = 1/base_scale
		elif event.button == 'down':
			# deal with zoom out
			scale_factor = base_scale
		else:
			# deal with something that should never happen
			scale_factor = 1
			print(event.button)
		# set new limits
		ax.set_xlim([xdata - cur_xrange*scale_factor,
					 xdata + cur_xrange*scale_factor])
		ax.set_ylim([ydata - cur_yrange*scale_factor,
					 ydata + cur_yrange*scale_factor])
		ax.figure.canvas.draw() # force re-draw
 
	fig = ax.get_figure() # get the figure of interest
	# attach the call back
	fig.canvas.mpl_connect('scroll_event',zoom_fun)
 
	#return the function
	return zoom_fun

class MplCanvas(FigureCanvasQTAgg):
	areaSelected=QtCore.pyqtSignal(tuple)
	def __init__(self):
		self.fig=Figure()
		super(MplCanvas, self).__init__(self.fig)
		
		self.ax=self.fig.add_subplot(111)
		#用于保存一个弱连接，参见：	 http://stackoverflow.com/questions/11551049/matplotlib-plot-zooming-with-scroll-wheel
		self.zoom_ref=zoom_factory(self.ax)
#		self.fig.add_subplot(211)
		
#		print('type(self.ax): ', type(self.ax))	#<class 'matplotlib.axes.AxesSubplot'>
#		self.fig.add_subplot(212)	#一个 fig 可以有多个 ax
		
		# self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
		self.updateGeometry()
		
		#mpl 信号槽， 处理鼠标
		self.mpl_connect('button_press_event', self.on_press)
		self.mpl_connect('button_release_event', self.on_release)
		self.mpl_connect('motion_notify_event', self.on_motion)
		self.mpl_connect('key_press_event', self.on_key_press)
		self.mpl_connect('key_release_event', self.on_key_release)
		
		self.ctrlPressed=False
		self.startX=None
		self.prevX=None
#		self.mouseReleaseX=None
		self.rectBar=None
#		print('self.rectBar',self.rectBar)

#		self.areaSelected=QtCore.pyqtSignal(tuple)
	
	def on_key_press(self, e):
		print('key pressed:', e.key, e.xdata, e.ydata, type(e.key))
		
		if e.key == 'control':
			self.ctrlPressed=True
		
	def on_key_release(self, e):
		print('key released :', e.key, e.xdata, e.ydata)
		if e.key == 'control':
			self.ctrlPressed=False

	def on_press(self, e):
		if not(e.inaxes is self.ax and e.button is 1 and self.ctrlPressed):
		#若非 axes 内左键 
			return
		print('on_press')
		if not self.startX:
			self.startX=int(round(e.xdata))
		
	def on_release(self, e):
#		if not (e.inaxes is self.ax and self.startX):
#			return
		if self.startX is None or e.inaxes is not self.ax:
			#若没 press过， 或鼠标移出范围
			return

		print('on_release')
		
		endX=int(round(e.xdata))
		print('self.startX, endX:', self.startX, endX)
		if self.startX is not endX:
			self.selectedLR=(self.startX, endX) if self.startX<endX else (endX, self.startX)
			self.areaSelected.emit(self.selectedLR)
		
		self.startX=None
		
		
	def on_motion(self, e):
		# if self.startX is None or e.inaxes is not self.ax or not self.ctrlPressed:
		if not (self.startX and e.inaxes is self.ax and self.ctrlPressed):
			#若没 press过， 或鼠标移出范围
			return
		# print('on_motion, self.ctrlPressed', self.ctrlPressed)
		curX=int(round(e.xdata))
		
#		if self.prevX is None or self.prevX is not curX:
		if self.prevX is not curX:
			print('self.prevX, self.startX, curX:', self.prevX, self.startX, curX)
			self.drawRectArea(self.startX, curX)
			self.prevX=curX	
		
	
	def drawRectArea(self, start, end):
		'''
		e 鼠标 event
		'''
		print('drawRectArea:', start, end)
		if self.rectBar:
#			print('------removing self.rectBar----:', self.rectBar)
#			print('id(self.rectBar):', id(self.rectBar))
			self.rectBar.remove()
			self.rectBar=None
			self.draw()	#卧槽忘了。。
		yBottom, yTop=self.ax.get_ylim()
		axHeight=yTop-yBottom
		width=end-start
#		print(width)
		if width is 0:
			print('width is 0')
			return
		self.rectBar, =self.ax.bar(start, axHeight, width, yBottom)
#		print('id(self.rectBar):', id(self.rectBar))
#		print(type(self.rectBar))
#		self.rectBar =self.ax.bar(start, axHeight, width, yBottom)
		self.rectBar.set_alpha(.5)
		self.draw()
		pass
	
	def resetAxis(self, title=None):
#		if self.rectBar:
#			self.rectBar=None
		self.rectBar=None
		self.startX=None
		self.prevX=None
		
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
		super(MatplotlibWidget, self).__init__(parent)
		self.canvas=MplCanvas()
		self.canvas.setFocusPolicy( QtCore.Qt.ClickFocus )
		self.canvas.setFocus()
		self.vbl=QtGui.QVBoxLayout(self)

		# 2013年9月1日11:18:50		试图加 toolbar
		from matplotlib.backends.backend_qt4 import NavigationToolbar2QT as NavigationToolbar
		self.vbl.addWidget(NavigationToolbar(self.canvas, self))
		self.vbl.addWidget(self.canvas)
		# self.setLayout(self.vbl)	#layout 用 self 初始化过
