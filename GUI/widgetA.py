from PyQt4 import QtCore, QtGui, uic
#from PyQt4 import *
import sys
from Node import OutPut, Tree
from Node import InPut
from InputTree import SceneGraphModel
from ModelTree import ModelTree
from LogicalNodes import LogicalNodes
from View import View
import os, shutil

base, form = uic.loadUiType("dialogA.ui")

class WidgetA(base, form):
    def __init__(self, parent=None):
        super(WidgetA, self).__init__(parent)
        self.setupUi(self)

        self._HamiltonianDir = None


        ########Attributes######
        self._paradict = {}
        self._eps = []
        self._integrator = []

#        self.getInput()


        self._tree = None
#        self._tree = Tree("36")  #Delegation instead of inheritance of Tree
#        self._treeData = self._tree._treeData

        self._dictHamil = {'CH3': '194', 'NO3': '195'}
        self._dictPES = {'CH3': '100', 'NO3': '101'}
        self._mctdhConfig = None 
        self._sysTreeFile = None
        self._inputFile = None
        # self._TMPmctdhConfig = None
        # self._TMPsysTreeFile = None
        # self._TMPinputFile = None
        self._SESmctdhConfig = None
        self._SESsysTreeFile = None
        self._SESinputFile = None
        self._TMPmctdhConfig = None
        self._TMPsysTreeFile = None
        self._TMPinputFile = None
        self._dest = None


        self._startingPath = None
        self._ProjectName = None
        self._SessionName = None
        self._temporarySES = None
        self._messagebut = None

        #####LineEdit:Projectname#######
        self.uiProjectName.textChanged.connect(self.change0)

        #####TextEdit:TreeFile#######
        self.uiTreeText.setReadOnly(True)

        #####ListModelHamilton#######
        self._model = QtGui.QStandardItemModel(self.listHamilton)
        for key in self._dictHamil:
            item = QtGui.QStandardItem(key)
            self._model.appendRow(item)
        self.listHamilton.setModel(self._model)
        self.listHamilton.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.listHamilton.clicked.connect(self.on_item_select1)

        #####RadioButtonsPES#####
        self.onRadio.setChecked(True)
        self.onRadio.toggled.connect(self.setPES)
        self.offRadio.toggled.connect(self.unsetPES)

        #####ListView of PES is built###
        self.setPES()

        ###RadioButtonsJob####
        self.RealRadio.toggled.connect(self.setJob1)
        self.RealRadio.setChecked(False)
        self.ImaginaryRadio.toggled.connect(self.setJob2)
        self.EigenstateRadio.toggled.connect(self.setJob3)
        self.fluxEigenstateRadio.toggled.connect(self.setJob4)

        self._job = None
        self._dictJob = {'real-time Propagation': self.RealRadio,
        'imaginary-time Propagation': self.ImaginaryRadio,
        'eigenstates': self.EigenstateRadio,
        'flux eigenstates': self.fluxEigenstateRadio}

        ####QGraphicsView###
