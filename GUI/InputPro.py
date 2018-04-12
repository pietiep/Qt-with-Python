from PyQt4 import QtCore, QtGui, uic
import sys

class ListModel(QtCore.QAbstractListModel):
    def __init__(self, data=[], parent=None):
        super(ListModel, self).__init__(parent)
        self.__data = data

    def rowCount(self, parent):
        return len(self.__data)

    def data(self, index, role):
        if role == QtCore.Qt.EditRole:
            row = index.row()
            return self.__data[row]

        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            value = self.__data[row]
            return value

    def flags(self, index):
        return QtCore.Qt.ItemIsEditable |QtCore.Qt.ItemIsEnabled |QtCore.Qt.ItemIsSelectable

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        print str(value.toString()), "from setData"
        if role == QtCore.Qt.EditRole:
            row = index.row()
            self.__data[row] = value
            return True
        return False

if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    app.setStyle("cleanlooks")
    listmy = ['bla1', 'bla2', 'bla3']
    model = ListModel(listmy)
    listView = QtGui.QListView()
    listView.show()
    listView.setModel(model)
    sys.exit(app.exec_())
