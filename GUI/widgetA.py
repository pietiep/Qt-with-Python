from PyQt4 import QtCore, QtGui, uic
from PyQt4 import *
import sys
from Node import OutPut, Tree, Node, TransformNode, CameraNode, LightNode
from InputTree import GenerateFile
from functools import partial

base, form = uic.loadUiType("widgetA.ui")

class WidgetA(base, form):
    def __init__(self, parent=None):
        super(WidgetA, self).__init__(parent)
        self.setupUi(self)
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

        #####ListModelHam#######
        self.model = QtGui.QStandardItemModel(self.listHamilton)
        for key in self._dictHamil:
            item = QtGui.QStandardItem(key)
            self.model.appendRow(item)
        self.listHamilton.setModel(self.model)
        self.listHamilton.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
    #    self.on_item_select_ha = partial(self.on_item_select, self._hamiltonian,
    #                                self._dictHamil)
        self.listHamilton.clicked.connect(self.on_item_select1)

        #####RadioButtonsPES#####
        self.onRadio.setChecked(True)
        self.onRadio.toggled.connect(self.setPES)
        self.offRadio.toggled.connect(self.unsetPES)

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

        self.uiGenerateFile.clicked.connect(self.output)

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
        self.model.removeRows(0, 2, QtCore.QModelIndex())
        self._potential = "None"

    def setPES(self):
         #####ListModelPES#######
        self.modelPES = QtGui.QStandardItemModel(self.listPES)
        for key in self._dictPES:
            item = QtGui.QStandardItem(key)
            self.modelPES.appendRow(item)
        self.listPES.setModel(self.model)
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
        outobj = OutPut(self._eps, self._integrator, self._hamiltonian, \
                        self._potential, self._job, self._parameters, \
                        self._tree) #Class OutPut takes all parameters
        # and saves them in File by creating the object of this class

if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    app.setStyle("cleanlooks")
    wnd =WidgetA()
    wnd.show()


    sys.exit(app.exec_())