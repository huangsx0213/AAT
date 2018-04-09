from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon
from PyQt5.QtSql import QSqlQueryModel, QSqlTableModel
from PyQt5.QtWidgets import QAction, QTabBar

from UserInterface.MainWindowUI import MainWindowUI


class TestcaseMenuLogic(MainWindowUI):

    def testcase_menu_logic(self):

        # List view data and action
        self.testcase_menu_model = QSqlQueryModel()
        self.testcase_menu_model.setQuery("select * from testcase")
        #print("The row count is :"+str(self.testcase_menu_model.rowCount()))
        self.testcase_menu_model2 = QStandardItemModel()
        self.testcase_menu_model2 = self.load_test_case_menu_model(self.testcase_menu_model2)
        # SConnect the model to the listView
        self.testcase_menu_listview.setModel(self.testcase_menu_model2)
        #self.testcase_menu_listview.clicked.connect(self.execution_menu_item_clicked)


        self.testcase_right_content_toolbar.actionTriggered[QAction].connect(self.testcase_main_tab_toolbar_clicked)

    def load_test_case_menu_model(self, model):

        for i in range(0,self.testcase_menu_model.rowCount()):
            item = QStandardItem(QIcon("./images/item.png"), str(self.testcase_menu_model.record(i).value(1)))
            model.appendRow(item)
        return model

    def testcase_menu_item_clicked(self, index):
        current_row = index.row()
        self.current_listdata = self.listdata[current_row]
        print("You are selecting left menu " + str(self.current_listdata.text()))
        count = self.execution_tabwidget.count()
        for i in range(count, 0, -1):
            self.execution_tabwidget.removeTab(i - 1)
        if self.current_listdata.text() == "Executions":
            self.execution_tabwidget.addTab(self.all_executions_tab, "All Executions")
        elif self.current_listdata.text() == "Test Sets":
            self.execution_tabwidget.addTab(self.all_testset_tab, "All Test Sets")
        elif self.current_listdata.text() == "Variables":
            self.execution_tabwidget.addTab(self.all_varialbes_tab, "Variables")
        elif self.current_listdata.text() == "Machines":
            self.execution_tabwidget.addTab(self.all_machine_tab, "Machines")
        QTabBar.setTabButton(self.execution_tabwidget.tabBar(), 0, QTabBar.RightSide, None)

    def testcase_main_tab_toolbar_clicked(self, action):
        if action.text() == "save":
            if self.current_listdata.text() == "Executions":
                self.save_execution_record()
            if self.current_listdata.text() == "Test Sets":
                self.save_testset_record()
        elif action.text() == "new":
            if self.current_listdata.text() == "Executions":
                self.add_dynamic_excution_tab()
            if self.current_listdata.text()=="Test Sets1":
                self.add_dynamic_testset_tab()