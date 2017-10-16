from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtWidgets import QGridLayout, QToolBox, QLabel, QGroupBox, QTabBar, QPushButton, QVBoxLayout, \
    QLineEdit, QAction
from UserInterface.CustomGroupBox import CustomGroupBox


class MainWindow_UI(object):
    def setupUi(self, MainWindow):
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

    def setup_execution_main_tab(self):
        # define the QGridLayout execution_tab_layout into the execution_tab.
        self.ex_tab_layout = QGridLayout()
        self.ex_tab_layout.setContentsMargins(5, 5, 5, 5)
        self.execution_main_tab.setLayout(self.ex_tab_layout)

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
        self.ex_right_content_toolbar = QtWidgets.QToolBar()
        self.ex_right_content_toolbar.setObjectName("new_same_tb")
        new=QAction(QIcon("./images/add.png"),"new",self)
        self.ex_right_content_toolbar.addAction(new)
        save=QAction(QIcon("./images/save.png"),"save",self)
        #self.ex_right_content_toolbar.addSeparator()
        self.ex_right_content_toolbar.addAction(save)
        self.ex_right_content_toolbar.addSeparator()
        self.ex_right_content_toolbar.setAutoFillBackground(True)
        # 1.define a groupbox
        self.ex_right_content_groupbox = QGroupBox()
        self.ex_right_content_groupbox.setContentsMargins(0, 0, 0, 0)
        # 2.define a gridlayout
        self.ex_right_content_gridlayout = QGridLayout()
        self.ex_right_content_gridlayout.setContentsMargins(3, 2, 1, 3)
        # 3.define a tabwidget
        # first page of the tabwidget
        self.ex_right_content_allex_tab = QtWidgets.QWidget()
        self.ex_right_content_allex_tab.setObjectName("tab3")
        # define the tabwidget add the first page
        self.ex_right_content_tabwidget = QtWidgets.QTabWidget()
        self.ex_right_content_tabwidget.addTab(self.ex_right_content_allex_tab, "All Executions")
        self.ex_right_content_tabwidget.setAutoFillBackground(True)
        self.ex_right_content_tabwidget.setTabsClosable(True)
        self.ex_right_content_tabwidget.setMovable(True)
        # close the tab
        self.ex_right_content_tabwidget.tabCloseRequested.connect(self.ex_right_content_tabwidget.removeTab)
        # add the new/edit page for execution
        # self.setup_excution_tab()

        # set the index 0 page hasn't colse button
        QTabBar.setTabButton(self.ex_right_content_tabwidget.tabBar(), 0, QTabBar.RightSide, None)

        # add the ex_right_content_toolbar and  ex_right_content_tabwidget into gridlayout
        self.ex_right_content_gridlayout.addWidget(self.ex_right_content_toolbar, 0, 0)
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

        # add tableview into execution
        self.ex_right_ex_tableview = QtWidgets.QTableView()
        self.ex_right_ex_gridlayout = QGridLayout()
        self.ex_right_ex_gridlayout.setContentsMargins(0, 0, 0, 0)
        self.ex_right_content_allex_tab.setLayout(self.ex_right_ex_gridlayout)
        self.ex_right_ex_gridlayout.addWidget(self.ex_right_ex_tableview)

        # add tableview into execution
        self.ex_right_ts_tableview = QtWidgets.QTableView()
        self.ex_right_ts_gridlayout = QGridLayout()
        self.ex_right_ts_gridlayout.setContentsMargins(0, 0, 0, 0)
        self.ex_right_content_allts_tab.setLayout(self.ex_right_ts_gridlayout)
        self.ex_right_ts_gridlayout.addWidget(self.ex_right_ts_tableview)

    def setup_excution_tab(self, name=None):
        # 1. define a page
        self.ex_right_content_one_ex_tab = QtWidgets.QWidget()
        self.ex_right_content_one_ex_tab.setObjectName(name)
        # 2. define a layout
        self.ex_right_content_one_ex_layout = QVBoxLayout()
        # self.ex_right_content_one_ex_layout.setSizeConstraint(QLayout.SetNoConstraint)
        # 3. define a Groupbox
        self.ex_right_content_ex_details_groupbox = CustomGroupBox("Details")
        #self.ex_right_content_ex_details_groupbox.setChecked(False)
        self.ex_right_content_ex_email_groupbox = CustomGroupBox("Email Notification")
        self.ex_right_content_ex_settings_groupbox = CustomGroupBox("Settings")
        self.ex_right_content_ex_Variables_groupbox = CustomGroupBox("Set Variables")
        self.ex_right_content_ex_Testcases_groupbox = CustomGroupBox("Test Cases")
        # 4. add the page to the tabwidet
        self.ex_right_content_tabwidget.addTab(self.ex_right_content_one_ex_tab, name)
        self.ex_right_content_tabwidget.setCurrentWidget(self.ex_right_content_one_ex_tab)
        # 5.set layout to the page tab
        self.ex_right_content_one_ex_tab.setLayout(self.ex_right_content_one_ex_layout)
        # 6. add all groupbox into page tab layout
        self.ex_right_content_one_ex_layout.addWidget(self.ex_right_content_ex_details_groupbox)
        self.ex_right_content_one_ex_layout.addWidget(self.ex_right_content_ex_email_groupbox)
        self.ex_right_content_one_ex_layout.addWidget(self.ex_right_content_ex_settings_groupbox)
        self.ex_right_content_one_ex_layout.addWidget(self.ex_right_content_ex_Variables_groupbox)
        self.ex_right_content_one_ex_layout.addWidget(self.ex_right_content_ex_Testcases_groupbox)
        self.ex_right_content_one_ex_layout.addStretch()
        self.g1 = QGridLayout()
        self.ex_right_content_ex_details_groupbox.setLayout(self.g1)
        self.g2 = QGridLayout()
        self.ex_right_content_ex_email_groupbox.setLayout(self.g2)
        self.g3 = QGridLayout()
        self.ex_right_content_ex_settings_groupbox.setLayout(self.g3)
        self.g4 = QGridLayout()
        self.ex_right_content_ex_Variables_groupbox.setLayout(self.g4)
        self.g5 = QGridLayout()
        self.ex_right_content_ex_Testcases_groupbox.setLayout(self.g5)

        # Details groupbox
        self.ex_right_content_ex_details_name_lable = QLabel("Name:")
        self.ex_right_content_ex_details_name_lineedit = QLineEdit()
        self.ex_right_content_ex_details_name_lineedit.setObjectName("name")
        self.ex_right_content_ex_details_tags_lable = QLabel("Tags:")
        self.ex_right_content_ex_details_tags_lineedit = QLineEdit()
        self.ex_right_content_ex_details_tags_lineedit.setObjectName("tags")
        self.ex_right_content_ex_details_ts_lable = QLabel("Test Set:")
        self.ex_right_content_ex_details_ts_lineedit = QLineEdit()
        self.ex_right_content_ex_details_ts_lineedit.setObjectName("testset")
        self.ex_right_content_ex_details_state_lable = QLabel("State:")
        self.ex_right_content_ex_details_state_lineedit = QLineEdit()
        self.ex_right_content_ex_details_state_lineedit.setObjectName("state")
        self.ex_right_content_ex_details_row_lineedit=QLineEdit()
        self.ex_right_content_ex_details_row_lineedit.setObjectName("row")
        self.ex_right_content_ex_details_row_lineedit.hide()
        self.g1.addWidget(self.ex_right_content_ex_details_name_lable, 0, 0)
        self.g1.addWidget(self.ex_right_content_ex_details_name_lineedit, 0, 1)
        self.g1.addWidget(self.ex_right_content_ex_details_tags_lable, 1, 0)
        self.g1.addWidget(self.ex_right_content_ex_details_tags_lineedit, 1, 1)
        self.g1.addWidget(self.ex_right_content_ex_details_ts_lable, 2, 0)
        self.g1.addWidget(self.ex_right_content_ex_details_ts_lineedit, 2, 1)
        self.g1.addWidget(self.ex_right_content_ex_details_state_lable, 3, 0)
        self.g1.addWidget(self.ex_right_content_ex_details_state_lineedit, 3, 1)
        self.g1.addWidget(self.ex_right_content_ex_details_row_lineedit, 4, 0)

    # define a QWidget and add View button, Delete button in it
    def setup_ex_right_ex_actions_column(self):
        self.ex_right_ex_widget = QtWidgets.QWidget()
        self.ex_right_ex_widget.setContentsMargins(0, 0, 0, 0)
        self.ex_right_ex_gridlayout = QGridLayout()
        self.ex_right_ex_gridlayout.setContentsMargins(3, 3, 3, 3)
        self.ex_right_ex_widget.setLayout(self.ex_right_ex_gridlayout)
        self.ex_right_ex_edit_button = QPushButton()
        self.ex_right_ex_edit_button.setObjectName("edit")
        self.ex_right_ex_edit_button.setIcon(QIcon("./images/edit.png"))
        self.ex_right_ex_edit_button.setFlat(True)
        self.ex_right_ex_edit_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.ex_right_ex_edit_button.setToolTip("Edit")
        self.ex_right_ex_delete_button = QPushButton()
        self.ex_right_ex_delete_button.setObjectName("delete")
        self.ex_right_ex_delete_button.setIcon(QIcon("./images/delete.png"))
        self.ex_right_ex_delete_button.setFlat(True)
        self.ex_right_ex_delete_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.ex_right_ex_delete_button.setToolTip("Delete")
        self.ex_right_ex_gridlayout.addWidget(self.ex_right_ex_edit_button, 0, 0)
        self.ex_right_ex_gridlayout.addWidget(self.ex_right_ex_delete_button, 0, 1)

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
