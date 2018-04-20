from PyQt4 import QtCore, QtGui
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
#        return QtCore.Qt.ItemIsEnabled |QtCore.Qt.ItemIsSelectable

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
        self._messageBu = False

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if value not in self.__data:
            if role == QtCore.Qt.EditRole:
                row = index.row()
                self.__data[row] = str(value.toString())
                self.getValue()
                return True
        else:
            return False

    def getValue(self):
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

    def removeRows(self, position, rows, parent=QtCore.QModelIndex()):
        self.beginRemoveRows(parent, position, position+rows-1)

        value = self.__data[position]
        self.showdialog(value)
        if self._messageBu == 'OK':
            for i in range(rows):    
                value = self.__data[position]   
                self.__data.remove(value)
            self.endRemoveRows()
            return True
        else:
            self.endRemoveRows()
            return False
            
    def showdialog(self, value):
        msg = QtGui.QMessageBox()
        msg.setIcon(QtGui.QMessageBox.Warning)

        msg.setText("Are sure you want to delete Folder %s?" %value)
        msg.setStandardButtons(QtGui.QMessageBox.Ok| QtGui.QMessageBox.Cancel)

        msg.buttonClicked.connect(self.msgbtn)
        msg.exec_()

    def msgbtn(self, i):
        self._messageBu = str(i.text())
        
class ListModel2(ListModel):  
    def __init__(self, project, data=[], parent=None):
        super(ListModel2, self).__init__(data, parent)
        self.__data = data
        self.__dataBefore = list(data)
        self._changePath = os.getcwd() + '/' + project

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if value not in self.__data:
            if role == QtCore.Qt.EditRole:
                row = index.row()
                self.__data[row] = str(value.toString())
                self.getValue(row)
                return True
        else:
            return False

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

    def removeRows(self, position, rows, parent=QtCore.QModelIndex()):
        self.beginRemoveRows(parent, position, position+rows-1)

        value = self.__data[position]
#        self.showdialog(value)
#        if self._messageBu == 'OK':
        for i in range(rows):    
            value = self.__data[position]   
            self.__data.remove(value)
        self.endRemoveRows()
        return True
 #       else:
 #           self.endRemoveRows()
 #           return False

if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    app.setStyle("cleanlooks")
    listmy = ['bla1', 'bla2', 'bla3', 'bla4']
    model = ListModel(listmy)
    proxy = QtGui.QSortFilterProxyModel()
    proxy.setSourceModel(model)
    proxy.sort(0, QtCore.Qt.AscendingOrder)
    listView = QtGui.QListView()
    listView.setModel(proxy)
    listView.show()
    model.removeRows(0,1)
    sys.exit(app.exec_())
