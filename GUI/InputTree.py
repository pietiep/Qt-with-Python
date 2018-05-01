from PyQt4 import QtCore, QtGui, uic
import sys
from Node import Node, Tree

class SceneGraphModel(QtCore.QAbstractItemModel):
    def __init__(self, root, parent=None):
        super(SceneGraphModel, self).__init__(parent)
        self._rootNode = root
        self._childIndex = QtCore.QModelIndex()

    def parent(self, index):
        node = index.internalPointer()
        parentNode = node.parent()

        if parentNode == self._rootNode:
            return QtCore.QModelIndex()
        return self.createIndex(parentNode.row(), 0, parentNode)

    def index(self, row, column, parent):

#        if not parent.isValid():
#            parentNode = self._rootNode
#        else:
#            parentNode = parent.internalPointer()

        parentNode = self.getNode(parent)

        childItem = parentNode.child(row)

        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex()

    def rowCount(self, parent):
        if not parent.isValid():
            parentNode = self._rootNode
        else:
            parentNode = parent.internalPointer()

        return parentNode.childcount()

    def columnCount(self, parent):
    #    return 1
        return 2

    
    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | \
            QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsDragEnabled | \
            QtCore.Qt.ItemIsDropEnabled

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if section == 0:
                return "Scenegraph"
            else:
                return "Mode"

    def data(self, index, role):

        if not index.isValid():
            return None

        node = index.internalPointer()

        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole: #Name is always displayed
            if index.column() == 0:
                return node.name()
            else:
                if node.typeInfo() == "Bottom":
                    return node._physcoor
        #        return node.typeInfo()

        if role == QtCore.Qt.DecorationRole:
            if index.column() == 0:

                typeInfo = node.typeInfo()

                if typeInfo == "LIGHT":
                    return QtGui.QIcon(QtGui.QPixmap(":/Bioshock.png")) #geht in die binary

    def setData(self, index, value, role = QtCore.Qt.EditRole):
        if index.isValid():
            if role == QtCore.Qt.EditRole:
                node = index.internalPointer()
                # print str(value.toString())
                # print index.column()
                if index.column() == 0:
                    node.setName(str(value.toString()))
                    return True
                elif index.column() == 1:
                    node.setPhyscoor(str(value.toString()))
                    return True
        return False

    def getNode(self, index):
        if index.isValid():
            node = index.internalPointer()
            if node:
                return node
        return self._rootNode

    def getNode2(self, index):
        return self._rootNode

    def insertRows(self, position, rows, parent=QtCore.QModelIndex()):
        parentNode = self.getNode(parent)
        child = self.getNode(self._childIndex)

        self.beginInsertRows(parent, position, position+rows-1)

        for row in range(rows):
            # childcount = parentNode.childcount()
            childNode = Node(child.name())
            success = parentNode.insertChild(position, childNode) # child inserted, _children grows, childcount counts one more

        self.endInsertRows()

        return success

    def removeRows(self, position, rows, parent=QtCore.QModelIndex()):
        parentNode = self.getNode(parent)

        self.beginRemoveRows(parent, position, position+rows-1)

        for row in range(rows):
            success = parentNode.removeChild(position)

        self.endRemoveRows()

        return success

#####Drag and Drop######

    def supportedDropActions(self):
        return QtCore.Qt.CopyAction | QtCore.Qt.MoveAction

    def mimeTypes(self):
        types = QtCore.QStringList()
        types.append('text/plain')
        return types

    def mimeData(self, index):   #index is list with len=2; SPFs and (for bottom) mode
        rc = ''
        self._childIndex = index[0]
        mimeData = QtCore.QMimeData()
        mimeData.setText(rc)
        return mimeData

    def dropMimeData(self, data, action, row, column, parentIndex):
        if action == QtCore.Qt.IgnoreAction:
            return True
        self.insertRows(0, 1, parentIndex)
        dummy = self._childIndex
        print dummy.internalPointer().name
        self._childIndex = dummy.child(1,0)
        print self._childIndex.internalPointer().name #here is the bug!!!!!!
        self.insertRows(0, 1, dummy)

        # self.InsertViaDrop(self._childIndex, parentIndex)
        return True
    
    def InsertViaDrop(self, childIndex, parentIndex):
        print parentIndex.internalPointer().name()
        self.insertRows(0, 1, parentIndex)
        dummyChild = childIndex

        childcount = dummyChild.internalPointer().childcount()

        if dummyChild.internalPointer().childAll():                #if has got children
            for i in range(childcount):
                self._childIndex = dummyChild.child(i,0)
                self.InsertViaDrop(self._childIndex, parentIndex)

    def getIndex(self, parentIndex):
        childcount = parentIndex.internalPointer().childcount()
        print parentIndex.internalPointer().name()

        if parentIndex.internalPointer().childAll():
            for i in range(childcount):
                childIndex = parentIndex.child(i,0)
                self.getIndex(childIndex)

    
base, form = uic.loadUiType("mctdhTree.ui")

#class GenerateFile(base, form):
#    def __init__(self, parent=None):
#        super(base, self).__init__(parent)
#        self.setupUi(self)
#        eps = ["1E-5", "1E-6", "1E-5"]
#        integrator = ["0", "1000", "0.1", "100"]
#        hamiltonian = "194"
#        potential = "101"
#        job = "eigenstates"
#        parameters = [[1, 2, 3, 4],
#                    [5, 6, 7, 8],
#                    [9, 10, 11, 12],
#                    [13, 14, 15, 16],
#                    [17, 18, 19, 20],
#                    [21, 22, 23, 24]]
#
#        self._eps = eps
#        self._integrator = integrator
#        self._hamiltonian = hamiltonian
#        self._potential = potential
#        self._job = job
#        self._parameters = parameters
#
#        self._tree = Tree("36")  #Delegation instead of inheritance of Tree
#        self._treeData = self._tree._treeData  #Top parent node object storing
#        #all child node which also contain child node objects
#
#        model = SceneGraphModel(self._tree._rootNode0)
#
#        self.uiTree.setModel(model)
#
#    #    self.connect(self.uiGenerateFile, SIGNAL("activated()"), self.BrowserCon)
#        self.uiGenerateFile.clicked.connect(self.output)
#

if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    app.setStyle("cleanlooks")
    tree = Tree('mctdh.config', 'CH3g1.txt')
    model = SceneGraphModel(tree._rootNode0)
    # RightLeg = model.index(0, 3, QtCore.QModelIndex())

    treeView = QtGui.QTreeView()
    treeView.show()
    treeView.setModel(model)
    treeView.expandAll()
    treeView.resizeColumnToContents(0)
    treeView.resizeColumnToContents(1)
    treeView.setDragDropMode(QtGui.QAbstractItemView.InternalMove)


#    wnd =GenerateFile()
#    wnd.show()


    sys.exit(app.exec_())
