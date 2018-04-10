from PyQt4 import QtCore, QtGui, uic
from PyQt4 import *
import sys
from Node import OutPut, Tree, Node, TransformNode, CameraNode, LightNode
from InputTree import SceneGraphModel
from functools import partial
from ModelTree import ModelTree
from LogicalNodes import LogicalNodes
from View import View
import os, shutil

base, form = uic.loadUiType("dialogA.ui")

class WidgetA(base, form):
    def __init__(self, parent=None):
        super(WidgetA, self).__init__(parent)
        self.setupUi(self)

        ####Data#####
        eps = ["1E-5", "1E-6", "1E-5"]
        integrator = ["0", "1000", "0.1", "100"]
        hamiltonian = "194"
        potential = "101"
        job = "real-time Propagation"
        parameters = [[1, 2, 3, 4],
                [5, 6, 7, 8],
                [9, 10, 11, 12],
                [13, 14, 15, 16],
                [17, 18, 19, 20],
                [21, 22, 23, 24]]

        ####Attributes#####
        self._eps = eps
        self._integrator = integrator
        self._operator = None
        self._hamiltonian = hamiltonian
        self._potential = potential
        self._job = job
        self._parameters = parameters

        self._tree = Tree("36")  #Delegation instead of inheritance of Tree
        self._treeData = self._tree._treeData

        self._dictHamil = {'CH3': '194', 'NO3': '195'}
        self._dictPES = {'CH3': '100', 'NO3': '101'}

        self._SessionName = None

        #####LineEdit:Projectname#######
#        self.uiProjectName.setText("Session1")
        self.uiProjectName.textChanged.connect(self.change0)

        #####ListModelHamilton#######
        self._model = QtGui.QStandardItemModel(self.listHamilton)
        for key in self._dictHamil:
            item = QtGui.QStandardItem(key)
            self._model.appendRow(item)
        self.listHamilton.setModel(self._model)
        self.listHamilton.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
    #    self.on_item_select_ha = partial(self.on_item_select, self._hamiltonian,
    #                                self._dictHamil)
        self.listHamilton.clicked.connect(self.on_item_select1)

        #####RadioButtonsPES#####
        self.onRadio.setChecked(True)
        self.onRadio.toggled.connect(self.setPES)
        self.offRadio.toggled.connect(self.unsetPES)

        #####ListView of PES is built###
        self.setPES()

        ###RadioButtonsJob####
        self.RealRadio.setChecked(True)
        #func1 = lambda job="real-time Propagation": self.setJob(job)
        self.RealRadio.toggled.connect(self.setJob1)
        #self.func2 = lambda job="imaginary-time Propagation": self.setJob(job)
        self.ImaginaryRadio.toggled.connect(self.setJob2)
        #func3 = lambda job="imaginary-time Propagation": self.setJob(job)
        self.EigenstateRadio.toggled.connect(self.setJob3)
        #func4 = lambda job="imaginary-time Propagation": self.setJob(job)
        self.fluxEigenstateRadio.toggled.connect(self.setJob4)

        ###LineEdit####
        self.uiStartTime.setText(self._integrator[0])
        self.uiStartTime.textChanged.connect(self.change1)
        self.uiEndTime.setText(self._integrator[1])
        self.uiEndTime.textChanged.connect(self.change2)
        self.uiInit.setText(self._integrator[2])
        self.uiInit.textChanged.connect(self.change3)
        self.uiIter.setText(self._integrator[3])
        self.uiIter.textChanged.connect(self.change4)

        ####TreeView########
        self.modelTree = SceneGraphModel(self._tree._rootNode0)
        self.uiTree.setModel(self.modelTree)
        self.uiTree.expandAll()
        self.uiTree.resizeColumnToContents(0)
        self.uiTree.resizeColumnToContents(1)
        my_index = self.modelTree.index(0, 0, QtCore.QModelIndex())
        self.uiTree.clicked.connect(self.changeNode)


        ####QGraphicsView###
        pixmap = QtGui.QPixmap('nx_test.png')
        self.scene = QtGui.QGraphicsScene(self)
        self.scene.addPixmap(pixmap)
        self.uiDisplayTree.setScene(self.scene)

        ####PushBottoms#####
        self.uiCancel.clicked.connect(self.esc)
        self.uiSaveJob.clicked.connect(self.saveProject)
        self.uiStartCal.clicked.connect(self.esc)

        ####Networkx and MCTDH####

        self.setConfig = None
        self.setSystem = None

        self.ModelTree = None


    def closeEvent(self, event):  #Overriding inherited memberfunction
        os.chdir("../") #if dialog is closed, leave folder
        event.accept()

    def showdialog(self):
        msg = QtGui.QMessageBox()
        msg.setIcon(QtGui.QMessageBox.Information)

        msg.setText("Please give a name for the current Session")
