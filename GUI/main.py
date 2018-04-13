from PyQt4 import QtCore, QtGui, uic
from PyQt4 import *
import sys, os, re
from widgetA import WidgetA
from InputPro import ListModel, ListModel2


base, form = uic.loadUiType("main.ui")

class Main(base, form):
    def __init__(self, parent=None):
        super(base, self).__init__(parent)
        self.setupUi(self)

        self._startingPath = os.getcwd()
        self._newpath = 'Project1'
        self._dir_list = None
        self._proContent = None

        self._model1 = None
        self._model2 = None

        self.getdirs()
        self._WidgetA = WidgetA(self)
#        self._DialogB = DialogB()

        self.uiNew.triggered.connect(self.openA)
        self.uiLoad.triggered.connect(self.openB)
        self.uiMCTDHcalc.triggered.connect(self.openC)

        self.setList()

    def getContent(self):
    #    print self._newpath + ' from getContent'
    #    print os.getcwd()
        if os.path.exists(self._newpath):
            root, directories, filenames = os.walk('./'+self._newpath).next()
            try:
                directories.remove('tmp')  #removes 'tmp' from list
            except ValueError as e:
                pass
            self._proContent = directories
        #    print self._proContent, 'from getContent'
        else:
            print "path doesn't exists"

    def on_item_select2(self, item):
#        key = self._model1.getValue()
        key = item.data().toString()
        print key
        newDir = str(key)
        os.chdir("/" + newDir)
#        self.getdirs()
#        print self._dir_list
#        self.getContent()
        self.setList2()

    def on_item_select(self, item):
#        key = self._model1.getValue()
        os.chdir(self._startingPath)
        print  'from ListModel2', os.getcwd()
        key = item.data().toString()
        print key
        self._newpath = str(key)
        self.getdirs()
#        print self._dir_list
        self.getContent()
        self.setList2()

    def setList2(self):
         #####ListModelPES#######
        self._model2 = ListModel2(self._newpath, self._proContent)
#        self.modelPES = QtGui.QStandardItemModel(self.uiSessions)
#        for key in self._proContent:
#            item = QtGui.QStandardItem(key)
#            self.modelPES.appendRow(item)
        self.uiSessions.setModel(self._model2)
#        self.uiSessions.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
#        self.uiProjects.clicked.connect(self.on_item_select2)

    def setList(self):
         #####ListModelPES#######
        self._model1 = ListModel(self._dir_list)
        self.uiProjects.setModel(self._model1)
#         self.modelPES = QtGui.QStandardItemModel(self.uiProjects)
#        for key in self._dir_list:
#            item = QtGui.QStandardItem(key)
#            self.modelPES.appendRow(item)
#        self.uiProjects.setModel(self.modelPES)
#        self.uiProjects.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.uiProjects.clicked.connect(self.on_item_select)

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
#            self._dir_list = [dirs for dirs in directories if "Project" in dirs]
            self._dir_list = [dirs for dirs in directories]



    def openA(self):
        self._WidgetA = WidgetA(self)
        if not os.path.exists(self._newpath):
            os.makedirs(self._newpath)
#            os.chdir("./" + self._newpath) !!!!!to uiMCTDHcalc
        else:
            self.getdirs()
            print self._dir_list
            num_list = [(re.findall(r'-?\d+\.?\d*', l_)) for l_ in self._dir_list]
            num_list = [int(l_[0]) for l_ in num_list if l_ != []] #removes empty lists
            self._newpath = "Project" + str(int(max(num_list))+1)
            if not os.path.exists(self._newpath):
                os.makedirs(self._newpath)
                self.getdirs()
                self.setList()

    def openB(self):
        self._newpath = str(QtGui.QFileDialog.getExistingDirectory(self))
        print self._newpath  + " from openB"
        self._newpath = self._newpath.split("/")[-1]
        self.getContent()
        self.setList2()


    def openC(self):
        print self._newpath + " from openC"
#        self._newpath = self._newpath.split("/")[-1]
#        print self._newpath
        os.chdir("./" + self._newpath)  # !!!!!to uiMCTDHcalc
#        print os.getcwd()
        dialog = self._WidgetA
        dialog.exec_()

if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    app.setStyle("cleanlooks")
    wnd =Main()
    wnd.show()
    sys.exit(app.exec_())
