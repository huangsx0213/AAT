from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QGridLayout, QGroupBox, QToolBox, QTabBar


class Testcase_UI:
    def setup_testcase_ui(self):
        # define the second tab and add it into the QTabWidget.
        self.testcase_main_tab = QtWidgets.QWidget()
        self.testcase_main_tab.setObjectName("testcase_main_tab")
        self.addTab(self.testcase_main_tab, "TestCase")


        self.setup_testcase_main_tab()

    def setup_testcase_main_tab(self):
        # define the QGridLayout testcases_tab_layout into the testcases_tab.
        self.tc_tab_layout = QGridLayout()
        self.tc_tab_layout.setContentsMargins(5, 5, 5, 5)
        self.testcase_main_tab.setLayout(self.tc_tab_layout)

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
        self.tc_right_content_toolbar = QtWidgets.QToolBar()
        self.tc_right_content_toolbar.addAction("new")
        self.tc_right_content_toolbar.addSeparator()
        self.tc_right_content_toolbar.addAction("save")
        self.tc_right_content_toolbar.addSeparator()
        self.tc_right_content_toolbar.setAutoFillBackground(True)
        # 1.define a groupbox
        self.tc_right_content_groupbox = QGroupBox()
        self.tc_right_content_groupbox.setContentsMargins(0, 0, 0, 0)
        # 2.define a gridlayout
        self.tc_right_content_gridlayout = QGridLayout()
        self.tc_right_content_gridlayout.setContentsMargins(3, 2, 1, 3)
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
        # self.tc_right_content_tabwidget.removeTab(0)

        # add the tc_right_content_toolbar and  tc_right_content_tabwidget into gridlayout
        self.tc_right_content_gridlayout.addWidget(self.tc_right_content_toolbar, 0, 0)
        self.tc_right_content_gridlayout.addWidget(self.tc_right_content_tabwidget, 1, 0)
        # add the gridlaout into the groupbox
        self.tc_right_content_groupbox.setLayout(self.tc_right_content_gridlayout)

        # add the left groupbox and  right groupbox into tcecution_tab_layout
        self.tc_tab_layout.addWidget(self.tc_left_menu_groupbox, 0, 0)
        self.tc_tab_layout.addWidget(self.tc_right_content_groupbox, 0, 1)