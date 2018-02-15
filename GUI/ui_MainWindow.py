# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created: Thu Feb 15 18:29:41 2018
#      by: PyQt4 UI code generator 4.10.4
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

class Ui_MCTDH(object):
    def setupUi(self, MCTDH):
        MCTDH.setObjectName(_fromUtf8("MCTDH"))
        MCTDH.resize(800, 600)
        self.centralwidget = QtGui.QWidget(MCTDH)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        MCTDH.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MCTDH)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuView_MCTDH_Tree = QtGui.QMenu(self.menubar)
        self.menuView_MCTDH_Tree.setObjectName(_fromUtf8("menuView_MCTDH_Tree"))
        MCTDH.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MCTDH)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MCTDH.setStatusBar(self.statusbar)
        self.actionLoad_Configuration = QtGui.QAction(MCTDH)
        self.actionLoad_Configuration.setObjectName(_fromUtf8("actionLoad_Configuration"))
        self.actionLoad_System = QtGui.QAction(MCTDH)
        self.actionLoad_System.setObjectName(_fromUtf8("actionLoad_System"))
        self.actionMCTDH_Tree = QtGui.QAction(MCTDH)
        self.actionMCTDH_Tree.setObjectName(_fromUtf8("actionMCTDH_Tree"))
        self.menuFile.addAction(self.actionLoad_Configuration)
        self.menuFile.addAction(self.actionLoad_System)
        self.menuView_MCTDH_Tree.addAction(self.actionMCTDH_Tree)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuView_MCTDH_Tree.menuAction())

        self.retranslateUi(MCTDH)
        QtCore.QMetaObject.connectSlotsByName(MCTDH)

    def retranslateUi(self, MCTDH):
        MCTDH.setWindowTitle(_translate("MCTDH", "MainWindow", None))
        self.menuFile.setTitle(_translate("MCTDH", "File", None))
        self.menuView_MCTDH_Tree.setTitle(_translate("MCTDH", "View", None))
        self.actionLoad_Configuration.setText(_translate("MCTDH", "Load Configuration", None))
        self.actionLoad_System.setText(_translate("MCTDH", "Load System", None))
        self.actionMCTDH_Tree.setText(_translate("MCTDH", "MCTDH Tree", None))

