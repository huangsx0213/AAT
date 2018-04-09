from PyQt5 import QtSql
from PyQt5.QtWidgets import QTabWidget

from BusinessLogic.ExecutionLogic import ExecutionLogic
from BusinessLogic.ExecutionMenuLogic import ExecutionMenuLogic
from BusinessLogic.TestCaseMenuLogic import TestcaseMenuLogic
from BusinessLogic.TestSetLogic import TestSetLogic
from BusinessLogic.TestCaseLogic import TestCaseLogic
class MainWindow(QTabWidget, ExecutionLogic, TestSetLogic, ExecutionMenuLogic, TestcaseMenuLogic, TestCaseLogic):
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