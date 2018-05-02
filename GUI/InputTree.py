from PyQt4 import QtCore, QtGui, uic
import sys
from Node import Node, BottomNode, Tree

class SceneGraphModel(QtCore.QAbstractItemModel):
    def __init__(self, root, parent=None):
        super(SceneGraphModel, self).__init__(parent)
        self._rootNode = root
        self._child = None
        self._childIndex = QtCore.QModelIndex()
        self._dictNodes = {}

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
        oldNode = self._child
        if oldNode.typeInfo() == 'NODE':
            self.addNode(oldNode.name(), oldNode.name(), None)    
        if oldNode.typeInfo() == 'Bottom':
            self.addBottomNode(oldNode.name(), oldNode.name(), None, oldNode.physcoor())
        self.copyNode(self._child)

        self.beginInsertRows(parent, position, position+rows-1)

        for row in range(rows):
            success = parentNode.insertChild(position, self._dictNodes[oldNode.name()]) # child inserted, _children grows, childcount counts one more

        self.endInsertRows()

        return success

    def removeRows(self, position, rows, parent=QtCore.QModelIndex()):
        parentNode = self.getNode(parent)
        grandfather = parentNode.parent()
        # fathers = grandfather.childAll()
        # pos = fathers.index(parentNode)
                
        self.beginRemoveRows(parent, position, position+rows-1)

        for row in range(rows):
            # success = grandfather.removeChild(0)
            print type(grandfather)
            
            success = grandfather.removeChild(position)

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
        self._child = index[0].internalPointer()
        self._childIndex = index[0]
        mimeData = QtCore.QMimeData()
        mimeData.setText(rc)
        return mimeData

    def dropMimeData(self, data, action, row, column, parentIndex):
        if action == QtCore.Qt.IgnoreAction:
            return True
        
        self.insertRows(0,1, parentIndex)
        index = self._childIndex
        self.removeRows(0,1, index)
        print self._rootNode.child(0)
        return True

    def copyNode(self, oldNode):
        children = oldNode.childAll()
        if children:
            for oldchild in children:
                if oldchild.typeInfo() == "NODE":
                    self.addNode(oldchild.name(), oldchild.name(), self._dictNodes[oldNode.name()])
                if oldchild.typeInfo() == "Bottom":
                    self.addBottomNode(oldchild.name(), oldchild.name(), self._dictNodes[oldNode.name()], oldchild.physcoor())
                self.copyNode(oldchild)
    
    def addNode(self, obj, SPF, parent):
        self._dictNodes[obj] = Node(SPF, parent)

    def addBottomNode(self, obj, SPF, parent, physcoor):
        self._dictNodes[obj] = BottomNode(SPF, parent, physcoor)
                
        


    
base, form = uic.loadUiType("mctdhTree.ui")


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


    sys.exit(app.exec_())
