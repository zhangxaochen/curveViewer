# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'curveViewer.ui'
#
# Created: Thu Apr 11 20:51:43 2013
#      by: PyQt4 UI code generator 4.10
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(641, 431)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.splitterH = QtGui.QSplitter(self.centralwidget)
        self.splitterH.setOrientation(QtCore.Qt.Horizontal)
        self.splitterH.setObjectName(_fromUtf8("splitterH"))
        self.splitterV = QtGui.QSplitter(self.splitterH)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitterV.sizePolicy().hasHeightForWidth())
        self.splitterV.setSizePolicy(sizePolicy)
        self.splitterV.setMinimumSize(QtCore.QSize(100, 0))
        self.splitterV.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.splitterV.setOrientation(QtCore.Qt.Vertical)
        self.splitterV.setObjectName(_fromUtf8("splitterV"))
        self.listWidgetNode = QtGui.QListWidget(self.splitterV)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listWidgetNode.sizePolicy().hasHeightForWidth())
        self.listWidgetNode.setSizePolicy(sizePolicy)
        self.listWidgetNode.setObjectName(_fromUtf8("listWidgetNode"))
        self.listWidgetData = QtGui.QListWidget(self.splitterV)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.listWidgetData.sizePolicy().hasHeightForWidth())
        self.listWidgetData.setSizePolicy(sizePolicy)
        self.listWidgetData.setObjectName(_fromUtf8("listWidgetData"))
        self.scrollArea = QtGui.QScrollArea(self.splitterH)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setMinimumSize(QtCore.QSize(0, 0))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.mplWidget = MatplotlibWidget()
        self.mplWidget.setGeometry(QtCore.QRect(0, 0, 360, 366))
        self.mplWidget.setObjectName(_fromUtf8("mplWidget"))
        self.scrollArea.setWidget(self.mplWidget)
        self.horizontalLayout.addWidget(self.splitterH)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 641, 23))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtGui.QAction(MainWindow)
        self.actionOpen.setObjectName(_fromUtf8("actionOpen"))
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.actionExit, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.menuFile.setTitle(_translate("MainWindow", "&File", None))
        self.actionOpen.setText(_translate("MainWindow", "(&O)pen", None))
        self.actionOpen.setToolTip(_translate("MainWindow", "Open a XML file", None))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O", None))
        self.actionExit.setText(_translate("MainWindow", "E(&x)it", None))
        self.actionExit.setToolTip(_translate("MainWindow", "E(x)it", None))
        self.actionExit.setShortcut(_translate("MainWindow", "Ctrl+Q", None))

from matplotlibwidget import MatplotlibWidget
