from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon
from PyQt5.QtWidgets import QAction, QTabBar

from UserInterface.MainWindowUI import MainWindowUI


class ExecutionMenuLogic(MainWindowUI):

    def execution_menu_logic(self):

        # List view data and action
        self.execution_menu_model = QStandardItemModel()
        # Load the data to the model
        self.execution_menu_model = self.load_execution_menu_model(self.execution_menu_model)
        # SConnect the model to the listView
        self.execution_menu_listview.setModel(self.execution_menu_model)
        self.execution_menu_listview.clicked.connect(self.execution_menu_item_clicked)
        self.current_listdata = QStandardItem(QIcon("./images/execution.png"), "Executions")

        self.execution_right_content_toolbar.actionTriggered[QAction].connect(self.execution_main_tab_toolbar_clicked)

    def load_execution_menu_model(self, model):
        # Demo data
        # now a simple list, later database with index field
        self.listdata = [QStandardItem(QIcon("./images/execution.png"), "Executions"),
                         QStandardItem(QIcon("./images/testset.png"), "Test Sets"),
                         QStandardItem(QIcon("./images/variables.png"), 'Variables'),
                         QStandardItem(QIcon("./images/mac.png"), 'Machines')]
        for data in self.listdata:
            item = data
            # Set item AlignCenter
            # item.setTextAlignment(QtCore.Qt.AlignCenter)
            model.appendRow(item)
        return model

    def execution_menu_item_clicked(self, index):
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

    def execution_main_tab_toolbar_clicked(self, action):
        if action.text() == "save":
            if self.current_listdata.text() == "Executions":
                self.save_execution_record()
            if self.current_listdata.text() == "Test Sets":
                self.save_testset_record()
        elif action.text() == "new":
            if self.current_listdata.text() == "Executions":
                self.add_dynamic_execution_tab()
            if self.current_listdata.text()=="Test Sets":
                self.add_dynamic_testset_tab()