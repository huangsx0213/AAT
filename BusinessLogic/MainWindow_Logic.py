from PyQt5 import QtSql
from PyQt5.QtWidgets import QTabWidget

from BusinessLogic.Execution_Logic import Execution_Logic
from BusinessLogic.Execution_Menu_Logic import Execution_Menu_Logic
from BusinessLogic.Testcase_Menu_Logic import Testcase_Menu_Logic
from BusinessLogic.TestSet_Logic import TestSet_Logic
from BusinessLogic.Test_Case_Logic import Test_Case_Logic
class MainWindow(QTabWidget, Execution_Logic, TestSet_Logic, Execution_Menu_Logic,Testcase_Menu_Logic,Test_Case_Logic):
    def __init__(self):
        super().__init__()

        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('.\DataBase\QAAT.db')
        db.open()
        db.exec('pragma foreign_keys=ON')


        self.execution_menu_logic()
        self.testcase_menu_logic()
        self.execution_logic()
        self.testset_logic()
        self.test_case_logic()