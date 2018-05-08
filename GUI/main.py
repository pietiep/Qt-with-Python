from PyQt4 import QtGui, uic
import sys, os, shutil
from widgetA import WidgetA
from InputPro import ListModel, ListModel2
from dialogC import DialogC


base, form = uic.loadUiType("main.ui")

class Main(base, form):
    def __init__(self, parent=None):
        super(base, self).__init__(parent)
        self.setupUi(self)

        self._HamiltonianDir = os.getcwd() + '/' + 'Hamiltonians'
        os.chdir('Projects')
        self._startingPath = os.getcwd()
        self._ProjectName = None
        self._path2 = None
        self._dir_list = None
        self._proContent = []

        self._model1 = None
        self._model2 = None
        self._itemIndex1 = None
        self._itemIndex2 = None

        self.getdirs()
        self._WidgetA = WidgetA(self)
        self._WidgetA._HamiltonianDir = self._HamiltonianDir
        self._WidgetA._startingPath = self._startingPath

        self.setList()
        self.uiNew.triggered.connect(self.openA)
        self.uiLoad.triggered.connect(self.openB)
        self.uiMCTDHcalc.triggered.connect(self.openD)
        self.uiPlusBu.clicked.connect(self.openA)
        self.uiPlusBu2.clicked.connect(self.open0)
        self.uiMinusBu.clicked.connect(self.removeA)
        self.uiMinusBu2.clicked.connect(self.remove0)

        # self.setList()
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
        session = str(self._itemIndex2.data().toString())
        self.showdialog(session)
        if 'OK' in self._messageBu:
            self._model2.removeRows(rowNum,1, self._itemIndex2)

            shutil.rmtree(self._startingPath+'/'+self._ProjectName+'/'+session)

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
        if os.path.exists(self._ProjectName):
            directories = os.walk('./'+self._ProjectName).next()[1]
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
        self._ProjectName = projectFolder

        os.chdir(self._ProjectName)
        self._WidgetA._ProjectName = projectFolder
        self._WidgetA.makedir()
        self._WidgetA.editSession(sessionFolder)
        self._WidgetA.setSessionName(sessionFolder)
        self._WidgetA.start()
        self._WidgetA.removeContent()
        self.openC()
        os.chdir('./')

    def on_item_select(self, index):
        """clicked Event on Items belonging to ListModel()"""
        self._itemIndex1 = index
        self._ProjectName = str(index.data().toString())
        self._WidgetA._ProjectName = self._ProjectName
        self._WidgetA._SessionName = None
        self._WidgetA.clearSession()
        self.getdirs()
        self.setList2()

    def setList2(self):
    #####ListModelPES#######
        self.getContent()
        self._model2 = ListModel2(self._ProjectName, self._proContent)
        self.uiSessions.setModel(self._model2)
        indices = self.uiSessions.selectionModel().selectedIndexes()
        if not indices:
            index = self._model2.index(0,0)
            self._itemIndex2 = index
            self.uiSessions.selectionModel().select(index, QtGui.QItemSelectionModel.Select)
            self._path2 = str(self._itemIndex2.data().toString())

    def setList(self):
    #####ListModelPES#######
        self.getdirs() #updates self._dir_list 
        self._model1 = ListModel(self._dir_list)
        self.uiProjects.setModel(self._model1)
        indices = self.uiProjects.selectionModel().selectedIndexes()
        if not indices:
            index = self._model1.index(0,0)
            self._ProjectName = str(index.data().toString())
            self._WidgetA._ProjectName = self._ProjectName
            self._itemIndex1 = index
            self._itemProxyIndex1 = index
            self.uiProjects.selectionModel().select(index, QtGui.QItemSelectionModel.Select)

    def getdirs(self):
            directories = os.walk(self._startingPath).next()[1]
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
            path = self._startingPath + '/' + self._ProjectName + '/' + self._path2
            if not os.path.exists(path):
                try:
                    os.chdir(self._startingPath+'/'+self._ProjectName)
                    os.makedirs(self._path2)
                    os.chdir(self._startingPath)
                except IOError as identifier:
                    print dir(identifier)
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
        self._ProjectName = str(dialogC._FolderName)

        if self._ProjectName != 'Cancel':
            path = self._startingPath + '/' + self._ProjectName
#            print path, 'before path.exists'
            if not os.path.exists(path):
                try:
                    os.makedirs(path)
                    os.makedirs(path+'/tmp')
                except IOError as identifier:
                    print identifier
#                self.getdirs()
                self.setList()
            else:
                print 'Folder already exists!'
                self.openA('Folder already exists!')

    def openB(self):
        self._ProjectName = str(QtGui.QFileDialog.getExistingDirectory(self))
        self._ProjectName = self._ProjectName.split("/")[-1]
        self.getContent()
        self.setList2()

    def openC(self):
        dialog = self._WidgetA
        dialog.exec_()

    def openD(self):
        self._WidgetA.clearSession()
        self._WidgetA.setSessionName(None)
        self._WidgetA.removeContent()

        self.openC()

if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    app.setStyle("cleanlooks")
    wnd =Main()
    wnd.show()
    sys.exit(app.exec_())
