from PyQt4 import QtCore, QtGui, uic
import sys
from Node import OutPut, Tree
from Node import InPut
from InputTree import SceneGraphModel
from ModelTree import ModelTree
from LogicalNodes import LogicalNodes
from View import View
import os, shutil
from compiler.consts import CO_FUTURE_PRINT_FUNCTION

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
        self._tree = None

        self._dictHamil = {'CH3': '194', 'NO3': '195'}
        self._dictPES = {'CH3': '100', 'NO3': '101'}
        self._mctdhConfig = None 
        self._sysTreeFile = None
        self._inputFile = None
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
        #self.uiProjectName.textChanged.connect(self.change0)


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

        ####PushBottoms#####
        self.uiCancel.clicked.connect(self.cancel)
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

        print self._TMPinputFile
        

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

    def showdialog3(self, Stringmes):
        msg = QtGui.QMessageBox()
        msg.setIcon(QtGui.QMessageBox.Information)

        msg.setText(Stringmes)
        msg.setStandardButtons(QtGui.QMessageBox.Save | QtGui.QMessageBox.Cancel)

        msg.buttonClicked.connect(self.msgbtn)
        msg.exec_()

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
        # print self._inputFile    
        # print self._SESinputFile    
        # print self._sysTreeFile
        # print self._SESsysTreeFile
        # print self._mctdhConfig        
        # print self._SESmctdhConfig

        if self._inputFile != None or self._sysTreeFile != None or self._mctdhConfig != None:

            shutil.copy2(self._mctdhConfig, self._TMPmctdhConfig)
            shutil.copy2(self._sysTreeFile, self._TMPsysTreeFile)
            shutil.copy2(self._inputFile, self._TMPinputFile)
        else:
            pass

    def changeNode(self, my_index):
        if self._SessionName == None:
                self.showdialog('Please give Session name!')
        else:
            self.managefolder()

            # self.ModelTree = ModelTree(self._SESmctdhConfig, self._SESsysTreeFile)
                
            topNode = self.modelTree.getNode2(my_index).child(0) #modelTree from SceneGraphModel
            self._tree.setRootNode(topNode)
            
            self.PicGenerate()

    def PicGenerate(self):
        ####Generate Outputfiles for new Pic###
        self.output()

        ####Pic with MCTDH Code and Networkx####
        print self._SESmctdhConfig, 'from change Node'
        print self._SESsysTreeFile, 'from change Node'

        self.ModelTree = ModelTree(self._TMPmctdhConfig, self._TMPsysTreeFile)
        self.LogicalNodes = LogicalNodes(self.ModelTree.lay_matr_mode, self._TMPmctdhConfig, self._TMPsysTreeFile) #object
        self.View = View(self.ModelTree.label_mode, self.ModelTree.nodes_spf) #object
        self.View.Display(self.LogicalNodes.G) #View method Display() generated .png file

        ####QGraphicsView###
        pixmap = QtGui.QPixmap('nx_test.png')
        self.scene = QtGui.QGraphicsScene(self)
        self.scene.addPixmap(pixmap)
        self.uiDisplayTree.setScene(self.scene)

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
            print scr
            print self._dest


    def saveProject(self):
        name = self.uiProjectName.text()
        self._SessionName = name
        SESfolders = os.walk(self._startingPath+'/'+self._ProjectName).next()[1]
        if name == '':
                self.showdialog('Please give Session name')
        elif name in SESfolders:
            self.showdialog2('Overwriting %s?' %name)
            if 'Yes' in self._messagebut:
                print 'yes'
                self.fromTMPToSES()
                self.output()  #saves all Parameter and Tree to *.in and tree only to *.txt 
            else:
                pass
        else:
            self.fromTMPToSES()
            self.output()  #saves all Parameter and Tree to *.in and tree only to *.txt 

    def cancel(self):
        self.removeContent()
        self.esc()

    def removeContent(self):
        sysPath = self._startingPath +'/'+ self._ProjectName
        os.chdir(sysPath)

        try:
            shutil.rmtree('tmp')
        except OSError:
            pass
            
        os.mkdir('tmp')
        os.chdir(self._startingPath)

    def checkTMP(self):
        sysPathTMP = self._startingPath +'/'+ self._ProjectName +'/tmp'
        files = os.walk(sysPathTMP).next()[2]
        print files
        if files:
            return True
        return False

    def fromHToTMP(self, item):
        if self.checkTMP():

            self.showdialog2('Overwriting temporary Settings?')
            if 'Yes' in self._messagebut:
                print 'Yes'
                self.fromHToTMPinner(item)
            else:
                pass
        else:
            self.fromHToTMPinner(item)

    def fromHToTMPinner(self, item):
        sysPath = self._HamiltonianDir+'/'+item
        files = os.walk(sysPath).next()[2]
        for file_ in files:
            if 'txt' in file_:
                sysFile = file_    

        self._mctdhConfig = sysPath+'/'+'mctdh.config'
        self._sysTreeFile = sysPath+'/'+sysFile
        self._inputFile   = sysPath+'/'+'example.in'

        self._TMPmctdhConfig = self._startingPath + '/' \
        + self._ProjectName + '/' + \
        '/tmp/mctdh.config'

        self._TMPsysTreeFile = self._startingPath + '/' \
        + self._ProjectName + '/' + \
        '/tmp/' + sysFile

        self._TMPinputFile =  self._startingPath  + '/' \
        + self._ProjectName  + '/' \
        '/tmp/example.in'

        try:
            shutil.copy2(self._mctdhConfig, self._TMPmctdhConfig) 
            shutil.copy2(self._sysTreeFile, self._TMPsysTreeFile)
            shutil.copy2(self._inputFile, self._TMPinputFile)
        except Exception:
            print' Hello Error'
            raise

    def fromSESToTMP(self):    
        try:
            files = os.walk(self._startingPath+'/'+self._ProjectName+'/'+self._SessionName).next()[2]
        except Exception:
            raise
        if files:
            print files
            for file_ in files:
                if 'txt' in file_:
                    sysFile = file_

            self._TMPmctdhConfig = self._startingPath + '/' \
            + self._ProjectName + \
            '/tmp/mctdh.config'

            self._TMPsysTreeFile = self._startingPath + '/' \
            + self._ProjectName + \
            '/tmp/' + sysFile

            self._TMPinputFile =  self._startingPath  + '/' \
            + self._ProjectName  +\
            '/tmp/example.in'

            try:
                shutil.copy2(self._TMPmctdhConfig, self._SESmctdhConfig) 
                shutil.copy2(self._TMPsysTreeFile, self._SESSESsysTreeFile)
                shutil.copy2(self._TMPinputFile, self._SESinputFile)
            except Exception:
                print' Hello Error'
                raise

    def fromTMPToSES(self):    
        files = os.walk(self._startingPath + '/' \
        + self._ProjectName + '/' + \
        '/tmp').next()[2]

        for file_ in files:
            if 'txt' in file_:
                sysFile = file_  #Error prone!!! if you have multiple txt Files

        self._TMPmctdhConfig = self._startingPath + '/' \
        + self._ProjectName + \
        '/tmp/mctdh.config'

        self._TMPsysTreeFile = self._startingPath + '/' \
        + self._ProjectName + \
        '/tmp/' + sysFile

        self._TMPinputFile =  self._startingPath  + '/' \
        + self._ProjectName +\
        '/tmp/example.in'

        print self._TMPinputFile
        try:
            shutil.copy2(self._TMPmctdhConfig, self._SESmctdhConfig) 
            shutil.copy2(self._TMPsysTreeFile, self._SESsysTreeFile)
            shutil.copy2(self._TMPinputFile,   self._SESinputFile)
        except Exception:
            print' Hello Error'

    def esc(self):
        self.close()

    def setSessionName(self, name):
        self._SessionName = name

    def folderExist(self):
        folders = os.walk(self._startingPath+'/'+self._ProjectName).next()[1]
        if self._SessionName in folders:
            self.showdialog('Folder already exists!')
            return False
        return True
        
    def change0(self):
        self._SessionName = str(self.uiProjectName.text())

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

    def unsetPES(self):
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
        self.listPES.clicked.connect(self.on_item_select2)

    def start(self):
        self.clearTree()
        name = str(self.uiProjectName.text())
        self._SessionName = name
        #### if SES contains files, these files will be copied to TMP
        try:
            filenames = os.walk(self._startingPath+'/'+self._ProjectName+'/'+self._SessionName).next()[2]
            print filenames       
            for val in filenames:
                if 'txt' in val:
                    sysTreeFile = val

            self._SESmctdhConfig = self._startingPath + '/' + self._ProjectName +'/' + self._SessionName + '/' + 'mctdh.config'
            self._SESsysTreeFile  = self._startingPath + '/' + self._ProjectName + '/' + self._SessionName + '/' + sysTreeFile
            self._SESinputFile = self._startingPath + '/' + self._ProjectName + '/' + self._SessionName + '/' + 'example.in'

            ###copies files from SES to TMP
            self.fromSESToTMP()

            ###Parameters from example.in in TMP will be loaded####
            self.genereInput(self._TMPinputFile)

            ###Tree will be constructed from parameters###
            self.TreeOnly()

        except (StopIteration, UnboundLocalError):
            self.clearTree()
    
    def clearTree(self):
                try:
                    self.scene.clear()
                    self.uiDisplayTree.setScene(self.scene)
                    self.modelTree.removeRow(0)
                    # print self.modelTree._rootNode._children
                except (IndexError, AttributeError) as e:
                    print e.message, 'start'
            
    def TreeOnly(self):
        ####TreeView########
        self._tree = Tree(self._TMPmctdhConfig, self._TMPsysTreeFile)
        self.modelTree = SceneGraphModel(self._tree._rootNode0)
        self.uiTree.setModel(self.modelTree)
        self.uiTree.expandAll()
        self.uiTree.resizeColumnToContents(0)
        self.uiTree.resizeColumnToContents(1)
        # self.uiTree.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
        self.uiTree.clicked.connect(self.changeNode)

        #####make Pic from tmp###
        self.PicGenerate()

    def generateTree(self, item):
        key = item
        self.getInput(key)
        
        self._hamiltonian = self._dictHamil[str(key)]

        #####generates Tree###
        self.TreeOnly()


    def on_item_select1(self, item):

        key = str(item.data().toString())        

        ####Copy from default Hamilton to tmp
        self.fromHToTMP(key)
        self.generateTree(key)

    def on_item_select2(self, item):
        key = item.data().toString()
        self._potential = self._dictPES[str(key)]

    def output(self):
        """Class OutPut takes all parameters and saves them in File by creating
     the object of this class"""
        self.makeParaDict()
        outobj = OutPut(self._tree, self._paradict, self._TMPsysTreeFile, self._TMPinputFile)
        outobj.savefile()
        outobj.savefile2()

if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    app.setStyle("cleanlooks")
    wnd =WidgetA(None)
    wnd.show()


    sys.exit(app.exec_())
