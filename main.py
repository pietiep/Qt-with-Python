import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.uic import *

def convert():
    x=1
    with open("config.txt") as f:
        content = f.readlines()
        content = "".join(content)
        print repr(content)
    w.plainTextEdit.setPlainText(content)

app = QApplication(sys.argv)
w = loadUi("haupt.ui")
w.plainTextEdit.setReadOnly(True)
#w.exec_()
w.connect(w.actionLoad, SIGNAL("activated()"),convert)
w.show()
sys.exit(app.exec_())

