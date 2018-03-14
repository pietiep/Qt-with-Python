from PyQt4 import QtCore, QtGui, uic
import sys
from Node import Tree, Node, TransformNode, CameraNode, LightNode
import icons_rc

class SceneGraphModel(QtCore.QAbstractItemModel):
    def __init__(self, root, parent=None):
        super(SceneGraphModel, self).__init__(parent)
        self._rootNode = root


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
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable

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
                node.setName(value)
                return True
        return False

    def getNode(self, index):
        if index.isValid():
            node = index.internalPointer()
            if node:
                return node
        return self._rootNode

    def insertRows(self, position, rows, parent=QtCore.QModelIndex()):
        parentNode = self.getNode(parent)

        self.beginInsertRows(parent, position, position+rows-1)

        for row in range(rows):
            childcount = parentNode.childcount()
            childNode = Node("untitled" + str(childcount))
            success = parentNode.insertChild(position, childNode) # child inserted, _children grows, childcount counts one more

        self.endInsertRows()

        return success

    def removeRows(self, position, rows, parent=QtCore.QModelIndex()):
        parentNode = self.getNode(parent)

        self.beginRemoveRows(parent, position, position+rows-1)

        for row in range(rows):
            success = parentNode.removeChild(position) # child inserted, _children grows, childcount counts one more

        self.endRemoveRows()

        return success

base, form = uic.loadUiType("mctdhTree.ui")

class WndTutorial05(base, form):
    def __init__(self, parent=None):
        super(base, self).__init__(parent)
        self.setupUi(self)

if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    app.setStyle("plastique")
    tree = Tree("36")
#    tree.addNode("child0", "19", tree._rootNode)
#    tree.addNode("child2", "9", tree._dictNodes["child0"])
    model = SceneGraphModel(tree._rootNode0)
#    RightLeg = model.index(1, 2, QtCore.QModelIndex())
#    model.insertRows(1, 5, RightLeg)
    treeView = QtGui.QTreeView()
    treeView.show()
    treeView.setModel(model)

#    wnd =WndTutorial05()
#    wnd.show()

    sys.exit(app.exec_())
