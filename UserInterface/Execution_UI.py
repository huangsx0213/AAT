from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtWidgets import QGridLayout, QGroupBox, QToolBox, QAction, QTabBar, QVBoxLayout, QLabel, QLineEdit, \
    QPushButton, QSplitter, QTreeView

from UserInterface.CustomGroupBox import CustomGroupBox


class Execution_UI(object):
    def setup_execution_ui(self):
        # define the first tab and add it into the QTabWidget.
        self.execution_main_tab = QtWidgets.QWidget()
        self.execution_main_tab.setObjectName("execution_main_tab")
        self.addTab(self.execution_main_tab, "Execution")

        self.setup_execution_main_tab()

    def setup_execution_main_tab(self):
        # define the QGridLayout execution_tab_layout into the execution_tab.
        self.execution_main_tab_layout = QGridLayout()
        self.execution_main_tab_layout.setContentsMargins(5, 5, 5, 5)
        self.execution_main_tab.setLayout(self.execution_main_tab_layout)

        # define the left groupbox
        # 1. define a groupbox
        self.execution_menu_groupbox = QGroupBox()
        self.execution_menu_groupbox.setFixedWidth(185)
        # 2.define a gridlayout
        self.execution_menu_gridlayout = QGridLayout()
        self.execution_menu_gridlayout.setContentsMargins(2, 2, 2, 2)
        # 3.define a toolbox
        self.execution_menu_listview = QtWidgets.QListView()
        self.execution_menu_toolbox = QToolBox()
        self.execution_menu_toolbox.addItem(self.execution_menu_listview, "Execution")
        # add the toolbox into gridlayout
        self.execution_menu_gridlayout.addWidget(self.execution_menu_toolbox)
        # add the gridlaout into the groupbox
        self.execution_menu_groupbox.setLayout(self.execution_menu_gridlayout)

        # define the right groupbox
        # 0.define the save toolbar
        self.execution_main_tab_toolbar = QtWidgets.QToolBar()
        self.execution_main_tab_toolbar.setObjectName("new_same_tb")
        new = QAction(QIcon("./images/add.png"), "new", self)
        self.execution_main_tab_toolbar.addAction(new)
        save = QAction(QIcon("./images/save.png"), "save", self)
        # self.ex_right_content_toolbar.addSeparator()
        self.execution_main_tab_toolbar.addAction(save)
        self.execution_main_tab_toolbar.addSeparator()
        self.execution_main_tab_toolbar.setAutoFillBackground(True)
        # 1.define a groupbox
        self.execution_groupbox = QGroupBox()
        self.execution_groupbox.setContentsMargins(0, 0, 0, 0)
        # 2.define a gridlayout
        self.execution_gridlayout = QGridLayout()
        self.execution_gridlayout.setContentsMargins(3, 2, 1, 3)
        # 3.define a tabwidget
        # first page of the tabwidget
        self.all_executions_tab = QtWidgets.QWidget()
        self.all_executions_tab.setObjectName("all_executions_tab")
        # define the tabwidget add the first page
        self.execution_tabwidget = QtWidgets.QTabWidget()
        self.execution_tabwidget.addTab(self.all_executions_tab, "All Executions")
        self.execution_tabwidget.setAutoFillBackground(True)
        self.execution_tabwidget.setTabsClosable(True)
        self.execution_tabwidget.setMovable(True)
        # close the tab
        self.execution_tabwidget.tabCloseRequested.connect(self.execution_tabwidget.removeTab)
        # add the new/edit page for execution
        # self.setup_excution_tab()

        # set the index 0 page hasn't colse button
        QTabBar.setTabButton(self.execution_tabwidget.tabBar(), 0, QTabBar.RightSide, None)

        # add the ex_right_content_toolbar and  ex_right_content_tabwidget into gridlayout
        self.execution_gridlayout.addWidget(self.execution_main_tab_toolbar, 0, 0)
        self.execution_gridlayout.addWidget(self.execution_tabwidget, 1, 0)
        # add the gridlaout into the groupbox
        self.execution_groupbox.setLayout(self.execution_gridlayout)

        # add the left groupbox and  right groupbox into execution_tab_layout
        self.execution_main_tab_layout.addWidget(self.execution_menu_groupbox, 0, 0)
        self.execution_main_tab_layout.addWidget(self.execution_groupbox, 0, 1)

        # add first page for each listdata
        self.all_testset_tab = QtWidgets.QWidget()
        self.all_testset_tab.setObjectName("all_testset_tab")

        self.all_varialbes_tab = QtWidgets.QWidget()
        self.all_varialbes_tab.setObjectName("all_varialbes_tab")

        self.all_machine_tab = QtWidgets.QWidget()
        self.all_machine_tab.setObjectName("all_machine_tab")

        # add tableview into execution
        self.execution_tableview = QtWidgets.QTableView()
        self.execution_gridlayout = QGridLayout()
        self.execution_gridlayout.setContentsMargins(0, 0, 0, 0)
        self.all_executions_tab.setLayout(self.execution_gridlayout)
        self.execution_gridlayout.addWidget(self.execution_tableview)

        # add tableview into execution
        self.testset_tableview = QtWidgets.QTableView()
        self.testset_tableview.setBaseSize(303,500)
        self.testset_testcase_tableview = QtWidgets.QTableView()
        self.testset_gridlayout = QGridLayout()
        self.testset_gridlayout.setContentsMargins(0, 0, 0, 0)
        self.all_testset_tab.setLayout(self.testset_gridlayout)
        self.all_testset_splitter=QSplitter(Qt.Horizontal)
        self.testset_gridlayout.addWidget(self.all_testset_splitter)
        self.all_testset_splitter.addWidget(self.testset_tableview)
        self.all_testset_splitter.addWidget(self.testset_testcase_tableview)
        self.all_testset_splitter.setStretchFactor(0,60)
        self.all_testset_splitter.setStretchFactor(1,40)

    def setup_dynamic_excution_tab(self, name=None):
        # 1. define a page
        self.one_dynamic_execution_tab = QtWidgets.QWidget()
        self.one_dynamic_execution_tab.setObjectName(name)
        # 2. define a layout
        self.one_dynamic_execution_layout = QVBoxLayout()
        # self.ex_right_content_one_ex_layout.setSizeConstraint(QLayout.SetNoConstraint)
        # 3. define a Groupbox
        self.execution_details_groupbox = CustomGroupBox("Details")
        # self.ex_right_content_ex_details_groupbox.setChecked(False)
        self.execution_email_groupbox = CustomGroupBox("Email Notification")
        self.execution_settings_groupbox = CustomGroupBox("Settings")
        self.execution_Variables_groupbox = CustomGroupBox("Set Variables")
        self.execution_Testcases_groupbox = CustomGroupBox("Test Cases")
        # 4. add the page to the tabwidet
        self.execution_tabwidget.addTab(self.one_dynamic_execution_tab, name)
        self.execution_tabwidget.setCurrentWidget(self.one_dynamic_execution_tab)
        # 5.set layout to the page tab
        self.one_dynamic_execution_tab.setLayout(self.one_dynamic_execution_layout)
        # 6. add all groupbox into page tab layout
        self.one_dynamic_execution_layout.addWidget(self.execution_details_groupbox)
        self.one_dynamic_execution_layout.addWidget(self.execution_email_groupbox)
        self.one_dynamic_execution_layout.addWidget(self.execution_settings_groupbox)
        self.one_dynamic_execution_layout.addWidget(self.execution_Variables_groupbox)
        self.one_dynamic_execution_layout.addWidget(self.execution_Testcases_groupbox)
        self.one_dynamic_execution_layout.addStretch()
        self.execution_details_gridlayout = QGridLayout()
        self.execution_details_groupbox.setLayout(self.execution_details_gridlayout)
        self.g2 = QGridLayout()
        self.execution_email_groupbox.setLayout(self.g2)
        self.g3 = QGridLayout()
        self.execution_settings_groupbox.setLayout(self.g3)
        self.g4 = QGridLayout()
        self.execution_Variables_groupbox.setLayout(self.g4)
        self.g5 = QGridLayout()
        self.execution_Testcases_groupbox.setLayout(self.g5)

        # Details groupbox
        self.execution_details_name_lable = QLabel("Name:")
        self.execution_details_name_lineedit = QLineEdit()
        self.execution_details_name_lineedit.setObjectName("name")
        self.execution_details_tags_lable = QLabel("Tags:")
        self.execution_details_tags_lineedit = QLineEdit()
        self.execution_details_tags_lineedit.setObjectName("tags")
        self.execution_details_testset_lable = QLabel("Test Set:")
        self.execution_details_testset_lineedit = QLineEdit()
        self.execution_details_testset_lineedit.setObjectName("testset")
        self.execution_details_state_lable = QLabel("State:")
        self.execution_details_state_lineedit = QLineEdit()
        self.execution_details_state_lineedit.setObjectName("state")
        self.execution_details_row_lineedit = QLineEdit()
        self.execution_details_row_lineedit.setObjectName("row")
        self.execution_details_row_lineedit.hide()
        self.execution_details_gridlayout.addWidget(self.execution_details_name_lable, 0, 0)
        self.execution_details_gridlayout.addWidget(self.execution_details_name_lineedit, 0, 1)
        self.execution_details_gridlayout.addWidget(self.execution_details_tags_lable, 1, 0)
        self.execution_details_gridlayout.addWidget(self.execution_details_tags_lineedit, 1, 1)
        self.execution_details_gridlayout.addWidget(self.execution_details_testset_lable, 2, 0)
        self.execution_details_gridlayout.addWidget(self.execution_details_testset_lineedit, 2, 1)
        self.execution_details_gridlayout.addWidget(self.execution_details_state_lable, 3, 0)
        self.execution_details_gridlayout.addWidget(self.execution_details_state_lineedit, 3, 1)
        self.execution_details_gridlayout.addWidget(self.execution_details_row_lineedit, 4, 0)

    def setup_dynamic_testset_tab(self, name=None):
        # 1. define a page
        self.one_dynamic_testset_tab = QtWidgets.QWidget()
        self.one_dynamic_testset_tab.setObjectName(name)
        # 2. define a layout
        self.one_dynamic_testset_layout = QVBoxLayout()
        # self.ex_right_content_one_ex_layout.setSizeConstraint(QLayout.SetNoConstraint)
        # 3. define a Groupbox
        self.testset_details_groupbox = CustomGroupBox("Details")
        # self.ex_right_content_ex_details_groupbox.setChecked(False)
        # 4. add the page to the tabwidet
        self.execution_tabwidget.addTab(self.one_dynamic_testset_tab, name)
        self.execution_tabwidget.setCurrentWidget(self.one_dynamic_testset_tab)
        # 5.set layout to the page tab
        self.one_dynamic_testset_tab.setLayout(self.one_dynamic_testset_layout)
        # 6. add all groupbox into page tab layout
        self.one_dynamic_testset_layout.addWidget(self.testset_details_groupbox)
        self.one_dynamic_testset_layout.addStretch()
        self.testset_details_gridlayout = QGridLayout()
        self.testset_details_groupbox.setLayout(self.testset_details_gridlayout)

        # Details groupbox
        self.testset_details_name_lable = QLabel("Name:")
        self.testset_details_name_lineedit = QLineEdit()
        self.testset_details_name_lineedit.setObjectName("testset_name")

        self.testset_details_testcases_lable = QLabel("TestCases:")
        self.testset_details_testcases_treeview=QTreeView()


        self.testset_details_row_lineedit = QLineEdit()
        self.testset_details_row_lineedit.setObjectName("row")
        self.testset_details_row_lineedit.hide()
        self.testset_details_gridlayout.addWidget(self.testset_details_name_lable, 0, 0)
        self.testset_details_gridlayout.addWidget(self.testset_details_name_lineedit, 0, 1)
        self.testset_details_gridlayout.addWidget(self.testset_details_row_lineedit, 1, 0)
        if name != "New Test Set":
            self.testset_details_gridlayout.addWidget(self.testset_details_testcases_lable, 1, 0)
            self.testset_details_gridlayout.addWidget(self.testset_details_testcases_treeview, 1, 1)
        
    def setup_execution_actions_column(self):
        self.execution_action_widget = QtWidgets.QWidget()
        self.execution_action_widget.setContentsMargins(0, 0, 0, 0)
        self.execution_gridlayout = QGridLayout()
        self.execution_gridlayout.setContentsMargins(3, 3, 3, 3)
        self.execution_action_widget.setLayout(self.execution_gridlayout)
        self.execution_edit_button = QPushButton()
        self.execution_edit_button.setObjectName("edit")
        self.execution_edit_button.setIcon(QIcon("./images/edit.png"))
        self.execution_edit_button.setFlat(True)
        self.execution_edit_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.execution_edit_button.setToolTip("Edit")
        self.execution_delete_button = QPushButton()
        self.execution_delete_button.setObjectName("delete")
        self.execution_delete_button.setIcon(QIcon("./images/delete.png"))
        self.execution_delete_button.setFlat(True)
        self.execution_delete_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.execution_delete_button.setToolTip("Delete")
        self.execution_gridlayout.addWidget(self.execution_edit_button, 0, 0)
        self.execution_gridlayout.addWidget(self.execution_delete_button, 0, 1)
        
    def setup_testset_actions_column(self):
        self.testset_action_widget = QtWidgets.QWidget()
        self.testset_action_widget.setContentsMargins(0, 0, 0, 0)
        self.testset_action_gridlayout = QGridLayout()
        self.testset_action_gridlayout.setContentsMargins(3, 3, 3, 3)
        self.testset_action_widget.setLayout(self.testset_action_gridlayout)
        self.testset_edit_button = QPushButton()
        self.testset_edit_button.setObjectName("testset_edit")
        self.testset_edit_button.setIcon(QIcon("./images/edit.png"))
        self.testset_edit_button.setFlat(True)
        self.testset_edit_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.testset_edit_button.setToolTip("Edit")
        self.testset_delete_button = QPushButton()
        self.testset_delete_button.setObjectName("testset_edit")
        self.testset_delete_button.setIcon(QIcon("./images/delete.png"))
        self.testset_delete_button.setFlat(True)
        self.testset_delete_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.testset_delete_button.setToolTip("Delete")
        self.testset_action_gridlayout.addWidget(self.testset_edit_button, 0, 0)
        self.testset_action_gridlayout.addWidget(self.testset_delete_button, 0, 1)
