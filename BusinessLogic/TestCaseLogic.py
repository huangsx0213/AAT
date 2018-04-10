from UserInterface.MainWindowUI import MainWindowUI


class TestCaseLogic(MainWindowUI):
    def test_case_logic(self):
        pass

    def add_dynamic_test_case_tab(self, index):
        test_case_row = index.row()
        test_case_name = self.testcase_menu_model.record(test_case_row).value("Name")
        test_case_description = self.testcase_menu_model.record(test_case_row).value("Description")
        test_case_tags = self.testcase_menu_model.record(test_case_row).value("Tags")
        test_case_status = self.testcase_menu_model.record(test_case_row).value("Status")

        count = self.test_case_tabwidget.count()
        is_tab_existing = False
        for i in range(0, count):
            if (self.test_case_tabwidget.tabText(i) == test_case_name):
                is_tab_existing = True
                self.test_case_tabwidget.setCurrentIndex(i)
                break
        if not is_tab_existing:
            self.setup_dynamic_test_case_tab(test_case_name)

            self.test_case_details_name_lineedit.setText(test_case_name)
            self.test_case_details_description_lineedit.setText(test_case_description)
            self.test_case_details_tags_lineedit.setText(test_case_tags)
            self.test_case_details_status_lineedit.setText(test_case_status)
