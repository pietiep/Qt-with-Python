from PyQt4 import QtCore, QtGui, uic
from PyQt4 import *
import sys
from widgetA import WidgetA
from dialogB import DialogB

base, form = uic.loadUiType("main.ui")

class Main(base, form):
    def __init__(self, parent=None):
        super(base, self).__init__(parent)
        self.setupUi(self)

        self._newpath = 'Project1'

        self._WidgetA = WidgetA(self)
        self._DialogB = DialogB()
        self.uiNew.triggered.connect(self.openA)
        self.uiLoad.triggered.connect(self.openB)

    def openA(self):
        import os
        if not os.path.exists(self._newpath):
            os.makedirs(self._newpath)
            os.chdir("./" + self._newpath)
        else:
            root, directories, filenames = os.walk(".").next()
            dir_list = [dirs for dirs in directories if "Project" in dirs]
            num_list = [l_[-1] for l_ in dir_list]
            newProject = "Project" + str(int(max(num_list))+1)
            if not os.path.exists(newProject):
                os.makedirs(newProject)
                os.chdir("./" + newProject)  # Change dir


        dialog = self._WidgetA
        if dialog.exec_() == QtGui.QDialog.Accepted:
            print 'bla'
        else:
            print 'cancelled'
        dialog.deleteLater()

    def openB(self):
        dialog = self._DialogB
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
