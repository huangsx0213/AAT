from PyQt5 import QtWidgets, QtSql
from PyQt5.QtCore import Qt

from UserInterface.MainWindow_UI import MainWindow_UI
from PyQt5.QtGui import QStandardItem, QIcon, QStandardItemModel
from PyQt5.QtSql import QSqlRelationalTableModel, QSqlTableModel, QSqlRelation, QSqlRelationalDelegate
from PyQt5.QtWidgets import QLineEdit, QTabBar, QAction

class MainWindow(QtWidgets.QTabWidget, MainWindow_UI):
    def __init__(self):
        super().__init__()
        self.setupUi()
        self.excution_tab_dic={}
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('.\study\qaat.db')
        db.open()


        # List view data and action
        self.ex_list_view_model = QStandardItemModel()
        # Load the data to the model
        self.ex_list_view_model = self.ex_leftmenu_listview_loadModelData(self.ex_list_view_model)
        # SConnect the model to the listView
        self.ex_left_menu_listview.setModel(self.ex_list_view_model)
        self.ex_left_menu_listview.clicked.connect(self.ex_left_listview_on_clicked)
        # execution table logic
        self.ex_right_ex_tableview_model = QSqlRelationalTableModel()
        self.ex_right_ex_tableview_model.setTable("Execution")
        self.ex_right_ex_tableview_model.setEditStrategy(QSqlTableModel.OnRowChange)
        self.ex_right_ex_tableview_model.setRelation(3, QSqlRelation("TestSet", "Id", "Name"))
        self.ex_right_ex_tableview_model.setHeaderData(3, Qt.Horizontal, "TestSet")
        self.ex_right_ex_tableview_model.select()
        self.ex_right_ex_tableview.setModel(self.ex_right_ex_tableview_model)
        self.ex_right_ex_tableview.setItemDelegate(QSqlRelationalDelegate(self.ex_right_ex_tableview))
        self.ex_right_ex_tableview.verticalHeader().setVisible(False)
        # self.ex_right_ex_tableview_model.insertRow(4)
        # self.add_execution()
        # add the actions column into the tableview
        self.ex_right_ex_tableview_add_actions_column()
        # testset table logic
        self.ex_right_ts_tableview_model = QSqlTableModel()
        self.ex_right_ts_tableview_model.setTable("TestSet")
        self.ex_right_ts_tableview_model.setEditStrategy(QSqlTableModel.OnRowChange)
        self.ex_right_ts_tableview_model.select()
        self.ex_right_ts_tableview.setModel(self.ex_right_ts_tableview_model)
        self.ex_right_ts_tableview.verticalHeader().setVisible(False)
        self.current_listdata = QStandardItem(QIcon("./images/execution.png"), "Executions")
        self.ex_right_content_toolbar.actionTriggered[QAction].connect(self.tool_btn_clicked)

    def ex_right_ex_tableview_add_actions_column(self):
        # add a column into the ex table for actions
        self.ex_right_ex_tableview_model.select()
        tem_column_count = self.ex_right_ex_tableview_model.columnCount()
        self.ex_right_ex_tableview_model.insertColumn(tem_column_count)
        self.ex_right_ex_tableview_model.setHeaderData(tem_column_count, Qt.Horizontal, "Actions")

        for row in range(self.ex_right_ex_tableview_model.rowCount()):
            self.setup_execution_actions_column()
            self.ex_right_ex_edit_button.clicked.connect(self.add_execution_tab_ui)
            self.ex_right_ex_delete_button.clicked.connect(self.delete_execution_record)
            self.ex_right_ex_index = self.ex_right_ex_tableview.model().index(row, tem_column_count)
            self.ex_right_ex_tableview.setIndexWidget(self.ex_right_ex_index, self.ex_right_ex_widget)

    def add_execution_tab_ui(self):
        # get the selected  QPushButton's parent : the QWidget
        ex_right_ex_widget_selected = self.sender().parent()
        # print(self.sender().objectName())
        if self.sender().objectName() == "edit" or self.sender().objectName() == "delete":
            # get the index of the QWidget in the tableview and it's row
            ex_right_ex_widget_index = self.ex_right_ex_tableview.indexAt(ex_right_ex_widget_selected.pos())
            self.ex_right_ex_widget_row = ex_right_ex_widget_index.row()
            # print(ex_right_ex_widget_row)
            # remove the row from the model
            data_row = self.ex_right_ex_tableview_model.record(self.ex_right_ex_widget_row)
            row = self.ex_right_ex_widget_row
            name = data_row.value("Name")
            tags = data_row.value("Tags")
            test_set = data_row.value("TestSet_Name_2")
            state = data_row.value("State")
        else:
            row = -1
            name = ""
            tags = ""
            test_set = ""
            state = ""
        # create new tab,but if exist , do not create the new tab
        create = True
        if self.ex_right_content_tabwidget.count() > 1:
            count = self.ex_right_content_tabwidget.count()
            for i in range(count):
                if self.ex_right_content_tabwidget.tabText(i) == name:
                    create = False
                    break
        if create == True:
            # self.ex_right_content_tabwidget.removeTab(1)
            if row != -1:
                self.setup_dynamic_excution_tab(name)
            else:
                self.setup_dynamic_excution_tab("New Execution")
            # self.excution_tab_dic[self.ex_right_ex_widget_row ]=self.ex_right_content_one_ex_tab
            # l=self.excution_tab_dic[self.ex_right_ex_widget_row ].findChild(QLineEdit,name="lname",options=Qt.FindChildrenRecursively)
            # print(l.objectName())
            self.ex_right_content_ex_details_name_lineedit.setText(name)
            self.ex_right_content_ex_details_tags_lineedit.setText(tags)
            self.ex_right_content_ex_details_ts_lineedit.setText(test_set)
            self.ex_right_content_ex_details_state_lineedit.setText(state)
            self.ex_right_content_ex_details_row_lineedit.setText(str(row))
            # print(data_row.value("TestSet_Name_2"))
        # regenerate the actions_column
        self.ex_right_ex_tableview_add_actions_column()

    def delete_execution_record(self):
        # get the selected  QPushButton's parent : the QWidget
        ex_right_ex_widget_selected = self.sender().parent()
        # print(type(ex_right_ex_widget_selected))
        # get the index of the QWidget in the tableview and it's row
        ex_right_ex_widget_index = self.ex_right_ex_tableview.indexAt(ex_right_ex_widget_selected.pos())
        ex_right_ex_widget_row = ex_right_ex_widget_index.row()
        # print(ex_right_ex_widget_row)
        # remove the row from the model
        self.ex_right_ex_tableview_model.removeRow(ex_right_ex_widget_row)
        # regenerate the actions_column
        self.ex_right_ex_tableview_add_actions_column()

    def save_execution_record(self):
        row_edit = self.ex_right_content_tabwidget.currentWidget().findChild(QLineEdit, name="row",
                                                                             options=Qt.FindChildrenRecursively)
        if row_edit is not None:
            row = int(row_edit.text())
            name = self.ex_right_content_tabwidget.currentWidget().findChild(QLineEdit, name="name",
                                                                             options=Qt.FindChildrenRecursively).text()
            tags = self.ex_right_content_tabwidget.currentWidget().findChild(QLineEdit, name="tags",
                                                                             options=Qt.FindChildrenRecursively).text()
            testset = self.ex_right_content_tabwidget.currentWidget().findChild(QLineEdit, name="testset",
                                                                                options=Qt.FindChildrenRecursively).text()
            state = self.ex_right_content_tabwidget.currentWidget().findChild(QLineEdit, name="state",
                                                                              options=Qt.FindChildrenRecursively).text()
            if row != -1:
                record = self.ex_right_ex_tableview_model.record(row)
                print("editing row: " + str(row))
                record.setValue("Name", name)
                record.setValue("Tags", tags)
                record.setValue("TestSet_Name_2", testset)
                record.setValue("State", state)
                self.ex_right_ex_tableview_model.setRecord(row, record)
                self.ex_right_ex_tableview_add_actions_column()
            else:
                record = self.ex_right_ex_tableview_model.record()
                print("editing row: " + str(row))
                record.setValue("Name", name)
                record.setValue("Tags", tags)
                record.setValue("TestSet_Name_2", testset)
                record.setValue("State", state)
                self.ex_right_ex_tableview_model.insertRecord(0, record)
                self.ex_right_content_tabwidget.removeTab(self.ex_right_content_tabwidget.currentIndex())
                self.ex_right_ex_tableview_add_actions_column()
        else:
            print("No need saving.")

    def tool_btn_clicked(self, action):
        if action.text() == "save":
            if self.current_listdata.text() == "Executions":
                self.save_execution_record()
        elif action.text() == "new":
            if self.current_listdata.text() == "Executions":
                self.add_execution_tab_ui()

    def add_execution_record(self):
        record = self.ex_right_ex_tableview_model.record()
        record.setValue("Name", "ex1")
        record.setValue("Tags", "tag")
        record.setValue("TestSet_Name_2", 3)
        record.setValue("State", "notready")
        self.ex_right_ex_tableview_model.insertRecord(0, record)
        self.ex_right_ex_tableview_model.select()

    def ex_leftmenu_listview_loadModelData(self, model):
        # Demo data
        # now a simple list, later database with index field
        self.listdata = [QStandardItem(QIcon("./images/execution.png"), "Executions"),
                         QStandardItem(QIcon("./images/testset.png"), "Test Sets"),
                         QStandardItem(QIcon("./images/variables.png"), 'Variables'),
                         QStandardItem(QIcon("./images/mac.png"), 'Machines')]
        for row in self.listdata:
            item = QStandardItem(row)
            # Set item AlignCenter
            # item.setTextAlignment(QtCore.Qt.AlignCenter)
            model.appendRow(item)
        return model

    def ex_left_listview_on_clicked(self, index):
        current_row = index.row()
        self.current_listdata = self.listdata[current_row]
        print("You are selecting left menu " + str(self.current_listdata.text()))
        count = self.ex_right_content_tabwidget.count()
        for i in range(count, 0, -1):
            self.ex_right_content_tabwidget.removeTab(i - 1)
        if self.current_listdata.text() == "Executions":
            self.ex_right_content_tabwidget.addTab(self.ex_right_content_allex_tab, "All Executions")
        elif self.current_listdata.text() == "Test Sets":
            self.ex_right_content_tabwidget.addTab(self.ex_right_content_allts_tab, "All Test Sets")
        elif self.current_listdata.text() == "Variables":
            self.ex_right_content_tabwidget.addTab(self.ex_right_content_allva_tab, "Variables")
        elif self.current_listdata.text() == "Machines":
            self.ex_right_content_tabwidget.addTab(self.ex_right_content_allma_tab, "Machines")
        QTabBar.setTabButton(self.ex_right_content_tabwidget.tabBar(), 0, QTabBar.RightSide, None)




