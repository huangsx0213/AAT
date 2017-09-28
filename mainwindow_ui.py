from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QGridLayout, QToolBox, QLabel, QGroupBox


class MainWindow_Ui(object):
    def setupUi(self, MainWindow):

        #settings of MainWindow,the QTabWidget.
        self.setWindowIcon(QIcon('.\images\logo.png'))
        self.resize(800, 600)
        self.setWindowTitle('AAT 2.0')

        # define the first tab and add it into the QTabWidget.
        self.execution_tab = QtWidgets.QWidget()
        self.execution_tab.setObjectName("tab")
        self.addTab(self.execution_tab, "Execution")

        # define the second tab and add it into the QTabWidget.
        self.testcase_tab = QtWidgets.QWidget()
        self.testcase_tab.setObjectName("tab1")
        self.addTab(self.testcase_tab, "TestCase")

        # define the third tab and add it into the QTabWidget.
        self.action_tab = QtWidgets.QWidget()
        self.action_tab.setObjectName("tab2")
        self.addTab(self.action_tab, "Action")

        self.setup_execution_tab()

    def setup_execution_tab(self):
        # define the QGridLayout execution_tab_layout into the execution_tab.
        self.execution_tab_layout = QGridLayout()
        self.execution_tab_layout.setContentsMargins(5, 5, 5, 5)
        self.execution_tab.setLayout(self.execution_tab_layout)
        # define the left groupbox
        # 1. definea groupbox
        self.left_groupbox = QGroupBox()
        self.left_groupbox.setFixedWidth(185)
        # 2.define a gridlayout
        self.left_gridlayout = QGridLayout()
        self.left_gridlayout.setContentsMargins(2, 2, 2, 2)
        # 3.define a toolbox
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.left_toolbox = QToolBox()
        self.left_toolbox.addItem(self.page, "Execution")

        self.left_gridlayout.addWidget(self.left_toolbox)
        self.left_groupbox.setLayout(self.left_gridlayout)

        # define the right groupbox
        self.left_groupbox2 = QGroupBox()

        # add the left groupbox and  right groupbox into execution_tab_layout
        self.execution_tab_layout.addWidget(self.left_groupbox, 0, 0)
        self.execution_tab_layout.addWidget(self.left_groupbox2, 0, 1)