#        pixmap = QtGui.QPixmap('nx_test.png')
#        self.scene = QtGui.QGraphicsScene(self)
#        self.scene.addPixmap(pixmap)
#        self.uiDisplayTree.setScene(self.scene)

        ####PushBottoms#####
        self.uiCancel.clicked.connect(self.cancelFunc)
        self.uiSaveJob.clicked.connect(self.saveProject)
        self.uiStartCal.clicked.connect(self.esc)

        ####Line Edits#####
        self.uiStartTime.textChanged.connect(self.change1)
        self.uiEndTime.textChanged.connect(self.change2)
        self.uiInit.textChanged.connect(self.change3)
        self.uiIter.textChanged.connect(self.change4)

        ####Networkx and MCTDH####
        self.setConfig = None
        self.setSystem = None

        self.modelTree = None
        self.scene = None

    def genereInput(self, inputFile):
        ####Get all Parameters from example.in#####
        inobj = InPut(inputFile) 
        paradict = inobj._paradict

        self._integrator = []
        self._eps = []

        self._eps.append(paradict['eps_general'])
        self._eps.append(paradict['eps_1'])
        self._eps.append(paradict['eps_2'])
        self._integrator.append(paradict['start'])
        self._integrator.append(paradict['end'])
        self._integrator.append(paradict['dt'])
        self._integrator.append(paradict['iteration'])
        self._hamiltonian = paradict['Hamiltonian']
        self._potential = paradict['Potential']
        self._job = paradict['job']
        self._parameters = paradict['para']

        ###LineEdit####
        self.uiStartTime.setText(self._integrator[0])
        self.uiEndTime.setText(self._integrator[1])
        self.uiInit.setText(self._integrator[2])
        self.uiIter.setText(self._integrator[3])

        self._dictJob[self._job].setChecked(True)


    def getInput(self, key):
        ###get Attributes#######
        print self._HamiltonianDir
        inputFile = self._HamiltonianDir + '/' + key + '/' + 'example.in' 
        self._inputFile = inputFile
        
        filenames = os.walk(self._HamiltonianDir+'/'+str(key)).next()[2]
        for val in filenames:
            if 'txt' in val:
                sysTreeFile = val
    
        self._mctdhConfig = self._HamiltonianDir + '/' + key + '/' + 'mctdh.config'
        self._sysTreeFile  = self._HamiltonianDir + '/' + key + '/' + sysTreeFile

        if self._ProjectName != None:
            if self._SessionName != None:
                self._SESmctdhConfig = self._startingPath + '/' + self._ProjectName +'/' + self._SessionName + '/' + 'mctdh.config'
                self._SESsysTreeFile  = self._startingPath + '/' + self._ProjectName + '/' + self._SessionName + '/' + sysTreeFile
                self._SESinputFile = self._startingPath + '/' + self._ProjectName + '/' + self._SessionName + '/' + 'example.in'

        print self._SessionName, 'from getInput, outside if clause'

        self.genereInput(inputFile)
        

    def editSession(self, name):
        self.uiProjectName.blockSignals(True)
        self.uiProjectName.setText(str(name))
        self.uiProjectName.blockSignals(False)

    def clearSession(self):
        self.uiProjectName.clear()

    def makeParaDict(self):
        self._paradict['eps_general'] = self._eps[0]
        self._paradict['eps_1']       = self._eps[1]
        self._paradict['eps_2']       = self._eps[2]
        self._paradict['start']       = self._integrator[0]
        self._paradict['end']         = self._integrator[1]
        self._paradict['dt']          = self._integrator[2]
        self._paradict['iteration']   = self._integrator[3]
        self._paradict['Hamiltonian'] = self._hamiltonian
        self._paradict['Potential']   = self._potential
        self._paradict['job']         = self._job
        self._paradict['para']        = self._parameters

    def closeEvent(self, event):  #Overriding inherited memberfunction
        os.chdir("../") #if dialog is closed, leave folder
        event.accept()

    def showdialog2(self, Stringmes):
        msg = QtGui.QMessageBox()
        msg.setIcon(QtGui.QMessageBox.Warning)

        msg.setText(Stringmes)
        msg.setStandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)

        msg.buttonClicked.connect(self.msgbtn)
        msg.exec_()

    def msgbtn(self, i):
        self._messagebut = str(i.text())

    def showdialog(self, stringMes):
        msg = QtGui.QMessageBox()
        msg.setIcon(QtGui.QMessageBox.Information)

        msg.setText(stringMes)
#        msg.setInformativeText("This is additional information")
#        msg.setWindowTitle("MessageBox")
#        msg.setDetailedText("The details are as follows:")
#        msg.setStandardButtons(QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)

#        msg.buttonClicked.connect(self.msgbtn)
        msg.exec_()        #!!!!!!!!!!! short way to execute Qobject
#        print "value of pressed message box button:", retval

#    def msgbtn(self, i):
#        print "Button pressed is:",i.text()

    def managefolder(self):
        # os.chdir(self._startingPath+"/"+self._ProjectName) 
