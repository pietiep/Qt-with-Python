from ModelTree import ModelTree
from LogicalNodes import LogicalNodes
from View import View
#from netw_embb_in_qt4 import ApplicationWindow
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import ui_MainWindow


class Controller(object):
    def __init__(self):
        self.model = ModelTree()
        self.model2 = LogicalNodes()
        self.view = View()
        self.berechne()

    def berechne(self):
        pass
        #processing
        self.model.getLayerMatr()
        G = self.model2.Networkx(self.model.layer_matr)
        self.view.Display(G) #View method Display() generated .png file

class MainW(QMainWindow,
        ui_MainWindow.Ui_MCTDH):

    def __init__(self, parent=None):
        super(MainW, self).__init__(parent)
        self.setupUi(self)

app = QApplication(sys.argv)
Form = MainW()
Form.show()
app.exec_()
#C = Controller()
