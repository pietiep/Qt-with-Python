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

def new():
    b.show()


def selectFile():
    b.lineEdit.setText(QFileDialog.getOpenFileName())
    print(QFileDialog.getOpenFileName())

app = QApplication(sys.argv)
w = loadUi("haupt.ui")
b = loadUi("baum.ui")
w.plainTextEdit.setReadOnly(True)
#w.exec_()
w.connect(w.actionLoad, SIGNAL("activated()"),convert)
w.connect(w.actionLoad2, SIGNAL("activated()"),new)
b.connect(b.Browse, SIGNAL("clicked()"), selectFile)
w.show()
sys.exit(app.exec_())

