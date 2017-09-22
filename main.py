from PyQt5 import QtCore, QtGui, QtWidgets
from mainwindow import *
import sys

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow2 = MainWindow2()
    #mainWindow2.show()
    mainWindow=MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())