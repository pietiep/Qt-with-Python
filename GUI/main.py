from PyQt4 import QtCore, QtGui, uic
from PyQt4 import *
import sys, os, re
from widgetA import WidgetA
from InputPro import ListModel, ListModel2
from dialogC import DialogC


base, form = uic.loadUiType("main.ui")

class Main(base, form):
    def __init__(self, parent=None):
        super(base, self).__init__(parent)
        self.setupUi(self)

        self._startingPath = os.getcwd()
        self._newpath = 'Project1'
        self._path2 = ''
        self._dir_list = None
        self._proContent = None

        self._model1 = None
        self._model2 = None

        self.getdirs()
        self._WidgetA = WidgetA(self)

        self.uiNew.triggered.connect(self.openA)
        self.uiLoad.triggered.connect(self.openB)
        self.uiMCTDHcalc.triggered.connect(self.openC)
        self.uiPlusBu.clicked.connect(self.openA)
        self.uiPlusBu2.clicked.connect(self.open0)
        self.uiPlusBu.clicked.connect(self.removeA)
        self.uiPlusBu2.clicked.connect(self.remove0)

        self.setList()

    def remove0(self):
        pass

    def removeA(self):
        pass        

    def getContent(self):
        print self._newpath, 'from getContent'
        if os.path.exists(self._newpath):
            root, directories, filenames = os.walk('./'+self._newpath).next()
            try:
                directories.remove('tmp')  #removes 'tmp' from list
            except ValueError as e:
                pass
            self._proContent = directories
        else:
            print "path doesn't exists"

    def on_item_select2(self, item):
        key = item.data().toString()
        newDir = str(key)
        os.chdir("/" + newDir)
        self.setList2()

    def on_item_select(self, item):
        os.chdir(self._startingPath)
        key = item.data().toString()
        self._newpath = str(key)
        self.getdirs()
        self.getContent()
        self.setList2()

    def setList2(self):
         #####ListModelPES#######
        self._model2 = ListModel2(self._newpath, self._proContent)
        self.uiSessions.setModel(self._model2)

    def setList(self):
         #####ListModelPES#######
        self._model1 = ListModel(self._dir_list)
        self.uiProjects.setModel(self._model1)
        self.uiProjects.clicked.connect(self.on_item_select)

    def getdirs(self):
            root, directories, filenames = os.walk(".").next()
            self._dir_list = [dirs for dirs in directories]

    def open0(self, warn):
        if warn == False:
            warn = ''
        dialogC = DialogC()
        print warn, 'from open0'
        dialogC.setWarning(str(warn))
        dialogC.exec_()
        self._path2 = str(dialogC._FolderName)

        if self._path2 != 'Cancel':
            path = os.getcwd() + '/' + self._newpath + '/' + self._path2
            print path, 'from open0'
            if not os.path.exists(path):
                try:
                    os.makedirs(path)
                except IOError as identifier:
                    print identifier
                self.getContent()
                self.setList2()
            else:
                print 'Folder already exists!'
                self.open0('Folder already exists!')

    def openA(self, warnings):
        if warnings == False:
            warnings = ''
        dialogC = DialogC()
        dialogC.setWarning(str(warnings))
        dialogC.exec_()
        self._newpath = str(dialogC._FolderName)

        if self._newpath != 'Cancel':
            path = os.getcwd() + '/' + self._newpath
            if not os.path.exists(path):
                try:

                    os.makedirs(path)
                except IOError as identifier:
                    print identifier
                self.getdirs()
                self.setList()
            else:
                print 'Folder already exists!'
                self.openA('Folder already exists!')

    def openB(self):
        self._newpath = str(QtGui.QFileDialog.getExistingDirectory(self))
        print self._newpath  + " from openB"
        self._newpath = self._newpath.split("/")[-1]
        self.getContent()
        self.setList2()

    def openC(self):
        print self._newpath + " from openC"
        os.chdir("./" + self._newpath) 
        dialog = self._WidgetA
        dialog.exec_()

if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    app.setStyle("cleanlooks")
    wnd =Main()
    wnd.show()
    sys.exit(app.exec_())
