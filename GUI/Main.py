from PyQt4 import QtCore, QtGui, uic
from PyQt4 import *
import sys
from widgetA import WidgetA

base, form = uic.loadUiType("main.ui")

class WToDia(QtGui.QDialog):
    def __init__(self, parent=None):
        super(WToDia, self).__init__(parent)
        self.widgetA = WidgetA(self)

class Main(base, form):
    def __init__(self, parent=None):
        super(base, self).__init__(parent)
        self.setupUi(self)

        self.WidgetA = WidgetA(self)
        self.uiNew.triggered.connect(self.openA)

    def openA(self):
        dialog = self.WidgetA
        if dialog.exec_() == QtGui.QDialog.Accepted:
            print 'bla'
        else:
            print 'cancelled'
        dialog.deleteLater()



if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    app.setStyle("cleanlooks")
    wnd =Main()
    wnd.show()
    sys.exit(app.exec_())
