# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'curveViewer.ui'
#
# Created: Mon Oct 14 10:57:22 2013
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
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.splitter_2 = QtGui.QSplitter(self.centralwidget)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName(_fromUtf8("splitter_2"))
        self.splitter = QtGui.QSplitter(self.splitter_2)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.scrollArea_2 = QtGui.QScrollArea(self.splitter)
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName(_fromUtf8("scrollArea_2"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 276, 197))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.scrollAreaWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setText(_fromUtf8("当前路径："))
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.labelDirOpened = QtGui.QLabel(self.scrollAreaWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelDirOpened.sizePolicy().hasHeightForWidth())
        self.labelDirOpened.setSizePolicy(sizePolicy)
        self.labelDirOpened.setObjectName(_fromUtf8("labelDirOpened"))
        self.horizontalLayout.addWidget(self.labelDirOpened)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.listWidgetFile = QtGui.QListWidget(self.scrollAreaWidgetContents)
        self.listWidgetFile.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.listWidgetFile.setObjectName(_fromUtf8("listWidgetFile"))
        self.verticalLayout.addWidget(self.listWidgetFile)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents)
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
        self.mplWidget.setGeometry(QtCore.QRect(0, 0, 338, 366))
        self.mplWidget.setObjectName(_fromUtf8("mplWidget"))
        self.scrollArea.setWidget(self.mplWidget)
        self.horizontalLayout_2.addWidget(self.splitter_2)
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
        self.actionVelocity = QtGui.QAction(MainWindow)
        self.actionVelocity.setCheckable(True)
        self.actionVelocity.setObjectName(_fromUtf8("actionVelocity"))
        self.actionDisplacement = QtGui.QAction(MainWindow)
        self.actionDisplacement.setCheckable(True)
        self.actionDisplacement.setObjectName(_fromUtf8("actionDisplacement"))
        self.actionLegend = QtGui.QAction(MainWindow)
        self.actionLegend.setCheckable(True)
        self.actionLegend.setChecked(True)
        self.actionLegend.setObjectName(_fromUtf8("actionLegend"))
        self.actionV_in_BF = QtGui.QAction(MainWindow)
        self.actionV_in_BF.setObjectName(_fromUtf8("actionV_in_BF"))
        self.actionGyro_in_BF = QtGui.QAction(MainWindow)
        self.actionGyro_in_BF.setObjectName(_fromUtf8("actionGyro_in_BF"))
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionExit)
        self.menuView.addAction(self.actionAccBodyFrame)
        self.menuView.addAction(self.actionAccWorldFrame)
        self.menuView.addAction(self.actionVelocity)
        self.menuView.addAction(self.actionDisplacement)
        self.menuView.addSeparator()
        self.menuView.addAction(self.actionLegend)
        self.menuView.addAction(self.actionV_in_BF)
        self.menuView.addAction(self.actionGyro_in_BF)
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
        self.actionAccBodyFrame.setText(_translate("MainWindow", "Acc(&B)odyFrame", None))
        self.actionAccBodyFrame.setShortcut(_translate("MainWindow", "Ctrl+B", None))
        self.actionAccWorldFrame.setText(_translate("MainWindow", "Acc(&W)orldFrame", None))
        self.actionAccWorldFrame.setShortcut(_translate("MainWindow", "Ctrl+W", None))
        self.actionVelocity.setText(_translate("MainWindow", "(&V)elocity", None))
        self.actionVelocity.setShortcut(_translate("MainWindow", "Ctrl+V", None))
        self.actionDisplacement.setText(_translate("MainWindow", "(&D)isplacement", None))
        self.actionDisplacement.setShortcut(_translate("MainWindow", "Ctrl+D", None))
        self.actionLegend.setText(_translate("MainWindow", "(&L)egend", None))
        self.actionLegend.setShortcut(_translate("MainWindow", "Ctrl+L", None))
        self.actionV_in_BF.setText(_translate("MainWindow", "V in BF", None))
        self.actionGyro_in_BF.setText(_translate("MainWindow", "(&G)yro in BF", None))
        self.actionGyro_in_BF.setShortcut(_translate("MainWindow", "Ctrl+G", None))

from matplotlibwidget import MatplotlibWidget