#        print os.getcwd()   
        # try:
        #     shutil.rmtree("tmp") #removes folder
        # except Exception:
        #     pass
        # os.makedirs("tmp")
        # os.chdir("./tmp")

        # sessionContent = os.walk(self._startingPath+"/"+self._ProjectName+'/'+str(self._SessionName)).next()[2]
        
        # if sessionContent:
            # print sessionContent, 'yes: from session'
            # shutil.copy2(str(self._SESmctdhConfig), str(os.getcwd()))
            # shutil.copy2(str(self._SESsysTreeFile), str(os.getcwd()))
            # shutil.copy2(str(self._SESinputFile), str(os.getcwd())) #!!!!!!!!!
        # else:
            # print sessionContent, 'no: from Hamilton'
        print self._inputFile    
        print self._SESinputFile    
        print self._sysTreeFile
        print self._SESsysTreeFile
        print self._mctdhConfig        
        print self._SESmctdhConfig

        if self._inputFile != None or self._sysTreeFile != None or self._mctdhConfig != None:

            shutil.copy2(self._mctdhConfig, self._SESmctdhConfig)
            shutil.copy2(self._sysTreeFile, self._SESsysTreeFile)
            shutil.copy2(self._inputFile, self._SESinputFile)
        else:
            pass
            #shutil.copy2(self._inputFile, self._SESinputFile)
                        

        #shutil.copy2(scr_mctdhConfig, str(os.getcwd()))
        #shutil.copy2(scr_sysTree, str(os.getcwd()))
        #shutil.copy2(scr_example, str(os.getcwd()))

    def TreeText(self):
        with open(self._SESsysTreeFile, "rb") as text:
            dataAll = text.readlines()
            lineNum = max([i for i, l_ in enumerate(dataAll) if l_ == '\n'])
            data = dataAll[:lineNum]
            data = ''.join(data)
            # QtGui.QTextEdit().setText
        self.uiTreeText.setText(data)
        
        

    def changeNode(self, my_index):
        if self._SessionName == None:
                self.showdialog('Please give Session name!')
        else:
            self.managefolder()

            # self.ModelTree = ModelTree(self._SESmctdhConfig, self._SESsysTreeFile)
                
            topNode = self.modelTree.getNode2(my_index).child(0) #modelTree from SceneGraphModel
            self._tree.setRootNode(topNode)
            
            self.PicGenerate()
            self.TreeText()

    def PicGenerate(self):
        ####Generate Outputfiles for new Pic###
        self.output()

        ####Pic with MCTDH Code and Networkx####
        print self._SESmctdhConfig, 'from change Node'
        print self._SESsysTreeFile, 'from change Node'

        self.ModelTree = ModelTree(self._SESmctdhConfig, self._SESsysTreeFile)
        self.LogicalNodes = LogicalNodes(self.ModelTree.lay_matr_mode, self._SESmctdhConfig, self._SESsysTreeFile) #object
        self.View = View(self.ModelTree.label_mode, self.ModelTree.nodes_spf) #object
        self.View.Display(self.LogicalNodes.G) #View method Display() generated .png file

        ####QGraphicsView###
        pixmap = QtGui.QPixmap('nx_test.png')
        self.scene = QtGui.QGraphicsScene(self)
        self.scene.addPixmap(pixmap)
        self.uiDisplayTree.setScene(self.scene)

        #####Leave tmp folder#####
        # os.chdir("../")

    def backUp(self):
        print self._startingPath
        print self._ProjectName
        if self._SessionName != None:
            scr = self._startingPath+ "/" + self._ProjectName + "/" + str(self._SessionName)
            self._dest = scr + '/tmp'
            try:
                shutil.rmtree(self._dest) #removes folder
            except Exception as e:
                print e.message, 'No tmp: copytmp; widgetA.py'

            shutil.copytree(scr, self._dest)


    def saveProject(self):
        if self._SessionName == None:
                self.showdialog('Please give Session name')
        else:
            files = os.walk(self._startingPath+'/'+self._ProjectName+'/'+str(self._SessionName)).next()[2]
            if files:
                #print "overwrite stuff?"
                self.showdialog2('Overwriting?')
                if 'Yes' in self._messagebut:
                    self.output()
                    os.chdir("../")
                    self.esc()
                else:
                    print 'out savePro'
                    
#            else:                         #Session Folder doesn't exists!
#                self.managefolder()
#                self.output()
#                os.chdir("../")

            # self.copytmp()

    def cancelFunc(self):    
        try:
            files = os.walk(self._startingPath+'/'+self._ProjectName+'/'+self._SessionName).next()[2]
            print files
        except Exception:
            raise
        if files:
            print files
            self.showdialog2("Warning if you proceed, your changes will irreversible lost? Do you want to proceed?")
            if 'Yes' in self._messagebut:
                print 'Yes'
                for file_ in files:
                    if 'txt' in file_:
                        sysFile = file_

                self._TMPmctdhConfig = self._startingPath + '/' \
                + self._ProjectName + '/' + self._SessionName + \
                '/tmp/mctdh.config'

                self._TMPsysTreeFile = self._startingPath + '/' \
                + self._ProjectName + '/' + self._SessionName + \
                '/tmp/' + sysFile

                self._TMPinputFile =  self._startingPath  + '/' \
                + self._ProjectName  + '/' + self._SessionName +\
                '/tmp/example.in'

                try:
                    shutil.copy2(self._TMPmctdhConfig, self._SESmctdhConfig)
                    shutil.copy2(self._TMPsysTreeFile, self._SESsysTreeFile)
                    shutil.copy2(self._TMPinputFile, self._SESinputFile)
                except Exception:
                    print' Hello Error'
                    raise
                try:
                    self.start()
                except Exception:
                    raise
            else:
                pass
        else:
            pass

    def esc(self):
        os.chdir("../")
        self.close()

    def setSessionName(self, name):
        self._SessionName = name

    def change0(self):
        self._SessionName = str(self.uiProjectName.text())
        folders = os.walk(self._startingPath+'/'+self._ProjectName).next()[1]
        if self._SessionName in folders:
            self.showdialog('Folder already exists!')
        # self.start()
        # self.backUp()

    def change1(self):
        self._integrator[0] = str(self.uiStartTime.text())
    def change2(self):
        self._integrator[1] = str(self.uiEndTime.text())
    def change3(self):
        self._integrator[2] = str(self.uiInit.text())
    def change4(self):
        self._integrator[3] = str(self.uiIter.text())


    def setJob1(self):
        self._job = "real-time Propagation"
    def setJob2(self):
        self._job = "imaginary-time Propagation"
    def setJob3(self):
        self._job = "eigenstates"
    def setJob4(self):
        self._job = "flux eigenstates"
    #    print job

    def unsetPES(self):
    #    print dir(self.model)
    #    print self.model.rowCount()
        self.modelPES.removeRows(0, 2, QtCore.QModelIndex())
        self._potential = "None"

    def setPES(self):
        #####ListModelPES#######
        self.modelPES = QtGui.QStandardItemModel(self.listPES)
        for key in self._dictPES:
            item = QtGui.QStandardItem(key)
            self.modelPES.appendRow(item)
        self.listPES.setModel(self.modelPES)
        self.listPES.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
    #    self.on_item_select_pes = partial(self.on_item_select, self._potential,
    #                                self._dictPES)
        self.listPES.clicked.connect(self.on_item_select2)



