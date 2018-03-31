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
        self._dir_list = None
        self._proContent = None
        self.getdirs()
        self._WidgetA = WidgetA(self)
        self._DialogB = DialogB()

        self.uiNew.triggered.connect(self.openA)
        self.uiLoad.triggered.connect(self.openB)
        self.uiMCTDHcalc.triggered.connect(self.openC)

        self.setList()

    def getContent(self):
        print self._newpath + ' from getContent'
        print os.getcwd()
        if os.path.exists(self._newpath):
            root, directories, filenames = os.walk('./'+self._newpath).next()
            self._proContent = directories
            print self._proContent
        else:
            print "path doesn't exists"

    def on_item_select2(self, item):
        key = item.data().toString()
        self._newpath = str(key)
        print self._newpath
        self.getContent()
        self.setList2()

    def setList2(self):
         #####ListModelPES#######
        self.modelPES = QtGui.QStandardItemModel(self.uiSessions)
        for key in self._proContent:
            item = QtGui.QStandardItem(key)
            self.modelPES.appendRow(item)
        self.uiSessions.setModel(self.modelPES)
        self.uiSessions.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)

    def setList(self):
         #####ListModelPES#######
        self.modelPES = QtGui.QStandardItemModel(self.uiProjects)
        for key in self._dir_list:
            item = QtGui.QStandardItem(key)
            self.modelPES.appendRow(item)
        self.uiProjects.setModel(self.modelPES)
        self.uiProjects.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.uiProjects.clicked.connect(self.on_item_select2)

        #####ListProject#######
#    def setList(self):
#        self._model = QtGui.QStandardItemModel(self.uiProjects)
#        for key in self._dir_list:
#            item = QtGui.QStandardItem(key)
#            self._model.appendRow(item)
#        self.uiProjects.setModel(self._model)
#        self.uiProjects.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
#        self.uiProjects.clicked.connect(self.on_item_select1)


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
#                self._DialogB = DialogB() #update object in order to get updated list

    def openB(self):
        self._newpath = str(QtGui.QFileDialog.getExistingDirectory(self))
        print self._newpath  + " from openB"
        self._newpath = self._newpath.split("/")[-1]
        self.getContent()
        self.setList2()


    def openC(self):
        print self._newpath + " from openC"
#        self._newpath = self._newpath.split("/")[-1]
        print self._newpath
        os.chdir("./" + self._newpath)  # !!!!!to uiMCTDHcalc
        print os.getcwd()
        dialog = self._WidgetA
        dialog.exec_()

if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    app.setStyle("cleanlooks")
    wnd =Main()
    wnd.show()
    sys.exit(app.exec_())
