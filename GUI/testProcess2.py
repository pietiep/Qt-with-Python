from PyQt4 import QtGui, QtCore
import sys, os

class runcommands(QtGui.QWidget):
    def __init__(self, parent=None):
        super(runcommands, self).__init__(parent)
        self.testPro()

    def testPro(self):
        self.process = QtCore.QProcess(self)
        self.process.setProcessChannelMode(QtCore.QProcess.MergedChannels)
        self.process.readyReadStandardOutput.connect(self.DataRead)
        mctdh = '/home/piet/newRepo/QuantumDynamics/build/bin/mctdh'
        inputFile = '/home/piet/Schreibtisch/masterarbeit/Qt-with-Python/GUI/Projects/pro1/HCHD3/InPut.in'
        self.process.start(mctdh+' '+inputFile)

    def DataRead(self):
        output = str(self.process.readAllStandardOutput())
        print output


def main():
    app = QtGui.QApplication(sys.argv)
    ex = runcommands()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()