import sys

from BusinessLogic.MainWindow_Logic import *

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow=MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())