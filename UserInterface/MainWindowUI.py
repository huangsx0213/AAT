from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon

from UserInterface.ActionUI import ActionUI
from UserInterface.ExecutionUI import ExecutionUI
from UserInterface.TestCaseUI import TestCaseUI


class MainWindowUI(ExecutionUI, TestCaseUI, ActionUI):
    def __init__(self):
        # settings of MainWindow,the QTabWidget.
        self.setWindowIcon(QIcon('.\images\logo.png'))
        self.resize(1020, 600)
        self.setWindowTitle('AAT 2.0')

        self.setup_execution_ui()
        self.setup_testcase_ui()
        self.setup_action_ui()
