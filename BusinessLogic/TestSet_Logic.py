from PyQt5.QtGui import QStandardItem, QIcon
from PyQt5.QtSql import QSqlTableModel
from PyQt5.QtWidgets import QAction

from UserInterface.MainWindow_UI import MainWindow_UI


class TestSet_Logic(MainWindow_UI):
    def testset_logic(self):
        # testset table logic
        self.ex_right_ts_tableview_model = QSqlTableModel()
        self.ex_right_ts_tableview_model.setTable("TestSet")
        self.ex_right_ts_tableview_model.setEditStrategy(QSqlTableModel.OnRowChange)
        self.ex_right_ts_tableview_model.select()
        self.ex_right_ts_tableview.setModel(self.ex_right_ts_tableview_model)
        self.ex_right_ts_tableview.verticalHeader().setVisible(False)
        self.current_listdata = QStandardItem(QIcon("./images/execution.png"), "Executions")
        self.ex_right_content_toolbar.actionTriggered[QAction].connect(self.tool_btn_clicked)