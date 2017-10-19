from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon

from UserInterface.Action_UI import Action_UI
from UserInterface.Execution_UI import Execution_UI
from UserInterface.Testcase_UI import Testcase_UI


class MainWindow_UI(Execution_UI, Testcase_UI, Action_UI):
    def __init__(self):
        # settings of MainWindow,the QTabWidget.
        self.setWindowIcon(QIcon('.\images\logo.png'))
        self.resize(1020, 600)
        self.setWindowTitle('AAT 2.0')

        self.setup_execution_ui()
        self.setup_testcase_ui()
        self.setup_action_ui()