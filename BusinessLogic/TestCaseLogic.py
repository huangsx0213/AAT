from UserInterface.MainWindowUI import MainWindowUI

class TestCaseLogic(MainWindowUI):
    def test_case_logic(self):

        # test case table logic
        self.setup_dynamic_test_case_tab("test")

    def add_dynamic_test_case_tab(self):
        # get the selected  QPushButton's parent : the QWidget
        test_case_selected = self.sender()
        test_case_menu_index = self.test_case_menu_listview.indexAt(test_case_selected.pos())
        self.test_case_menu_index_row = test_case_menu_index.row()
        # print(ex_right_ex_widget_row)
        # remove the row from the model
        data_row = self.testcase_menu_model.record(self.test_case_menu_index_row)
        row = self.test_case_menu_index_row
        name = data_row.value("Name")
        id = data_row.value("Id")
        print(name)
        tags = data_row.value("Tags")


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
                self.setup_dynamic_execution_tab(name)
            else:
                self.setup_dynamic_execution_tab("New Execution")
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