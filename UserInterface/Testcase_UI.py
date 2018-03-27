from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QGridLayout, QGroupBox, QToolBox, QTabBar, QAction


class Testcase_UI:
    def setup_testcase_ui(self):
        # define the second tab and add it into the QTabWidget.
        self.testcase_main_tab = QtWidgets.QWidget()
        self.testcase_main_tab.setObjectName("testcase_main_tab")
        self.addTab(self.testcase_main_tab, "TestCase")

        self.setup_testcase_main_tab()

    def setup_testcase_main_tab(self):
        # define the QGridLayout testcases_tab_layout into the testcases_tab.
        self.testcase_main_tab_layout = QGridLayout()
        self.testcase_main_tab_layout.setContentsMargins(5, 5, 5, 5)
        self.testcase_main_tab.setLayout(self.testcase_main_tab_layout)

        # define the left groupbox
        # 1. define a groupbox
        self.testcase_menu_groupbox = QGroupBox()
        self.testcase_menu_groupbox.setFixedWidth(185)
        # 2.define a gridlayout
        self.testcase_menu_gridlayout = QGridLayout()
        self.testcase_menu_gridlayout.setContentsMargins(2, 2, 2, 2)
        # 3.define a toolbox
        self.testcase_menu_listview = QtWidgets.QListView()
        self.testcase_tree_menu_listview = QtWidgets.QListView()
        self.testcase_menu_toolbox = QToolBox()
        self.testcase_menu_toolbox.addItem(self.testcase_menu_listview, "Test Cases")
        self.testcase_menu_toolbox.addItem(self.testcase_tree_menu_listview, "Test Cases Tree")
        self.testcase_menu_toolbox.setCurrentIndex(1)
        # add the toolbox into gridlayout
        self.testcase_menu_gridlayout.addWidget(self.testcase_menu_toolbox)
        # add the gridlaout into the groupbox
        self.testcase_menu_groupbox.setLayout(self.testcase_menu_gridlayout)

        # define the right groupbox
        # 0.define the save toolbar
        self.testcase_right_content_toolbar = QtWidgets.QToolBar()
        new = QAction(QIcon("./images/add.png"), "new", self)
        self.testcase_right_content_toolbar.addAction(new)
        #self.testcase_right_content_toolbar.addSeparator()
        save = QAction(QIcon("./images/save.png"), "save", self)
        self.testcase_right_content_toolbar.addAction(save)
        self.testcase_right_content_toolbar.addSeparator()
        self.testcase_right_content_toolbar.setAutoFillBackground(True)
        # 1.define a groupbox
        self.testcase_right_content_groupbox = QGroupBox()
        self.testcase_right_content_groupbox.setContentsMargins(0, 0, 0, 0)
        # 2.define a gridlayout
        self.testcase_right_content_gridlayout = QGridLayout()
        self.testcase_right_content_gridlayout.setContentsMargins(3, 2, 1, 3)
        # 3.define a tabwidget
        # first page of the tabwidget
        self.all_testcase_tab = QtWidgets.QWidget()
        self.all_testcase_tab.setObjectName("all_testcase_tab")
        # define the tabwidget add the first page
        self.testcase_tabwidget = QtWidgets.QTabWidget()
        self.testcase_tabwidget.addTab(self.all_testcase_tab, "one test case")
        self.testcase_tabwidget.setAutoFillBackground(True)
        self.testcase_tabwidget.setTabsClosable(True)
        # set the indtc 0 page hasn't colse button
        QTabBar.setTabButton(self.testcase_tabwidget.tabBar(), 0, QTabBar.RightSide, None)
        # self.tc_right_content_tabwidget.removeTab(0)

        # add the tc_right_content_toolbar and  tc_right_content_tabwidget into gridlayout
        self.testcase_right_content_gridlayout.addWidget(self.testcase_right_content_toolbar, 0, 0)
        self.testcase_right_content_gridlayout.addWidget(self.testcase_tabwidget, 1, 0)
        # add the gridlaout into the groupbox
        self.testcase_right_content_groupbox.setLayout(self.testcase_right_content_gridlayout)

        # add the left groupbox and  right groupbox into tcecution_tab_layout
        self.testcase_main_tab_layout.addWidget(self.testcase_menu_groupbox, 0, 0)
        self.testcase_main_tab_layout.addWidget(self.testcase_right_content_groupbox, 0, 1)
