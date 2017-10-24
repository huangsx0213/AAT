from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlTableModel, QSqlRelationalTableModel, QSqlRelation, QSqlRelationalDelegate
from PyQt5.QtWidgets import QLineEdit

from UserInterface.MainWindow_UI import MainWindow_UI


class TestSet_Logic(MainWindow_UI):
    def testset_logic(self):
        # testset table logic
        self.testset_tableview_model = QSqlTableModel()
        self.testset_tableview_model.setTable("TestSet")
        self.testset_tableview_model.setEditStrategy(QSqlTableModel.OnRowChange)
        self.testset_tableview_model.select()
        self.testset_tableview.setModel(self.testset_tableview_model)
        self.testset_tableview.verticalHeader().setVisible(False)
        self.testset_tableview_add_actions_column()

        self.testset_testcase_tableview_model=QSqlRelationalTableModel()
        self.testset_testcase_tableview_model.setTable("TestsetTestcase")
        self.testset_testcase_tableview_model.setRelation(1, QSqlRelation("TestCase", "Id", "Name"))
        self.testset_testcase_tableview_model.setRelation(2, QSqlRelation("TestCase", "Id", "Description"))
        self.testset_testcase_tableview_model.setHeaderData(1, Qt.Horizontal, "CaseName")
        self.testset_testcase_tableview_model.setHeaderData(2, Qt.Horizontal, "CaseDescription")
        self.testset_testcase_tableview_model.setFilter("testsetId=1")
        #Qt.AscendingOrder or Qt.DescendingOrder
        self.testset_testcase_tableview_model.setSort(2,Qt.AscendingOrder)

        self.testset_testcase_tableview_model.select()
        self.testset_testcase_tableview.setModel(self.testset_testcase_tableview_model)
        self.testset_testcase_tableview.setItemDelegate(QSqlRelationalDelegate(self.testset_testcase_tableview))
        self.testset_testcase_tableview.verticalHeader().setVisible(False)
        self.testset_testcase_tableview.setColumnHidden(0, True)
        self.testset_testcase_tableview.setColumnHidden(3, True)

        #self.setup_dynamic_testset_tab("test")



    def testset_tableview_add_actions_column(self):
        # add a column into the ex table for actions
        self.testset_tableview_model.select()
        tem_column_count = self.testset_tableview_model.columnCount()
        self.testset_tableview_model.insertColumn(tem_column_count)
        self.testset_tableview_model.setHeaderData(tem_column_count, Qt.Horizontal, "Actions")

        for row in range(self.testset_tableview_model.rowCount()):
            self.setup_testset_actions_column()
            self.testset_edit_button.clicked.connect(self.add_testset_tab_ui)
            self.testset_delete_button.clicked.connect(self.delete_testset_record)
            self.testset_index = self.testset_tableview.model().index(row, tem_column_count)
            self.testset_tableview.setIndexWidget(self.testset_index, self.testset_action_widget)

    def delete_testset_record(self):
        # get the selected  QPushButton's parent : the QWidget
        testset_action_widget_selected = self.sender().parent()
        # print(type(ex_right_ex_widget_selected))
        # get the index of the QWidget in the tableview and it's row
        testset_action_widget_index = self.testset_tableview.indexAt(testset_action_widget_selected.pos())
        testset_action_widget_row = testset_action_widget_index.row()
        # print(ex_right_ex_widget_row)
        # remove the row from the model
        self.testset_tableview_model.removeRow(testset_action_widget_row)
        # regenerate the actions_column
        self.testset_tableview_model.submitAll()
        self.testset_tableview_add_actions_column()

    def save_testset_record(self):
        row_edit = self.execution_tabwidget.currentWidget().findChild(QLineEdit, name="row",
                                                                      options=Qt.FindChildrenRecursively)
        if row_edit is not None:
            row = int(row_edit.text())
            name = self.execution_tabwidget.currentWidget().findChild(QLineEdit, name="testset_name",
                                                                      options=Qt.FindChildrenRecursively).text()
            if row != -1:
                record = self.testset_tableview_model.record(row)
                print("editing row: " + str(row))
                record.setValue("Name", name)
                self.testset_tableview_model.setRecord(row, record)
                self.testset_tableview_add_actions_column()
            else:
                record = self.testset_tableview_model.record()
                print("editing row: " + str(row))
                record.setValue("Name", name)
                self.testset_tableview_model.insertRecord(0, record)
                self.execution_tabwidget.removeTab(self.execution_tabwidget.currentIndex())
                self.testset_tableview_add_actions_column()
        else:
            print("No need saving.")

    def add_testset_tab_ui(self):
        # get the selected  QPushButton's parent : the QWidget
        testset_action_widget_selected = self.sender().parent()
        # print(self.sender().objectName())
        if self.sender().objectName() == "testset_edit" or self.sender().objectName() == "testset_edit":
            # get the index of the QWidget in the tableview and it's row
            testset_action_widget_index = self.testset_tableview.indexAt(testset_action_widget_selected.pos())
            self.testset_action_widget_row = testset_action_widget_index.row()
            # print(ex_right_ex_widget_row)
            # remove the row from the model
            data_row = self.testset_tableview_model.record(self.testset_action_widget_row)
            row = self.testset_action_widget_row
            name = data_row.value("Name")
        else:
            row = -1
            name = ""
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
                self.setup_dynamic_testset_tab(name)
            else:
                self.setup_dynamic_testset_tab("New Test Set")
            # self.excution_tab_dic[self.ex_right_ex_widget_row ]=self.ex_right_content_one_ex_tab
            # l=self.excution_tab_dic[self.ex_right_ex_widget_row ].findChild(QLineEdit,name="lname",options=Qt.FindChildrenRecursively)
            # print(l.objectName())
            self.testset_details_name_lineedit.setText(name)
            self.testset_details_row_lineedit.setText(str(row))
            # print(data_row.value("TestSet_Name_2"))
        # regenerate the actions_column
        self.testset_tableview_add_actions_column()