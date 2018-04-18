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
        self._modelProxy1 = QtGui.QSortFilterProxyModel()
        self._modelProxy2 = QtGui.QSortFilterProxyModel()
        self._itemIndex1 = None
        self._itemIndex2 = None
        self._itemProxyIndex1 = None
        self._itemProxyIndex2 = None

        self.getdirs()
        self._WidgetA = WidgetA(self)

        self.setList()
        self.uiNew.triggered.connect(self.openA)
        self.uiLoad.triggered.connect(self.openB)
        self.uiMCTDHcalc.triggered.connect(self.openC)
        self.uiPlusBu.clicked.connect(self.openA)
        self.uiPlusBu2.clicked.connect(self.open0)
        self.uiMinusBu.clicked.connect(self.removeA)
        self.uiMinusBu2.clicked.connect(self.remove0)

        self.setList()

    def remove0(self):
        rowNum = self._itemIndex2.row()
        key = str(self._itemIndex2.data().toString())
        self._model2.removeRows(rowNum,0)
        if self._model2._messageBu == 'OK':
            print 'delete %s' %key        
            shutil.rmtree(self._startingPath+'/'+self._newpath+'/'+key)

    def removeA(self):
        rowNum = self._itemIndex1.row()
        rowNumProxy = self._itemProxyIndex1.row()
        print rowNum, 'data', rowNumProxy, 'proxy'
        key = str(self._itemIndex1.data().toString())
        startingpath2 = self._startingPath + '/'
        delFolder = startingpath2 + key
        self._model1.removeRows(rowNum,0)
        if self._model1._messageBu == 'OK' and delFolder != self._startingPath and delFolder != startingpath2:
#            selIndexes = self.uiProjects.selectedIndexes()

            print 'delete %s' %key
            shutil.rmtree(self._startingPath+'/'+key)
            self.getdirs()
            self.setList()

    def getContent(self):
        print self._newpath, 'from getContent'
        if os.path.exists(self._newpath):
            root, directories, filenames = os.walk('./'+self._newpath).next()
            try:
                directories.remove('tmp')  #removes 'tmp' from list
            except ValueError:
                pass
            self._proContent = directories
        else:
            print "path doesn't exists"


    def on_item_select(self, index):
        self._itemProxyIndex1 = index   #index from Proxy
        model = index.model()          # model = ProxyModel
        if hasattr(model, 'mapToSource'):
            index = model.mapToSource(index)
        self._itemIndex1 = index
        os.chdir(self._startingPath)
        self._newpath = str(index.data().toString())
        self.getdirs()
        self.getContent()
        self.setList2()

    def setList2(self):
         #####ListModelPES#######
        self._model2 = ListModel2(self._newpath, self._proContent)
        self.uiSessions.setModel(self._model2)
        indices = self.uiSessions.selectionModel().selectedIndexes()
        if not indices:
            index = self._model2.index(0,0)
            self._itemIndex2 = index
            self.uiSessions.selectionModel().select(index, QtGui.QItemSelectionModel.Select)

    def setList(self):
         #####ListModelPES#######
        self._model1 = ListModel(self._dir_list)
        self._modelProxy1.setSourceModel(self._model1)
        self._modelProxy1.setDynamicSortFilter(True)
        self.uiProjects.setModel(self._modelProxy1)
        self._modelProxy1.sort(0, QtCore.Qt.AscendingOrder)
        indices = self.uiProjects.selectionModel().selectedIndexes()
        if not indices:
            index = self._model1.index(0,0)
            self._itemIndex1 = index
            self._itemProxyIndex1 = index
            self.uiProjects.selectionModel().select(index, QtGui.QItemSelectionModel.Select)
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
