from ModelTree import ModelTree
from LogicalNodes import LogicalNodes
from View import View
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtGui
import ui_MainWindow
import time

class ShowPng(QWidget):
    def __init__(self, parent=None):
        super(ShowPng, self).__init__(parent)
        self.setWindowTitle("MCTDH Tree")

        label = QLabel(self)
        pixmap = QPixmap('nx_test.png')
        label.setPixmap(pixmap)
        self.resize(pixmap.width(), pixmap.height())

class MainW(QMainWindow,
        ui_MainWindow.Ui_MCTDH):

    def __init__(self, parent=None):
        super(MainW, self).__init__(parent)
        self.setupUi(self)

        self.setConfig = None
        self.setSystem = None

        self.ModelTree = None # will be object of ModelTree()
#        self.LogicalNodes = LogicalNodes() #object
#        self.G = None # will be DiGraphs object

        self.connect(self.actionLoad_Configuration, SIGNAL("activated()"), self.BrowserCon)
        self.connect(self.actionLoad_System, SIGNAL("activated()"), self.BrowserSys)
        self.connect(self.actionMCTDH_Tree, SIGNAL("activated()"), self.Initialize)

        self.ShowPng = None

    def Initialize(self):

        if self.setConfig and self.setSystem is not None:

            self.ModelTree = ModelTree(str(self.setConfig),str(self.setSystem))

        else:

            self.ModelTree = ModelTree()

        self.LogicalNodes = LogicalNodes(self.ModelTree.lay_matr_mode) #object

#        self.ModelTree.getLayerMatr() #calculates list - layer_matr
#        self.G = self.LogicalNodes.Networkx(self.ModelTree.layer_matr) #connects nodes according to layer_matr
        self.View = View(self.ModelTree.label_mode, self.ModelTree.nodes_spf) #object
        self.View.Display(self.LogicalNodes.G) #View method Display() generated .png file
        self.ShowPng = ShowPng()
        self.ShowPng.show()

    def BrowserCon(self):
        self.setConfig = QFileDialog.getOpenFileName(self)

    def BrowserSys(self):
        self.setSystem = QFileDialog.getOpenFileName(self)

#C = Controller()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    app.setStyle("cleanLooks")
    u = MainW()
    u.show()
    app.exec_()
