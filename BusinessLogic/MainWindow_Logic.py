from PyQt5 import QtSql
from PyQt5.QtWidgets import QTabWidget

from BusinessLogic.Execution_Logic import Execution_Logic
from BusinessLogic.TestSet_Logic import TestSet_Logic


class MainWindow(QTabWidget, Execution_Logic, TestSet_Logic):
    def __init__(self):
        super().__init__()

        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('.\study\qaat.db')
        db.open()

        self.execution_logic()
        self.testset_logic()
