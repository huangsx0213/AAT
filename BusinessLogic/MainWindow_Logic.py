from PyQt5 import QtWidgets, QtSql

from BusinessLogic.Execution_Logic import Execution_Logic
from UserInterface.MainWindow_UI import MainWindow_UI
from ui_mainwindow import Ui_MainWindow


class MainWindow2(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow2, self).__init__(parent)
        self.setupUi(self)


class MainWindow(QtWidgets.QTabWidget, MainWindow_UI, Execution_Logic):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.excution_tab_dic={}
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('.\study\qaat.db')
        db.open()
        self.execution_logic()




