'''
Created on Apr 11, 2013

@author: zhangxaochen
'''
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PyQt4 import QtGui

class MplCanvas(FigureCanvasQTAgg):
	def __init__(self):
		self.fig=Figure()
		self.ax=self.fig.add_subplot(111)
		
		super().__init__(self.fig)
#		super().
		self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
		self.updateGeometry()
		
	
class MatplotlibWidget(QtGui.QWidget):

	def __init__(self, parent=None):
		super().__init__(parent)
		self.canvas=MplCanvas()
		self.vbl=QtGui.QVBoxLayout()
		self.vbl.addWidget(self.canvas)
		self.setLayout(self.vbl)
		
		
		
		
		