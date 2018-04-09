from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon
from PyQt5.QtSql import QSqlRelationalTableModel, QSqlTableModel, QSqlRelation, QSqlRelationalDelegate
from PyQt5.QtWidgets import QLineEdit, QTabBar, QAction, QHeaderView

from UserInterface.MainWindowUI import MainWindowUI

class ExecutionLogic(MainWindowUI):
    def execution_logic(self):

        # execution table logic
        self.execution_tableview_model = QSqlRelationalTableModel()
        self.execution_tableview_model.setTable("Execution")
        self.execution_tableview_model.setEditStrategy(QSqlTableModel.OnRowChange)
        self.execution_tableview_model.setRelation(3, QSqlRelation("TestSet", "Id", "Name"))
        self.execution_tableview_model.setHeaderData(3, Qt.Horizontal, "TestSet")
        self.execution_tableview_model.setRelation(4, QSqlRelation("ExecutionStatus", "Id", "Name"))
        self.execution_tableview_model.setHeaderData(4, Qt.Horizontal, "Status")
        self.execution_tableview_model.select()
        self.execution_tableview.setModel(self.execution_tableview_model)
        self.execution_tableview.setItemDelegate(QSqlRelationalDelegate(self.execution_tableview))
        self.execution_tableview.verticalHeader().setVisible(False)
        self.execution_tableview.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.execution_tableview.horizontalHeader().setStyleSheet("::section{Background-color:rgb(220,220,220)}")
        #self.execution_tableview.resizeColumnsToContents()
        # self.ex_right_ex_tableview_model.insertRow(4)
        # self.add_execution()
        # add the actions column into the tableview
        self.execution_tableview_add_actions_column()

    def execution_tableview_add_actions_column(self):
        # add a column into the ex table for actions
        self.execution_tableview_model.select()
        tem_column_count = self.execution_tableview_model.columnCount()
        self.execution_tableview_model.insertColumn(tem_column_count)
        self.execution_tableview_model.setHeaderData(tem_column_count, Qt.Horizontal, "Actions")

        for row in range(self.execution_tableview_model.rowCount()):
            self.setup_execution_actions_column()
            self.execution_edit_button.clicked.connect(self.add_dynamic_excution_tab)
            self.execution_delete_button.clicked.connect(self.delete_execution_record)
            self.execution_index = self.execution_tableview.model().index(row, tem_column_count)
            self.execution_tableview.setIndexWidget(self.execution_index, self.execution_action_widget)

    def add_dynamic_excution_tab(self):
        # get the selected  QPushButton's parent : the QWidget
        execution_action_widget_selected = self.sender().parent()
        # print(self.sender().objectName())
        if self.sender().objectName() == "edit" or self.sender().objectName() == "delete":
            # get the index of the QWidget in the tableview and it's row
            execution_action_widget_index = self.execution_tableview.indexAt(execution_action_widget_selected.pos())
            self.execution_action_widget_row = execution_action_widget_index.row()
            # print(ex_right_ex_widget_row)
            # remove the row from the model
            data_row = self.execution_tableview_model.record(self.execution_action_widget_row)
            row = self.execution_action_widget_row
            name = data_row.value("Name")
            tags = data_row.value("Tags")
            test_set = data_row.value("TestSet_Name_3")
            state = data_row.value("ExecutionStatus_Name_2")
        else:
            row = -1
            name = ""
            tags = ""
            test_set = ""
            state = ""
        # create new tab,but if exist , do not create the new tab
        create = True
        if self.execution_tabwidget.count() > 1:
            count = self.execution_tabwidget.count()
            for i in range(count):
                if self.execution_tabwidget.tabText(i) == name:
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
            self.execution_details_name_lineedit.setText(name)
            self.execution_details_tags_lineedit.setText(tags)
            self.execution_details_testset_lineedit.setText(test_set)
            self.execution_details_state_lineedit.setText(state)
            self.execution_details_row_lineedit.setText(str(row))
            # print(data_row.value("TestSet_Name_2"))
        # regenerate the actions_column
        self.execution_tableview_add_actions_column()

    def delete_execution_record(self):
        # get the selected  QPushButton's parent : the QWidget
        execution_action_widget_selected = self.sender().parent()
        # print(type(ex_right_ex_widget_selected))
        # get the index of the QWidget in the tableview and it's row
        execution_action_widget_index = self.execution_tableview.indexAt(execution_action_widget_selected.pos())
        execution_action_widget_row = execution_action_widget_index.row()
        # print(ex_right_ex_widget_row)
        # remove the row from the model
        self.execution_tableview_model.removeRow(execution_action_widget_row)
        # regenerate the actions_column
        self.execution_tableview_add_actions_column()

    def save_execution_record(self):
        row_edit = self.execution_tabwidget.currentWidget().findChild(QLineEdit, name="row",
                                                                      options=Qt.FindChildrenRecursively)
        if row_edit is not None:
            row = int(row_edit.text())
            name = self.execution_tabwidget.currentWidget().findChild(QLineEdit, name="name",
                                                                      options=Qt.FindChildrenRecursively).text()
            tags = self.execution_tabwidget.currentWidget().findChild(QLineEdit, name="tags",
                                                                      options=Qt.FindChildrenRecursively).text()
            testset = self.execution_tabwidget.currentWidget().findChild(QLineEdit, name="testset",
                                                                         options=Qt.FindChildrenRecursively).text()
            state = self.execution_tabwidget.currentWidget().findChild(QLineEdit, name="state",
                                                                       options=Qt.FindChildrenRecursively).text()
            if row != -1:
                record = self.execution_tableview_model.record(row)
                print("editing row: " + str(row))
                record.setValue("Name", name)
                record.setValue("Tags", tags)
                record.setValue("TestSet_Name_2", testset)
                record.setValue("State", state)
                self.execution_tableview_model.setRecord(row, record)
                self.execution_tableview_add_actions_column()
            else:
                record = self.execution_tableview_model.record()
                print("editing row: " + str(row))
                record.setValue("Name", name)
                record.setValue("Tags", tags)
                record.setValue("TestSet_Name_2", testset)
                record.setValue("State", state)
                self.execution_tableview_model.insertRecord(0, record)
                self.execution_tabwidget.removeTab(self.execution_tabwidget.currentIndex())
                self.execution_tableview_add_actions_column()
        else:
            print("No need saving.")

    # testing
    def add_execution_record(self):
        record = self.execution_tableview_model.record()
        record.setValue("Name", "ex1")
        record.setValue("Tags", "tag")
        record.setValue("TestSet_Name_2", 3)
        record.setValue("State", "notready")
        self.execution_tableview_model.insertRecord(0, record)
        self.execution_tableview_model.select()
