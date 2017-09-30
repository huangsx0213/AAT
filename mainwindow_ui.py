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
        self.ex_tab = QtWidgets.QWidget()
        self.ex_tab.setObjectName("tab")
        self.addTab(self.ex_tab, "Execution")

        # define the second tab and add it into the QTabWidget.
        self.testcase_tab = QtWidgets.QWidget()
        self.testcase_tab.setObjectName("tab1")
        self.addTab(self.testcase_tab, "TestCase")

        # define the third tab and add it into the QTabWidget.
        self.action_tab = QtWidgets.QWidget()
        self.action_tab.setObjectName("tab2")
        self.addTab(self.action_tab, "Action")

        self.setup_ex_tab()

    def setup_ex_tab(self):
        # define the QGridLayout execution_tab_layout into the execution_tab.
        self.ex_tab_layout = QGridLayout()
        self.ex_tab_layout.setContentsMargins(5, 5, 5, 5)
        self.ex_tab.setLayout(self.ex_tab_layout)
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
        self.ex_right_content_groupbox.setContentsMargins(0, 0, 0, 0)
        # 2.define a gridlayout
        self.ex_right_content_tabwidget = QtWidgets.QTabWidget()
        self.ex_right_content_allex_tab = QtWidgets.QWidget()
        self.ex_right_content_allex_tab.setObjectName("tab422")
        self.ex_right_content_tabwidget.addTab(self.ex_right_content_allex_tab, "All Execution")
        self.ex_right_content_tabwidget.setAutoFillBackground(True)

        self.ex_right_content_gridlayout = QGridLayout()
        self.ex_right_content_gridlayout.setContentsMargins(3, 2,1, 3)
        self.ex_right_content_toolbar=QtWidgets.QToolBar()
        self.ex_right_content_toolbar.addAction("save")
        self.ex_right_content_toolbar.addSeparator()
        self.ex_right_content_toolbar.setAutoFillBackground(True)

        self.ex_right_content_gridlayout.addWidget(self.ex_right_content_toolbar,0,0)
        self.ex_right_content_gridlayout.addWidget(self.ex_right_content_tabwidget, 1, 0)


        self.ex_right_content_groupbox.setLayout(self.ex_right_content_gridlayout)



        # add the left groupbox and  right groupbox into execution_tab_layout
        self.ex_tab_layout.addWidget(self.ex_left_menu_groupbox, 0, 0)
        self.ex_tab_layout.addWidget(self.ex_right_content_groupbox, 0, 1)