#    def on_item_select(self, operator, dictOp, item):
#        key = item.data().toString()
#        operator = dictOp[str(key)]
#        print operator


    def start(self):
        self.clearTree()
        if self._SessionName != None or self._SessionName == '':
            try:
                filenames = os.walk(self._startingPath+'/'+self._ProjectName+'/'+self._SessionName).next()[2]
                print filenames       
                for val in filenames:
                    if 'txt' in val:
                        sysTreeFile = val

                self._SESmctdhConfig = self._startingPath + '/' + self._ProjectName +'/' + self._SessionName + '/' + 'mctdh.config'
                self._SESsysTreeFile  = self._startingPath + '/' + self._ProjectName + '/' + self._SessionName + '/' + sysTreeFile
                self._SESinputFile = self._startingPath + '/' + self._ProjectName + '/' + self._SessionName + '/' + 'example.in'
                

                self.genereInput(self._SESinputFile)
                self.TreeText()
                self.TreeOnly()

            except (StopIteration, UnboundLocalError):
                self.clearTree()
        else:
            print 'Error in start'
            sys.exit()
    
    def clearTree(self):
                try:
                    self.uiTreeText.clear()
                    self.scene.clear()
                    self.uiDisplayTree.setScene(self.scene)
                    self.modelTree.removeRow(0)
                    print self.modelTree._rootNode._children
                except (IndexError, AttributeError) as e:
                    print e.message, 'start'
            
    def TreeOnly(self):
        ####TreeView########
        self._tree = Tree(self._SESmctdhConfig, self._SESsysTreeFile)
        self.modelTree = SceneGraphModel(self._tree._rootNode0)
        self.uiTree.setModel(self.modelTree)
        self.uiTree.expandAll()
        self.uiTree.resizeColumnToContents(0)
        self.uiTree.resizeColumnToContents(1)
        # self.uiTree.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
#        my_index = self.modelTree.index(0, 0, QtCore.QModelIndex())
        self.uiTree.clicked.connect(self.changeNode)

        #####make Pic from tmp###
        self.PicGenerate()

    def generateTree(self, item):
        key = str(item.data().toString())
        self.getInput(key)
        self._hamiltonian = self._dictHamil[str(key)]

        #####make tmp######
        self.managefolder()

        #####generates Tree###
        self.TreeOnly()        

    def on_item_select1(self, item):
        if self._SessionName != None:
            sessionpath = self._startingPath+'/'+self._ProjectName+'/'+self._SessionName
            try:
                SESfiles = os.walk(sessionpath).next()[2]
            except StopIteration:
                os.chdir(self._startingPath+'/'+self._ProjectName)
                os.makedirs(self._SessionName)
                self._temporarySES = self._SessionName
                os.chdir(self._startingPath)
                SESfiles = []
                self.on_item_select1(item)
            print SESfiles
            if SESfiles:
                self.showdialog2("Overwriting session's basis?")
                if 'Yes' in self._messagebut:
                    print 'Yes'
                    self.generateTree(item)
                else:
                    print self._messagebut
            else:
                self.generateTree(item)
        else:
            self.showdialog('Please give Session name!')

    def on_item_select2(self, item):
        key = item.data().toString()
        self._potential = self._dictPES[str(key)]
        #print self._potential

    def output(self):
        """Class OutPut takes all parameters and saves them in File by creating
     the object of this class"""
        # print os.getcwd()
        self.makeParaDict()
        print self._SESinputFile
        print self._SESsysTreeFile
        outobj = OutPut(self._tree, self._paradict, self._SESsysTreeFile, self._SESinputFile)
        outobj.savefile()
        outobj.savefile2()

if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    app.setStyle("cleanlooks")
    wnd =WidgetA(None)
    wnd.show()


    sys.exit(app.exec_())
