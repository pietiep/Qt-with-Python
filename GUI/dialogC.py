from PyQt4 import QtCore, QtGui, uic
from PyQt4 import *
import sys, os
from widgetA import WidgetA

base, form = uic.loadUiType("dialogNewName.ui")

class DialogC(base, form):
    def __init__(self, parent=None):
        super(base, self).__init__(parent)
        self.setupUi(self)

        self._FolderName = ""

        self.uiWarning.setText('')
        self.uiFolderName.setText("Give name for new Folder!")
        self.uiFolderName.selectAll()
        self.uiFolderName.textChanged.connect(self.change0)
        self.uiSaveBu.clicked.connect(self.save)
        self.uiCancelBu.clicked.connect(self.esc)
    
    def setWarning(self, warningUi):
        self.uiWarning.setText(warningUi)

    def save(self):
        self._FolderName = self.uiFolderName.text()
        if ' ' not in self._FolderName:
            self.close()
        else:
            self.setWarning(str('Name contains whitespace'))
            print 'Name contains whitespace'

    def esc(self):
        self._FolderName = "Cancel"
        self.close()

    def change0(self):
        self._FolderName = self.uiFolderName.text()


if __name__ == '__main__':
    
    app = QtGui.QApplication(sys.argv)
    app.setStyle("cleanlooks")
    wnd = DialogC()
    wnd.show()
    sys.exit(app.exec_())
