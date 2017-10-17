from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QGridLayout, QGroupBox, QToolBox, QTabBar


class Action_UI:
    def setup_action_main_tab(self):
        # define the QGridLayout action_tab_layout into the action_tab.
        self.ac_tab_layout = QGridLayout()
        self.ac_tab_layout.setContentsMargins(5, 5, 5, 5)
        self.action_main_tab.setLayout(self.ac_tab_layout)

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
        self.ac_right_content_toolbar = QtWidgets.QToolBar()
        self.ac_right_content_toolbar.addAction("new")
        self.ac_right_content_toolbar.addSeparator()
        self.ac_right_content_toolbar.addAction("save")
        self.ac_right_content_toolbar.addSeparator()
        self.ac_right_content_toolbar.setAutoFillBackground(True)
        # 1.define a groupbox
        self.ac_right_content_groupbox = QGroupBox()
        self.ac_right_content_groupbox.setContentsMargins(0, 0, 0, 0)
        # 2.define a gridlayout
        self.ac_right_content_gridlayout = QGridLayout()
        self.ac_right_content_gridlayout.setContentsMargins(3, 2, 1, 3)
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
        # self.ac_right_content_tabwidget.removeTab(0)

        # add the ac_right_content_toolbar and  ac_right_content_tabwidget into gridlayout
        self.ac_right_content_gridlayout.addWidget(self.ac_right_content_toolbar, 0, 0)
        self.ac_right_content_gridlayout.addWidget(self.ac_right_content_tabwidget, 1, 0)
        # add the gridlaout into the groupbox
        self.ac_right_content_groupbox.setLayout(self.ac_right_content_gridlayout)

        # add the left groupbox and  right groupbox into acecution_tab_layout
        self.ac_tab_layout.addWidget(self.ac_left_menu_groupbox, 0, 0)
        self.ac_tab_layout.addWidget(self.ac_right_content_groupbox, 0, 1)