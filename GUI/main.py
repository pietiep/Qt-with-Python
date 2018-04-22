from PyQt4 import QtGui, uic, QtCore
import sys, os, shutil
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
        self._itemIndex1 = None
        self._itemIndex2 = None

        self.getdirs()
        self._WidgetA = WidgetA(self)
        self._WidgetA._startingPath = self._startingPath

        self.setList()
        self.uiNew.triggered.connect(self.openA)
        self.uiLoad.triggered.connect(self.openB)
        self.uiMCTDHcalc.triggered.connect(self.openC)
        self.uiPlusBu.clicked.connect(self.openA)
        self.uiPlusBu2.clicked.connect(self.open0)
        self.uiMinusBu.clicked.connect(self.removeA)
        self.uiMinusBu2.clicked.connect(self.remove0)

        self.setList()
        self.uiProjects.clicked.connect(self.on_item_select)
        self.uiProjects.customContextMenuRequested.connect(self.openMenu)

        self.setList2()
        self.uiSessions.clicked.connect(self.on_item_select0)
        self.uiSessions.customContextMenuRequested.connect(self.openMenu0)

        self._messageBu = None

    def openMenu0(self, position):
        """Context menu"""
        menu = QtGui.QMenu()
        renameAction = menu.addAction("Rename")
        action = menu.exec_(self.uiSessions.mapToGlobal(position))
        if action == renameAction:
            self.uiSessions.edit(self._itemIndex2)

    def openMenu(self, position):
        """Context menu"""
        menu = QtGui.QMenu()
        renameAction = menu.addAction("Rename")
        action = menu.exec_(self.uiProjects.mapToGlobal(position))
        if action == renameAction:
            self.uiProjects.edit(self._itemIndex1)

    def remove0(self):
        """Removes Rows from ListModel2()"""
        rowNum = self._itemIndex2.row()
        key = str(self._itemIndex2.data().toString())
        self.showdialog(key)
        if 'OK' in self._messageBu:
            self._model2.removeRows(rowNum,1, self._itemIndex2)
            print os.getcwd(), 'before rmtree'
            self._newpath
            shutil.rmtree(self._newpath)

    def removeA(self):
        """Removes Rows from ListModel()"""
        rowNum = self._itemIndex1.row()
        key = str(self._itemIndex1.data().toString())
        startingpath2 = self._startingPath + '/'
        delFolder = startingpath2 + key

        self._model1.removeRows(rowNum,1, self._itemIndex1)

        if self._model1._messageBu == 'OK' and delFolder != self._startingPath and delFolder != startingpath2:
            shutil.rmtree(self._startingPath+'/'+key)

            maxRow = self._model2.rowCount(self._itemIndex2)
            if maxRow != 0:
                self._model2.removeRows(0, maxRow)
#            index = self._model1.index(0,0)
#           self.uiProjects.selectionModel().select(index, QtGui.QItemSelectionModel.Select)

    def showdialog(self, value):
        msg = QtGui.QMessageBox()
        msg.setIcon(QtGui.QMessageBox.Warning)

        msg.setText("Are sure you want to delete Folder %s?" %value)
        msg.setStandardButtons(QtGui.QMessageBox.Ok| QtGui.QMessageBox.Cancel)

        msg.buttonClicked.connect(self.msgbtn)
        msg.exec_()

    def msgbtn(self, i):
        self._messageBu = str(i.text())

    def getContent(self):
        os.chdir(self._startingPath)
        if os.path.exists(self._newpath):
            root, directories, filenames = os.walk('./'+self._newpath).next()
            try:
                directories.remove('tmp')  #removes 'tmp' from list
            except ValueError:
                pass
            self._proContent = sorted(directories)
        else:
            print "path doesn't exists"

    def on_item_select0(self, index):
        """clicked Event on Items belonging to ListModel2()"""
        os.chdir(self._startingPath)
        projectFolder = str(self._itemIndex1.data().toString())
        sessionFolder = str(index.data().toString())
#        print projectFolder, sessionFolder
        self._itemIndex2 = index
        self._newpath = self._startingPath + '/' + projectFolder + '/' + sessionFolder
#        print self._newpath

        os.chdir(self._newpath)
        self._WidgetA._ProjectName = projectFolder
        self._WidgetA.editSession(sessionFolder)
        self.openC()
        os.chdir('./')
#        print os.getcwd(), 'after OC'

    def on_item_select(self, index):
        """clicked Event on Items belonging to ListModel()"""
        self._itemIndex1 = index
        self._newpath = str(index.data().toString())
        self._WidgetA._ProjectName = self._newpath
        self._WidgetA._SessionName = None
        self._WidgetA.clearSession()
        self.getdirs()
        self.setList2()

    def setList2(self):
         #####ListModelPES#######
        self.getContent()
        self._model2 = ListModel2(self._newpath, self._proContent)
        self.uiSessions.setModel(self._model2)
        indices = self.uiSessions.selectionModel().selectedIndexes()
        if not indices:
            index = self._model2.index(0,0)
            self._itemIndex2 = index
            self.uiSessions.selectionModel().select(index, QtGui.QItemSelectionModel.Select)

    def setList(self):
         #####ListModelPES#######
        self.getdirs() #updates self._dir_list 
        self._model1 = ListModel(self._dir_list)
 #       self._modelProxy1.setSourceModel(self._model1)
#        self.uiProjects.setModel(self._modelProxy1)
        self.uiProjects.setModel(self._model1)
#        self.uiProjects.clicked.connect(self.on_item_select)
#        self._modelProxy1.sort(0, QtCore.Qt.AscendingOrder)
        indices = self.uiProjects.selectionModel().selectedIndexes()
        if not indices:
            index = self._model1.index(0,0)
            self._newpath = str(index.data().toString())
            self._itemIndex1 = index
            self._itemProxyIndex1 = index
            self.uiProjects.selectionModel().select(index, QtGui.QItemSelectionModel.Select)

    def getdirs(self):
            path = self._startingPath
            root, directories, filenames = os.walk(self._startingPath).next()
            self._dir_list = [dirs for dirs in directories]
            self._dir_list = sorted(self._dir_list)

    def open0(self, warn):
        if warn == False:
            warn = ''
        dialogC = DialogC()
        dialogC.setWarning(str(warn))
        dialogC.exec_()
        self._path2 = str(dialogC._FolderName)

        if self._path2 != 'Cancel':
            path = os.getcwd() + '/' + self._newpath + '/' + self._path2
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
#            path = os.getcwd() + '/' + self._newpath
            path = self._startingPath + '/' + self._newpath
#            print path, 'before path.exists'
            if not os.path.exists(path):
                try:

                    os.makedirs(path)
                except IOError as identifier:
                    print identifier
#                self.getdirs()
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
#        print self._newpath + " from openC"
#        os.chdir("./" + self._newpath) 
#        print os.getcwd(), 'before WA'
        dialog = self._WidgetA
#        print os.getcwd(), 'after WA'
        dialog.exec_()

if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    app.setStyle("cleanlooks")
    wnd =Main()
    wnd.show()
    sys.exit(app.exec_())
