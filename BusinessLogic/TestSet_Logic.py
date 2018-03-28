from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlTableModel, QSqlQuery, QSqlQueryModel
from PyQt5.QtWidgets import QLineEdit, QHeaderView

from UserInterface.MainWindow_UI import MainWindow_UI
from UserInterface.CheckableTestcaseTree import CheckableTestcaseNode, CheckalbeTestcaseFolderNode, \
    CheckableTestCaseTreeModel


class TestSet_Logic(MainWindow_UI):
    def testset_logic(self):
        # testset table logic
        self.testset_tableview_model = QSqlTableModel()
        self.testset_tableview_model.setTable("TestSet")
        self.testset_tableview_model.setEditStrategy(QSqlTableModel.OnRowChange)
        self.testset_tableview_model.select()
        self.testset_tableview.setModel(self.testset_tableview_model)
        self.testset_tableview.verticalHeader().setVisible(False)
        self.testset_tableview.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.testset_tableview.horizontalHeader().setStyleSheet("::section{Background-color:rgb(220,220,220)}")
        self.testset_tableview_add_actions_column()

        self.testset_testcase_tableview_model = QSqlTableModel()
        self.testset_testcase_tableview_model.setTable("Testcase")
        self.testset_testcase_tableview_model.setFilter(
            "Id in (select testcaseId from testsettestcase where testsetId='1')")
        self.testset_testcase_tableview_model.setHeaderData(1, Qt.Horizontal, "CaseName")
        # Qt.AscendingOrder or Qt.DescendingOrder
        self.testset_testcase_tableview_model.setSort(0, Qt.AscendingOrder)
        self.testset_testcase_tableview_model.select()
        self.testset_testcase_tableview.setModel(self.testset_testcase_tableview_model)

        self.testset_testcase_tableview.verticalHeader().setVisible(False)
        self.testset_testcase_tableview.setColumnHidden(0, True)
        self.testset_testcase_tableview.setColumnHidden(3, True)
        self.testset_testcase_tableview.setColumnHidden(4, True)
        self.testset_testcase_tableview.setColumnHidden(5, True)
        self.testset_testcase_tableview.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.testset_testcase_tableview.horizontalHeader().setStyleSheet("::section{Background-color:rgb(220,220,220)}")

        # self.setup_dynamic_testset_tab("test")

    def testset_tableview_add_actions_column(self):
        # add a column into the ex table for actions
        self.testset_tableview_model.select()
        tem_column_count = self.testset_tableview_model.columnCount()
        self.testset_tableview_model.insertColumn(tem_column_count)
        self.testset_tableview_model.setHeaderData(tem_column_count, Qt.Horizontal, "Actions")

        for row in range(self.testset_tableview_model.rowCount()):
            self.setup_testset_actions_column()
            self.testset_view_button.clicked.connect(self.view_testset_tab_ui)
            self.testset_edit_button.clicked.connect(self.add_dynamic_testset_tab)
            self.testset_delete_button.clicked.connect(self.delete_testset_record)
            self.testset_index = self.testset_tableview.model().index(row, tem_column_count)
            self.testset_tableview.setIndexWidget(self.testset_index, self.testset_action_widget)

    def view_testset_tab_ui(self):
        # get the selected  QPushButton's parent : the QWidget
        testset_action_widget_selected = self.sender().parent()
        # print(self.sender().objectName())
        if self.sender().objectName() == "testset_view":
            # get the index of the QWidget in the tableview and it's row
            testset_action_widget_index = self.testset_tableview.indexAt(testset_action_widget_selected.pos())
            self.testset_action_widget_row = testset_action_widget_index.row()
            # print(ex_right_ex_widget_row)
            # remove the row from the model
            data_row = self.testset_tableview_model.record(self.testset_action_widget_row)
            testset_id = data_row.value("Id")
        self.testset_testcase_tableview_model.setFilter(
            "Id in (select testcaseId from testsettestcase where testsetId='" + str(testset_id) + "')")
        self.testset_testcase_tableview_model.setSort(0, Qt.AscendingOrder)
        self.testset_testcase_tableview_model.select()
        self.testset_testcase_tableview.setModel(self.testset_testcase_tableview_model)
        self.testset_tableview.selectRow(self.testset_action_widget_row)

    def delete_testset_record(self):
        # get the selected  QPushButton's parent : the QWidget
        testset_action_widget_selected = self.sender().parent()
        # print(type(ex_right_ex_widget_selected))
        # get the index of the QWidget in the tableview and it's row
        testset_action_widget_index = self.testset_tableview.indexAt(testset_action_widget_selected.pos())
        testset_action_widget_row = testset_action_widget_index.row()
        # print(ex_right_ex_widget_row)
        # remove the row from the model
        testsetId_delete = self.testset_tableview_model.record(testset_action_widget_row).value("Id")
        QSqlQuery("delete from testsettestcase where testsetId ='" + str(testsetId_delete) + "'")
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

    def add_dynamic_testset_tab(self):
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
            testset_id = data_row.value("Id")
        else:
            row = -1
            name = ""
            query = QSqlQuery("SELECT Id FROM Testset order by Id desc")
            query.next()
            testset_id = query.value(0) + 1
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

            rootNode = CheckableTestcaseNode(0, "TestCases", 0)

            self.initialize_have_tags_testcase(rootNode, testset_id)

            self.initialize_non_tags_testcase(rootNode, testset_id)
            # print(rootNode)
            model = CheckableTestCaseTreeModel(rootNode)
            self.testset_details_testcases_treeview.setModel(model)
        # regenerate the actions_column
        self.testset_tableview_add_actions_column()

    def initialize_have_tags_testcase(self, rootNode, testset_id):
        query_tags = QSqlQuery()
        query_tags.prepare("SELECT distinct Tags FROM TestCase where Tags is not Null")
        query_tags.exec_()
        query_tags_model = QSqlQueryModel()
        query_tags_model.setQuery(query_tags)
        query_tags_count = query_tags_model.rowCount()
        for i in range(0, query_tags_count):
            tag_name = query_tags_model.data(query_tags_model.index(i, 0))
            childNode0 = CheckalbeTestcaseFolderNode(0, tag_name, str(testset_id), rootNode)
            query_have_tags_testcase = QSqlQuery()
            query_have_tags_testcase.prepare("SELECT Id,Name FROM TestCase where Tags=:tags")
            query_have_tags_testcase.bindValue(":tags", tag_name)
            query_have_tags_testcase.exec_()
            have_tags_testcase_model = QSqlQueryModel()
            have_tags_testcase_model.setQuery(query_have_tags_testcase)
            have_tags_testcase_count = have_tags_testcase_model.rowCount()
            tem_selected_testcase_count = 0
            for j in range(0, have_tags_testcase_count):
                tem_testcase_id = have_tags_testcase_model.data(have_tags_testcase_model.index(j, 0))
                tem_testcase_name = have_tags_testcase_model.data(have_tags_testcase_model.index(j, 1))
                query_selected_testcase = QSqlQuery()
                query_selected_testcase.prepare(
                    "SELECT TestcaseId FROM TestsetTestcase where TestsetId = :TestsetId and TestcaseId =:TestcaseId")
                query_selected_testcase.bindValue(":TestsetId", testset_id)
                query_selected_testcase.bindValue(":TestcaseId", tem_testcase_id)
                query_selected_testcase.exec_()
                selected_testcase_model = QSqlQueryModel()
                selected_testcase_model.setQuery(query_selected_testcase)
                selected_testcase_count = selected_testcase_model.rowCount()
                if selected_testcase_count == 1:
                    check_status = Qt.Checked
                    tem_selected_testcase_count = tem_selected_testcase_count + 1
                else:
                    check_status = Qt.Unchecked

                childNode1 = CheckableTestcaseNode(tem_testcase_id, tem_testcase_name, testset_id, childNode0,
                                                   check_status)

            if selected_testcase_count == tem_selected_testcase_count:
                childNode0.setCheckStatus(Qt.Checked)
            elif tem_selected_testcase_count > 0:
                childNode0.setCheckStatus(Qt.PartiallyChecked)
            else:
                childNode0.setCheckStatus(Qt.Unchecked)

    def initialize_non_tags_testcase(self, rootNode, testset_id):
        # query the testcase which has no tags
        query_non_tags_testcase = QSqlQuery()
        query_non_tags_testcase.prepare("SELECT Id,Name FROM TestCase where Tags is Null")
        query_non_tags_testcase.exec_()
        # set model for the testcase which has no tags
        non_tags_testcase_Model = QSqlQueryModel()
        non_tags_testcase_Model.setQuery(query_non_tags_testcase)
        # print(query_non_tags_Model.rowCount())
        for i in range(0, non_tags_testcase_Model.rowCount()):
            tem_testcase_id = non_tags_testcase_Model.data(non_tags_testcase_Model.index(i, 0))
            tem_testcase_name = non_tags_testcase_Model.data(non_tags_testcase_Model.index(i, 1))
            # query the checked testcase which has no tags
            query_non_tags_checked_testcase = QSqlQuery()
            query_non_tags_checked_testcase.prepare(
                "SELECT TestcaseId FROM TestsetTestcase where TestsetId =:TestsetId and TestcaseId=:TestcaseId")
            query_non_tags_checked_testcase.bindValue(":TestsetId", testset_id)
            query_non_tags_checked_testcase.bindValue(":TestcaseId", tem_testcase_id)
            query_non_tags_checked_testcase.exec_()
            # set model for the checked testcase which has no tags
            non_tags_checked_testcase_model = QSqlQueryModel()
            non_tags_checked_testcase_model.setQuery(query_non_tags_checked_testcase)
            non_tags_testcase_count = non_tags_checked_testcase_model.rowCount()
            # print(non_tags_testcase_count)
            if non_tags_testcase_count == 1:
                check_status = Qt.Checked
            else:
                check_status = Qt.Unchecked
            childNode2 = CheckableTestcaseNode(tem_testcase_id, tem_testcase_name, testset_id, rootNode, check_status)
