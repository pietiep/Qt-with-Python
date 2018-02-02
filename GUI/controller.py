from ModelTree import ModelTree
from LogicalNodes import LogicalNodes
from View import View
from netw_embb_in_qt4 import ApplicationWindow
import sys
from PyQt4 import QtGui


class Controller(object):
    def __init__(self):
        self.model = ModelTree()
        self.model2 = LogicalNodes()
        self.view = View()
        self.G = None

    def berechne(self):
        pass
        #processing
        self.model.getLayerMatr()
        G = self.model2.Networkx(self.model.layer_matr)
        return G


C = Controller()
G = C.berechne()
print type(C.G)
C.G = G
print type(C.G)

app = QtGui.QApplication(sys.argv)

main = ApplicationWindow()
main.G = G
print type(main.G)
main.show()
sys.exit(app.exec_())
