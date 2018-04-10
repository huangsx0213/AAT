from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QGridLayout, QGroupBox, QToolBox, QTabBar, QAction, QLabel, QLineEdit, QVBoxLayout, \
    QTextEdit

from UserInterface.CustomGroupBox import CustomGroupBox


class TestCaseUI:
    def setup_test_case_ui(self):
        # define the second tab and add it into the QTabWidget.
        self.test_case_main_tab = QtWidgets.QWidget()
        self.test_case_main_tab.setObjectName("testcase_main_tab")
        self.addTab(self.test_case_main_tab, "TestCase")

        self.setup_test_case_main_tab()

    def setup_test_case_main_tab(self):
        # define the QGridLayout testcases_tab_layout into the testcases_tab.
        self.test_case_main_tab_layout = QGridLayout()
        self.test_case_main_tab_layout.setContentsMargins(5, 5, 5, 5)
        self.test_case_main_tab.setLayout(self.test_case_main_tab_layout)

        # define the left groupbox
        # 1. define a groupbox
        self.test_case_menu_groupbox = QGroupBox()
        self.test_case_menu_groupbox.setFixedWidth(185)
        # 2.define a gridlayout
        self.test_case_menu_gridlayout = QGridLayout()
        self.test_case_menu_gridlayout.setContentsMargins(2, 2, 2, 2)
        # 3.define a toolbox
        self.test_case_menu_listview = QtWidgets.QListView()
        self.test_case_tree_menu_listview = QtWidgets.QListView()
        self.test_case_menu_toolbox = QToolBox()
        self.test_case_menu_toolbox.addItem(self.test_case_menu_listview, "Test Cases")
        self.test_case_menu_toolbox.addItem(self.test_case_tree_menu_listview, "Test Cases Tree")
        self.test_case_menu_toolbox.setCurrentIndex(1)
        # add the toolbox into gridlayout
        self.test_case_menu_gridlayout.addWidget(self.test_case_menu_toolbox)
        # add the gridlaout into the groupbox
        self.test_case_menu_groupbox.setLayout(self.test_case_menu_gridlayout)

        # define the right groupbox
        # 0.define the save toolbar
        self.test_case_right_content_toolbar = QtWidgets.QToolBar()
        new = QAction(QIcon("./images/add.png"), "new", self)
        self.test_case_right_content_toolbar.addAction(new)
        #self.testcase_right_content_toolbar.addSeparator()
        save = QAction(QIcon("./images/save.png"), "save", self)
        self.test_case_right_content_toolbar.addAction(save)
        self.test_case_right_content_toolbar.addSeparator()
        self.test_case_right_content_toolbar.setAutoFillBackground(True)
        # 1.define a groupbox
        self.test_case_right_content_groupbox = QGroupBox()
        self.test_case_right_content_groupbox.setContentsMargins(0, 0, 0, 0)
        # 2.define a gridlayout
        self.test_case_right_content_gridlayout = QGridLayout()
        self.test_case_right_content_gridlayout.setContentsMargins(3, 2, 1, 3)
        # 3.define a tabwidget

        # define the tabwidget add the first page
        self.test_case_tabwidget = QtWidgets.QTabWidget()

        self.test_case_tabwidget.setAutoFillBackground(True)
        self.test_case_tabwidget.setTabsClosable(True)
        # close the tab
        self.test_case_tabwidget.tabCloseRequested.connect(self.test_case_tabwidget.removeTab)
        # set the indtc 0 page hasn't colse button
        QTabBar.setTabButton(self.test_case_tabwidget.tabBar(), 0, QTabBar.RightSide, None)
        # self.tc_right_content_tabwidget.removeTab(0)

        # add the tc_right_content_toolbar and  tc_right_content_tabwidget into gridlayout
        self.test_case_right_content_gridlayout.addWidget(self.test_case_right_content_toolbar, 0, 0)
        self.test_case_right_content_gridlayout.addWidget(self.test_case_tabwidget, 1, 0)
        # add the gridlaout into the groupbox
        self.test_case_right_content_groupbox.setLayout(self.test_case_right_content_gridlayout)

        # add the left groupbox and  right groupbox into tcecution_tab_layout
        self.test_case_main_tab_layout.addWidget(self.test_case_menu_groupbox, 0, 0)
        self.test_case_main_tab_layout.addWidget(self.test_case_right_content_groupbox, 0, 1)

    def setup_dynamic_test_case_tab(self, name=None):
        # 1. define a page
        self.one_dynamic_test_case_tab = QtWidgets.QWidget()
        self.one_dynamic_test_case_tab.setObjectName(name)
        # 2. define a layout
        self.one_dynamic_test_case_layout = QVBoxLayout()
        # self.ex_right_content_one_ex_layout.setSizeConstraint(QLayout.SetNoConstraint)
        # 3. define a Groupbox
        self.test_case_details_groupbox = CustomGroupBox("Details")
        # self.ex_right_content_ex_details_groupbox.setChecked(False)
        self.test_case_action_collection_groupbox = CustomGroupBox("Action Collection")
        self.test_case_test_case_data_groupbox = CustomGroupBox("Test Case Data")
        # 4. add the page to the tabwidet
        self.test_case_tabwidget.addTab(self.one_dynamic_test_case_tab, name)
        self.test_case_tabwidget.setCurrentWidget(self.one_dynamic_test_case_tab)
        # 5.set layout to the page tab
        self.one_dynamic_test_case_tab.setLayout(self.one_dynamic_test_case_layout)
        # 6. add all groupbox into page tab layout
        self.one_dynamic_test_case_layout.addWidget(self.test_case_details_groupbox)
        self.one_dynamic_test_case_layout.addWidget(self.test_case_action_collection_groupbox)
        self.one_dynamic_test_case_layout.addWidget(self.test_case_test_case_data_groupbox)
        self.one_dynamic_test_case_layout.addStretch()
        self.test_case_details_gridlayout = QGridLayout()
        self.test_case_details_groupbox.setLayout(self.test_case_details_gridlayout)
        self.test_case_action_collection_gridlayout = QGridLayout()
        self.test_case_action_collection_groupbox.setLayout(self.test_case_action_collection_gridlayout)
        self.test_case_test_case_data_gridlayout = QGridLayout()
        self.test_case_test_case_data_groupbox.setLayout(self.test_case_test_case_data_gridlayout)

        # Details groupbox
        self.test_case_details_name_lable = QLabel("Name:")
        self.test_case_details_name_lineedit = QLineEdit()
        self.test_case_details_name_lineedit.setObjectName("name")
        self.test_case_details_description_lable = QLabel("Description:")
        self.test_case_details_description_lineedit = QTextEdit()
        self.test_case_details_description_lineedit.setObjectName("description")
        self.test_case_details_description_lineedit.setFixedHeight(52)
        self.test_case_details_tags_lable = QLabel("Tags:")
        self.test_case_details_tags_lineedit = QLineEdit()
        self.test_case_details_tags_lineedit.setObjectName("tags")
        self.test_case_details_status_lable = QLabel("Status:")
        self.test_case_details_status_lineedit = QLineEdit()
        self.test_case_details_status_lineedit.setObjectName("status")
        self.test_case_details_row_lineedit = QLineEdit()
        self.test_case_details_row_lineedit.setObjectName("row")
        self.test_case_details_row_lineedit.hide()
        self.test_case_details_gridlayout.addWidget(self.test_case_details_name_lable, 0, 0)
        self.test_case_details_gridlayout.addWidget(self.test_case_details_name_lineedit, 0, 1)
        self.test_case_details_gridlayout.addWidget(self.test_case_details_description_lable, 1, 0)
        self.test_case_details_gridlayout.addWidget(self.test_case_details_description_lineedit,1, 1)
        self.test_case_details_gridlayout.addWidget(self.test_case_details_tags_lable, 2, 0)
        self.test_case_details_gridlayout.addWidget(self.test_case_details_tags_lineedit, 2, 1)
        self.test_case_details_gridlayout.addWidget(self.test_case_details_status_lable, 3, 0)
        self.test_case_details_gridlayout.addWidget(self.test_case_details_status_lineedit,3, 1)
        self.test_case_details_gridlayout.addWidget(self.test_case_details_row_lineedit, 4, 0)
