# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'curveViewer.ui'
#
# Created: Tue May 21 21:37:34 2013
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
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.splitter_2 = QtGui.QSplitter(self.centralwidget)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName(_fromUtf8("splitter_2"))
        self.splitter = QtGui.QSplitter(self.splitter_2)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.layoutWidget = QtGui.QWidget(self.splitter)
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setText(_fromUtf8("当前路径："))
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.labelDirOpened = QtGui.QLabel(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelDirOpened.sizePolicy().hasHeightForWidth())
        self.labelDirOpened.setSizePolicy(sizePolicy)
        self.labelDirOpened.setObjectName(_fromUtf8("labelDirOpened"))
        self.horizontalLayout.addWidget(self.labelDirOpened)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.listWidgetFile = QtGui.QListWidget(self.layoutWidget)
        self.listWidgetFile.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.listWidgetFile.setObjectName(_fromUtf8("listWidgetFile"))
        self.verticalLayout.addWidget(self.listWidgetFile)
        self.listWidgetNode = QtGui.QListWidget(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listWidgetNode.sizePolicy().hasHeightForWidth())
        self.listWidgetNode.setSizePolicy(sizePolicy)
        self.listWidgetNode.setObjectName(_fromUtf8("listWidgetNode"))
        self.scrollArea = QtGui.QScrollArea(self.splitter_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setMinimumSize(QtCore.QSize(0, 0))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.mplWidget = MatplotlibWidget()
        self.mplWidget.setGeometry(QtCore.QRect(0, 0, 358, 366))
        self.mplWidget.setObjectName(_fromUtf8("mplWidget"))
        self.scrollArea.setWidget(self.mplWidget)
        self.verticalLayout_2.addWidget(self.splitter_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 641, 23))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuView = QtGui.QMenu(self.menubar)
        self.menuView.setObjectName(_fromUtf8("menuView"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtGui.QAction(MainWindow)
        self.actionOpen.setObjectName(_fromUtf8("actionOpen"))
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.actionSave = QtGui.QAction(MainWindow)
        self.actionSave.setObjectName(_fromUtf8("actionSave"))
        self.actionAccBodyFrame = QtGui.QAction(MainWindow)
        self.actionAccBodyFrame.setCheckable(True)
        self.actionAccBodyFrame.setChecked(True)
        self.actionAccBodyFrame.setObjectName(_fromUtf8("actionAccBodyFrame"))
        self.actionAccWorldFrame = QtGui.QAction(MainWindow)
        self.actionAccWorldFrame.setCheckable(True)
        self.actionAccWorldFrame.setObjectName(_fromUtf8("actionAccWorldFrame"))
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionExit)
        self.menuView.addAction(self.actionAccBodyFrame)
        self.menuView.addAction(self.actionAccWorldFrame)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuView.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.actionExit, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.labelDirOpened.setText(_translate("MainWindow", "N/a", None))
        self.menuFile.setTitle(_translate("MainWindow", "&File", None))
        self.menuView.setTitle(_translate("MainWindow", "&View", None))
        self.actionOpen.setText(_translate("MainWindow", "(&O)pen", None))
        self.actionOpen.setToolTip(_translate("MainWindow", "Open a XML file", None))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O", None))
        self.actionExit.setText(_translate("MainWindow", "E(&x)it", None))
        self.actionExit.setToolTip(_translate("MainWindow", "E(x)it", None))
        self.actionExit.setShortcut(_translate("MainWindow", "Ctrl+Q", None))
        self.actionSave.setText(_translate("MainWindow", "(&S)ave", None))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S", None))
        self.actionAccBodyFrame.setText(_translate("MainWindow", "AccBodyFrame", None))
        self.actionAccBodyFrame.setShortcut(_translate("MainWindow", "Alt+A, B", None))
        self.actionAccWorldFrame.setText(_translate("MainWindow", "AccWorldFrame", None))
        self.actionAccWorldFrame.setShortcut(_translate("MainWindow", "Alt+A, W", None))

from matplotlibwidget import MatplotlibWidget
