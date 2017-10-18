from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon

from UserInterface.Action_UI import Action_UI
from UserInterface.Execution_UI import Execution_UI
from UserInterface.Testcase_UI import Testcase_UI


class MainWindow_UI(Execution_UI, Testcase_UI, Action_UI):
    def __init__(self):
        pass
    def setupUi(self):
        # settings of MainWindow,the QTabWidget.
        self.setWindowIcon(QIcon('.\images\logo.png'))
        self.resize(1020, 600)
        self.setWindowTitle('AAT 2.0')

        # define the first tab and add it into the QTabWidget.
        self.execution_main_tab = QtWidgets.QWidget()
        self.execution_main_tab.setObjectName("execution_main_tab")
        self.addTab(self.execution_main_tab, "Execution")

        # define the second tab and add it into the QTabWidget.
        self.testcase_main_tab = QtWidgets.QWidget()
        self.testcase_main_tab.setObjectName("testcase_main_tab")
        self.addTab(self.testcase_main_tab, "TestCase")

        # define the third tab and add it into the QTabWidget.
        self.action_main_tab = QtWidgets.QWidget()
        self.action_main_tab.setObjectName("action_main_tab")
        self.addTab(self.action_main_tab, "Action")

        self.setup_execution_main_tab()
        self.setup_testcase_main_tab()
        self.setup_action_main_tab()
