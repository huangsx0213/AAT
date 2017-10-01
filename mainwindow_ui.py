from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QCoreApplication, QModelIndex
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QGridLayout, QToolBox, QLabel, QGroupBox, QTabBar
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
        self.tc_tab = QtWidgets.QWidget()
        self.tc_tab.setObjectName("tab1")
        self.addTab(self.tc_tab, "TestCase")

        # define the third tab and add it into the QTabWidget.
        self.ac_tab = QtWidgets.QWidget()
        self.ac_tab.setObjectName("tab2")
        self.addTab(self.ac_tab, "Action")

        self.setup_ex_tab()
        self.setup_tc_tab()
        self.setup_ac_tab()

    def setup_ex_tab(self):
        # define the QGridLayout execution_tab_layout into the execution_tab.
        self.ex_tab_layout = QGridLayout()
        self.ex_tab_layout.setContentsMargins(5, 5, 5, 5)
        self.ex_tab.setLayout(self.ex_tab_layout)

        # define the left groupbox
        # 1. define a groupbox
        self.ex_left_menu_groupbox = QGroupBox()
        self.ex_left_menu_groupbox.setFixedWidth(185)
        # 2.define a gridlayout
        self.ex_left_menu_gridlayout = QGridLayout()
        self.ex_left_menu_gridlayout.setContentsMargins(2, 2, 2, 2)
        # 3.define a toolbox
        self.ex_left_menu_listview = QtWidgets.QListView()
        self.ex_left_menu_toolbox = QToolBox()
        self.ex_left_menu_toolbox.addItem(self.ex_left_menu_listview, "Execution")
        # add the toolbox into gridlayout
        self.ex_left_menu_gridlayout.addWidget(self.ex_left_menu_toolbox)
        # add the gridlaout into the groupbox
        self.ex_left_menu_groupbox.setLayout(self.ex_left_menu_gridlayout)

        # define the right groupbox
        # 0.define the save toolbar
        self.ex_right_content_toolbar=QtWidgets.QToolBar()
        self.ex_right_content_toolbar.addAction("save")
        self.ex_right_content_toolbar.addSeparator()
        self.ex_right_content_toolbar.setAutoFillBackground(True)
        # 1.define a groupbox
        self.ex_right_content_groupbox = QGroupBox()
        self.ex_right_content_groupbox.setContentsMargins(0, 0, 0, 0)
        # 2.define a gridlayout
        self.ex_right_content_gridlayout = QGridLayout()
        self.ex_right_content_gridlayout.setContentsMargins(3, 2,1, 3)
        # 3.define a tabwidget
        # first page of the tabwidget
        self.ex_right_content_allex_tab = QtWidgets.QWidget()
        self.ex_right_content_allex_tab.setObjectName("tab3")
        # define the tabwidget add the first page
        self.ex_right_content_tabwidget = QtWidgets.QTabWidget()
        self.ex_right_content_tabwidget.addTab(self.ex_right_content_allex_tab, "All Executions")
        self.ex_right_content_tabwidget.setAutoFillBackground(True)
        self.ex_right_content_tabwidget.setTabsClosable(True)
        # set the index 0 page hasn't colse button
        QTabBar.setTabButton(self.ex_right_content_tabwidget.tabBar(), 0, QTabBar.RightSide, None)
        #self.ex_right_content_tabwidget.removeTab(0)

        # add the ex_right_content_toolbar and  ex_right_content_tabwidget into gridlayout
        self.ex_right_content_gridlayout.addWidget(self.ex_right_content_toolbar,0,0)
        self.ex_right_content_gridlayout.addWidget(self.ex_right_content_tabwidget, 1, 0)
        # add the gridlaout into the groupbox
        self.ex_right_content_groupbox.setLayout(self.ex_right_content_gridlayout)

        # add the left groupbox and  right groupbox into execution_tab_layout
        self.ex_tab_layout.addWidget(self.ex_left_menu_groupbox, 0, 0)
        self.ex_tab_layout.addWidget(self.ex_right_content_groupbox, 0, 1)

        # add first page for each listdata
        self.ex_right_content_allts_tab = QtWidgets.QWidget()
        self.ex_right_content_allts_tab.setObjectName("tab4")

        self.ex_right_content_allva_tab = QtWidgets.QWidget()
        self.ex_right_content_allva_tab.setObjectName("tab5")

        self.ex_right_content_allma_tab = QtWidgets.QWidget()
        self.ex_right_content_allma_tab.setObjectName("tab6")
    def setup_tc_tab(self):
        # define the QGridLayout testcases_tab_layout into the testcases_tab.
        self.tc_tab_layout = QGridLayout()
        self.tc_tab_layout.setContentsMargins(5, 5, 5, 5)
        self.tc_tab.setLayout(self.tc_tab_layout)

        # define the left groupbox
        # 1. define a groupbox
        self.tc_left_menu_groupbox = QGroupBox()
        self.tc_left_menu_groupbox.setFixedWidth(185)
        # 2.define a gridlayout
        self.tc_left_menu_gridlayout = QGridLayout()
        self.tc_left_menu_gridlayout.setContentsMargins(2, 2, 2, 2)
        # 3.define a toolbox
        self.tc_left_menu_listview = QtWidgets.QListView()
        self.tctree_left_menu_listview = QtWidgets.QListView()
        self.tc_left_menu_toolbox = QToolBox()
        self.tc_left_menu_toolbox.addItem(self.tc_left_menu_listview, "Test Cases")
        self.tc_left_menu_toolbox.addItem(self.tctree_left_menu_listview, "Test Cases Tree")
        # add the toolbox into gridlayout
        self.tc_left_menu_gridlayout.addWidget(self.tc_left_menu_toolbox)
        # add the gridlaout into the groupbox
        self.tc_left_menu_groupbox.setLayout(self.tc_left_menu_gridlayout)

        # define the right groupbox
        # 0.define the save toolbar
        self.tc_right_content_toolbar=QtWidgets.QToolBar()
        self.tc_right_content_toolbar.addAction("save")
        self.tc_right_content_toolbar.addSeparator()
        self.tc_right_content_toolbar.setAutoFillBackground(True)
        # 1.define a groupbox
        self.tc_right_content_groupbox = QGroupBox()
        self.tc_right_content_groupbox.setContentsMargins(0, 0, 0, 0)
        # 2.define a gridlayout
        self.tc_right_content_gridlayout = QGridLayout()
        self.tc_right_content_gridlayout.setContentsMargins(3, 2,1, 3)
        # 3.define a tabwidget
        # first page of the tabwidget
        self.tc_right_content_alltc_tab = QtWidgets.QWidget()
        self.tc_right_content_alltc_tab.setObjectName("tab3")
        # define the tabwidget add the first page
        self.tc_right_content_tabwidget = QtWidgets.QTabWidget()
        self.tc_right_content_tabwidget.addTab(self.tc_right_content_alltc_tab, "one test case")
        self.tc_right_content_tabwidget.setAutoFillBackground(True)
        self.tc_right_content_tabwidget.setTabsClosable(True)
        # set the indtc 0 page hasn't colse button
        QTabBar.setTabButton(self.tc_right_content_tabwidget.tabBar(), 0, QTabBar.RightSide, None)
        #self.tc_right_content_tabwidget.removeTab(0)

        # add the tc_right_content_toolbar and  tc_right_content_tabwidget into gridlayout
        self.tc_right_content_gridlayout.addWidget(self.tc_right_content_toolbar,0,0)
        self.tc_right_content_gridlayout.addWidget(self.tc_right_content_tabwidget, 1, 0)
        # add the gridlaout into the groupbox
        self.tc_right_content_groupbox.setLayout(self.tc_right_content_gridlayout)

        # add the left groupbox and  right groupbox into tcecution_tab_layout
        self.tc_tab_layout.addWidget(self.tc_left_menu_groupbox, 0, 0)
        self.tc_tab_layout.addWidget(self.tc_right_content_groupbox, 0, 1)
    def setup_ac_tab(self):
        # define the QGridLayout action_tab_layout into the action_tab.
        self.ac_tab_layout = QGridLayout()
        self.ac_tab_layout.setContentsMargins(5, 5, 5, 5)
        self.ac_tab.setLayout(self.ac_tab_layout)

        # define the left groupbox
        # 1. define a groupbox
        self.ac_left_menu_groupbox = QGroupBox()
        self.ac_left_menu_groupbox.setFixedWidth(185)
        # 2.define a gridlayout
        self.ac_left_menu_gridlayout = QGridLayout()
        self.ac_left_menu_gridlayout.setContentsMargins(2, 2, 2, 2)
        # 3.define a toolbox
        self.ac_left_menu_listview = QtWidgets.QListView()
        self.actree_left_menu_listview = QtWidgets.QListView()
        self.ac_left_menu_toolbox = QToolBox()
        self.ac_left_menu_toolbox.addItem(self.ac_left_menu_listview, "Actions")
        self.ac_left_menu_toolbox.addItem(self.actree_left_menu_listview, "Actions Tree")
        # add the toolbox into gridlayout
        self.ac_left_menu_gridlayout.addWidget(self.ac_left_menu_toolbox)
        # add the gridlaout into the groupbox
        self.ac_left_menu_groupbox.setLayout(self.ac_left_menu_gridlayout)

        # define the right groupbox
        # 0.define the save toolbar
        self.ac_right_content_toolbar=QtWidgets.QToolBar()
        self.ac_right_content_toolbar.addAction("save")
        self.ac_right_content_toolbar.addSeparator()
        self.ac_right_content_toolbar.setAutoFillBackground(True)
        # 1.define a groupbox
        self.ac_right_content_groupbox = QGroupBox()
        self.ac_right_content_groupbox.setContentsMargins(0, 0, 0, 0)
        # 2.define a gridlayout
        self.ac_right_content_gridlayout = QGridLayout()
        self.ac_right_content_gridlayout.setContentsMargins(3, 2,1, 3)
        # 3.define a tabwidget
        # first page of the tabwidget
        self.ac_right_content_allac_tab = QtWidgets.QWidget()
        self.ac_right_content_allac_tab.setObjectName("tab3")
        # define the tabwidget add the first page
        self.ac_right_content_tabwidget = QtWidgets.QTabWidget()
        self.ac_right_content_tabwidget.addTab(self.ac_right_content_allac_tab, "one action")
        self.ac_right_content_tabwidget.setAutoFillBackground(True)
        self.ac_right_content_tabwidget.setTabsClosable(True)
        # set the indac 0 page hasn't colse button
        QTabBar.setTabButton(self.ac_right_content_tabwidget.tabBar(), 0, QTabBar.RightSide, None)
        #self.ac_right_content_tabwidget.removeTab(0)

        # add the ac_right_content_toolbar and  ac_right_content_tabwidget into gridlayout
        self.ac_right_content_gridlayout.addWidget(self.ac_right_content_toolbar,0,0)
        self.ac_right_content_gridlayout.addWidget(self.ac_right_content_tabwidget, 1, 0)
        # add the gridlaout into the groupbox
        self.ac_right_content_groupbox.setLayout(self.ac_right_content_gridlayout)

        # add the left groupbox and  right groupbox into acecution_tab_layout
        self.ac_tab_layout.addWidget(self.ac_left_menu_groupbox, 0, 0)
        self.ac_tab_layout.addWidget(self.ac_right_content_groupbox, 0, 1)



