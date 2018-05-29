from PyQt4 import QtGui, QtCore, uic
import sys, os, shutil

base, form = uic.loadUiType("processList.ui")

class DialogD(base, form):
    def __init__(self, parent=None):
        super(base, self).__init__(parent)
        self.setupUi(self)
        self._model = None
        

    def esc(self):
        self.close()