#        msg.setInformativeText("This is additional information")
        msg.setWindowTitle("MessageBox")
        msg.setDetailedText("The details are as follows:")
        msg.setStandardButtons(QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)

#        msg.buttonClicked.connect(self.msgbtn)
        retval = msg.exec_()        #!!!!!!!!!!! short way to execute Qobject
#        print "value of pressed message box button:", retval

#    def msgbtn(self, i):
#        print "Button pressed is:",i.text()

    def managefolder(self):
        import os, shutil
        try:
            shutil.rmtree("tmp") #removes folder
        except Exception:
            pass
        os.makedirs("tmp")
        os.chdir("./tmp")
        shutil.copy2("""/home/piet/Schreibtisch/masterarbeit/Qt-with-Python/GUI/mctdh.config"""
                    , str(os.getcwd()))
        shutil.copy2("""/home/piet/Schreibtisch/masterarbeit/Qt-with-Python/GUI/CH3g1.txt"""
                    , str(os.getcwd()))

    def changeNode(self, my_index):
        if self._SessionName == None:
                self.showdialog()
        else:
            self.managefolder()

            self.ModelTree = ModelTree()
            topNode = self.modelTree.getNode2(my_index).child(0)
            self._tree.setRootNode(topNode)

            ####Generate Outputfiles for new Pic###
            self.output()

            ####Pic with MCTDH Code and Networkx####
            self.ModelTree = ModelTree()
            self.LogicalNodes = LogicalNodes(self.ModelTree.lay_matr_mode) #object
            self.View = View(self.ModelTree.label_mode, self.ModelTree.nodes_spf) #object
            self.View.Display(self.LogicalNodes.G) #View method Display() generated .png file


            ####QGraphicsView###
            pixmap = QtGui.QPixmap('nx_test.png')
            self.scene = QtGui.QGraphicsScene(self)
            self.scene.addPixmap(pixmap)
            self.uiDisplayTree.setScene(self.scene)

            #####Leave tmp folder#####
            os.chdir("../")

    def copytmp(self):
        scr = str(os.getcwd()) + "/tmp"
        dest = str(os.getcwd()) + "/" + str(self._SessionName)
        print scr, dest
        try:
            shutil.rmtree(dest) #removes folder
        except Exception:
            pass
        shutil.copytree(scr, dest)


    def saveProject(self):
        if self._SessionName == None:
                self.showdialog()
        else:
            root, directories, filenames = os.walk(".").next()
            if "tmp" in directories:
                pass
            else:
                print "hello"
                print "hello"
                print "hello"
                print "hello"
                print "hello"
                print "hello"
                self.managefolder()
                self.output()
                os.chdir("../")

            self.copytmp()

    def esc(self):
        os.chdir("../")
        self.close()

    def change0(self):
        import os
        self._SessionName = self.uiProjectName.text()
#        os.chdir("./" + self._SessionName)  # Change dir

    def change1(self):
        self._integrator[0] = self.uiStartTime.text()
    def change2(self):
        self._integrator[1] = self.uiEndTime.text()
    def change3(self):
        self._integrator[2] = self.uiInit.text()
    def change4(self):
        self._integrator[3] = self.uiIter.text()


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


    def on_item_select1(self, item):
        key = item.data().toString()
        self._hamiltonian = self._dictHamil[str(key)]
        print self._hamiltonian

    def on_item_select2(self, item):
        key = item.data().toString()
        self._potential = self._dictPES[str(key)]
        print self._potential

    def output(self):
        """Class OutPut takes all parameters and saves them in File by creating
     the object of this class"""
        outobj = OutPut(self._eps, self._integrator, self._hamiltonian, \
                        self._potential, self._job, self._parameters, \
                        self._tree)

if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    app.setStyle("cleanlooks")
    wnd =WidgetA(None)
    wnd.show()


    sys.exit(app.exec_())
