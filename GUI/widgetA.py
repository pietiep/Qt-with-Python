from PyQt4 import QtCore, QtGui, uic
from PyQt4 import *
import sys
from Node import OutPut, Tree, Node, TransformNode, CameraNode, LightNode

base, form = uic.loadUiType("widgetA.ui")

class WidgetA(base, form):
    def __init__(self, parent=None):
        super(WidgetA, self).__init__(parent)
        self.setupUi(self)

        self.model = QtGui.QStandardItemModel(self.listHamilton)
        item = QtGui.QStandardItem("CH3")
        item.setCheckable(True)
        self.model.appendRow(item)
        item = QtGui.QStandardItem("NO3")
        item.setCheckable(True)
        self.model.appendRow(item)
        print dir(item)
        print dir(item.lastIndexOf)
        #output = QtCore.QDataStream()
    #    print self.model.item(0).read(output)
    #    print str(output)
        self.model.itemChanged.connect(self.on_item_changed)
        self.listHamilton.setModel(self.model)

    def on_item_changed(self, item):
        if not item.checkState():
            return
        output = QtCore.QDataStream()
    #    item.read(output)
    #    print output


if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    app.setStyle("cleanlooks")
    wnd =WidgetA()
    wnd.show()


    sys.exit(app.exec_())
