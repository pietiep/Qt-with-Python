from PyQt4 import QtCore, QtGui
import sys
from Node import Node, TransformNode, CameraNode, LightNode
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
        return 1
    #    return 2

    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if section == 0:
                return "Scenegraph"
            else:
                return "Type"

    def data(self, index, role):

        if not index.isValid():
            return None

        node = index.internalPointer()

        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole: #Name is always displayed
            if index.column() == 0:
                return node.name()
        #    else:
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

if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    app.setStyle("plastique")

    rootNode = LightNode("Hips")
    childNode0 = LightNode("LeftPirateLeg", rootNode)
    childNode1 = CameraNode("RightLeg", rootNode)
    childNode2 = TransformNode("RightFoot", childNode1)
    #print rootNode._children
    #print childNode0._children
    print rootNode

    model = SceneGraphModel(rootNode)
    RightLeg = model.index(1, 2, QtCore.QModelIndex())
    model.insertRows(1, 5, RightLeg)
    treeView = QtGui.QTreeView()
    treeView.show()
    treeView.setModel(model)
    sys.exit(app.exec_())
