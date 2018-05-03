from PyQt4 import QtCore, QtGui, uic
import sys

class MyMessageBox(QtGui.QMessageBox):
    def __init__(self):
        super(MyMessageBox, self).__init__()

        self._label = QtGui.QLabel('bla')
        self._LineEdit = QtGui.QLineEdit(self)
        self._label.setBuddy(self._LineEdit)
        layout = QtGui.QBoxLayout(QtGui.QBoxLayout.LeftToRight)
        layout.addWidget(self._label)
        layout.addWidget(self._LineEdit)
        self.setLayout(layout)
        


if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    app.setStyle("cleanlooks")
    msg = MyMessageBox()
    msg.setIcon(QtGui.QMessageBox.Information)

    msg.setText('bla?')
    msg.setStandardButtons(QtGui.QMessageBox.Save | QtGui.QMessageBox.Cancel)
    msg.show()

    sys.exit(app.exec_())