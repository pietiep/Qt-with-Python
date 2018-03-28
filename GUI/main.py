from PyQt4 import QtCore, QtGui, uic
from PyQt4 import *
import sys, os, re
from widgetA import WidgetA
from dialogB import DialogB


base, form = uic.loadUiType("main.ui")

class Main(base, form):
    def __init__(self, parent=None):
        super(base, self).__init__(parent)
        self.setupUi(self)

        self._newpath = 'Project1'
        #self._newpath = None
        self._dir_list = None
        self.getdirs()
        self._DialogB = DialogB()

        self.uiNew.triggered.connect(self.openA)
        self.uiLoad.triggered.connect(self.openB)
        self.uiMCTDHcalc.triggered.connect(self.openC)

        self.setList()
    #    self.uiProjects.clicked.connect(self._DialogB.on_item_select1)

        #####ListProject#######
    def setList(self):
        self._model = QtGui.QStandardItemModel(self.uiProjects)
        for key in self._dir_list:
            item = QtGui.QStandardItem(key)
            self._model.appendRow(item)
        self.uiProjects.setModel(self._model)
        self.uiProjects.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.uiProjects.clicked.connect(self.on_item_select1)

        self.uiProjects.visualRect(item.index())

    def getdirs(self):
            root, directories, filenames = os.walk(".").next()
            self._dir_list = [dirs for dirs in directories if "Project" in dirs]


    def openA(self):
        self._WidgetA = WidgetA(self)
        if not os.path.exists(self._newpath):
            os.makedirs(self._newpath)
#            os.chdir("./" + self._newpath) !!!!!to uiMCTDHcalc
        else:
            self.getdirs()
            num_list = [int((re.findall(r'-?\d+\.?\d*', l_))[0]) #Regex
                        for l_ in self._dir_list]
            self._newpath = "Project" + str(int(max(num_list))+1)
            if not os.path.exists(self._newpath):
                os.makedirs(self._newpath)
                self.getdirs()
                self.setList()
                self._DialogB = DialogB() #update object in order to get updated list

    def openB(self):
        #dialog = self._DialogB
        #dialog.exec_()
        #self._newpath = QtGui.QFileDialog.getOpenFileName(self)
        self._newpath = QtGui.QFileDialog.getExistingDirectory(self)
        print self._newpath
    #    print "here is main: "+self._newpath


    def openC(self):
        os.chdir("./" + self._newpath)  # !!!!!to uiMCTDHcalc
        print os.getcwd()
        dialog = self._WidgetA
        dialog.exec_()

    def on_item_select1(self, item):
        self.setList()
    #    self.getdirs()
        key = item.data().toString()
        self._projectName = str(key)
    #    print type(item)
    #    print os.getcwd() + 'from main select1'

if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    app.setStyle("cleanlooks")
    wnd =Main()
    wnd.show()
    sys.exit(app.exec_())
