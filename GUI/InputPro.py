from PyQt4 import QtCore, QtGui, uic
import sys, os

class ListAbstrModel(QtCore.QAbstractListModel):
    def __init__(self, data=[], parent=None):
        super(ListAbstrModel, self).__init__(parent)
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
        if role == QtCore.Qt.EditRole:
            row = index.row()
            self.__data[row] = str(value.toString())
            return True
        return False

class ListModel(ListAbstrModel):
    def __init__(self, data=[], parent=None):
        super(ListModel, self).__init__(data, parent)
        self.__data = data
        self.__dataBefore = list(data)

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if value not in self.__data:
            if role == QtCore.Qt.EditRole:
                row = index.row()
                self.__data[row] = str(value.toString())
                self.getValue(row)
                return True
        else:
#            self.showdialog(str(value.toString()))
            return False

    def getValue(self, row):
        matches = list(set(self.__data).intersection(self.__dataBefore))
        new = [l_ for l_ in self.__data if l_ not in matches]
        old = [l_ for l_ in self.__dataBefore if l_ not in matches]
        print new, old
        print os.getcwd()
        self.__dataBefore = list(self.__data)
        try:
            os.rename(old[0], new[0])
        except OSError:
            raise

#    def showdialog(self, value):
#        msg = QtGui.QMessageBox()
#        msg.setIcon(QtGui.QMessageBox.Warning)
#
#        msg.setText("Folder %s already exists!" %value)
#        msg.setStandardButtons(QtGui.QMessageBox.Ok)
#
#        retval = msg.exec_()
        
class ListModel2(ListModel):  
    def __init__(self, project, data=[], parent=None):
        super(ListModel2, self).__init__(data, parent)
        self.__data = data
        self.__dataBefore = list(data)
        self._changePath = os.getcwd() + '/' + project

    def getValue(self, row):
        matches = list(set(self.__data).intersection(self.__dataBefore))
        new = [l_ for l_ in self.__data if l_ not in matches]
        old = [l_ for l_ in self.__dataBefore if l_ not in matches]
        self.__dataBefore = list(self.__data)
        os.chdir(self._changePath)
        try:
            os.rename(old[0], new[0])
        except Exception as e:
            self.showdialog(row)


if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    app.setStyle("cleanlooks")
    listmy = ['bla1', 'bla2', 'bla3']
    model = ListModel(listmy)
    listView = QtGui.QListView()
    listView.show()
    listView.setModel(model)
    sys.exit(app.exec_())
