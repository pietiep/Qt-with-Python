from PyQt4 import QtCore, QtGui, uic
from PyQt4 import *
import sys, os
from widgetA import WidgetA

base, form = uic.loadUiType("dialogB.ui")

class DialogB(base, form):
    def __init__(self, parent=None):
        super(base, self).__init__(parent)
        self.setupUi(self)

        self._WidgetA = WidgetA(self)

    #    root, directories, filenames = os.walk(".").next()
        self._dir_list = None # [dirs for dirs in directories if "Project" in dirs]
        self._projectName = None

        #####ListProject#######
        self.setList()
        self.uiProjectlist.clicked.connect(self.on_item_select1)


            ####PushBottoms#####
        self.uiCancelB.clicked.connect(self.esc)
        self.uiLoadB.clicked.connect(self.LoadProject)

    def setList(self):
        self._model = QtGui.QStandardItemModel(self.uiProjectlist)
        root, directories, filenames = os.walk(".").next() ###does not recognize new folder
        self._dir_list = [dirs for dirs in directories if "Project" in dirs]
    #    print sorted(self._dir_list)
        for key in self._dir_list:
            item = QtGui.QStandardItem(key)
            self._model.appendRow(item)
        self.uiProjectlist.setModel(self._model)
        self.uiProjectlist.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)

    def LoadProject(self):
        self.close()
        os.chdir("./" + self._projectName)  # Change dir
        print os.getcwd() + ' from B'
    #    dialog = self._WidgetA

    def esc(self):
        self.close()

    def on_item_select1(self, item):
        self.setList()
    #    root, directories, filenames = os.walk(".").next()
    #    self._dir_list = [dirs for dirs in directories if "Project" in dirs]
        key = item.data().toString()
        self._projectName = str(key)
        print self._projectName + ' from B'

    def getnewpath(self):
        return self._projectName

if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    app.setStyle("cleanlooks")
    wnd = DialogB()
    wnd.show()
    sys.exit(app.exec_())
