from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QCoreApplication, QModelIndex
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QGridLayout, QToolBox, QLabel, QGroupBox
from PyQt5.QtGui import QStandardItemModel, QStandardItem

class MainWindow_Ui(object):
    def setupUi(self, MainWindow):

        #settings of MainWindow,the QTabWidget.
        self.setWindowIcon(QIcon('.\images\logo.png'))
        self.resize(1020, 600)
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
        self.ex_left_menu_groupbox = QGroupBox()
        self.ex_left_menu_groupbox.setFixedWidth(185)
        # 2.define a gridlayout
        self.ex_left_menu_gridlayout = QGridLayout()
        self.ex_left_menu_gridlayout.setContentsMargins(2, 2, 2, 2)
        # 3.define a toolbox
        self.ex_left_menu_listview = QtWidgets.QListView()
        self.ex_left_menu_toolbox = QToolBox()
        self.ex_left_menu_toolbox.addItem(self.ex_left_menu_listview, "Execution")

        self.ex_left_menu_gridlayout.addWidget(self.ex_left_menu_toolbox)
        self.ex_left_menu_groupbox.setLayout(self.ex_left_menu_gridlayout)

        # define the right groupbox
        self.ex_right_content_groupbox = QGroupBox()
        # 2.define a gridlayout
        self.taba = QtWidgets.QTabWidget()
        self.taba.setContentsMargins(0, 0, 0, 0)
        self.tabpage = QtWidgets.QTabWidget()
        self.tabpage.setObjectName("tab422")
        self.taba.addTab(self.tabpage, "Execution")
        self.ex_right_content_gridlayout = QGridLayout()
        self.ex_right_content_gridlayout.setContentsMargins(2, 2, 2, 2)
        self.ex_right_content_gridlayout.addWidget(self.taba)

        self.ex_right_content_groupbox.setLayout(self.ex_right_content_gridlayout)



        # add the left groupbox and  right groupbox into execution_tab_layout
        self.execution_tab_layout.addWidget(self.ex_left_menu_groupbox, 0, 0)
        self.execution_tab_layout.addWidget(self.ex_right_content_groupbox, 0, 1)



