from PyQt5 import QtWidgets, QtSql
from PyQt5.QtCore import Qt, QModelIndex, QVariant
from PyQt5.QtGui import QStandardItem, QStandardItemModel, QIcon, QCursor
from PyQt5.QtSql import QSqlTableModel, QSqlRelationalTableModel, QSqlRelation, QSqlRelationalDelegate, QSqlRecord
from PyQt5.QtWidgets import QTabBar, QPushButton, QComboBox, QGridLayout

from mainwindow_ui import MainWindow_Ui
from ui_mainwindow import Ui_MainWindow


class MainWindow2(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow2, self).__init__(parent)
        self.setupUi(self)
class MainWindow(QtWidgets.QTabWidget, MainWindow_Ui):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
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

        self.ex_right_ex_tableview_model=QSqlRelationalTableModel()
        self.ex_right_ex_tableview_model.setTable("Execution")
        self.ex_right_ex_tableview_model.setEditStrategy(QSqlTableModel.OnRowChange)
        self.ex_right_ex_tableview_model.setRelation(3,QSqlRelation("TestSet","Id","Name"))
        self.ex_right_ex_tableview_model.setHeaderData(3, Qt.Horizontal, "TestSet")
        self.ex_right_ex_tableview_model.select()
        self.ex_right_ex_tableview.setModel(self.ex_right_ex_tableview_model)
        self.ex_right_ex_tableview.setItemDelegate(QSqlRelationalDelegate(self.ex_right_ex_tableview))
        self.ex_right_ex_tableview.verticalHeader().setVisible(False)
        #self.ex_right_ex_tableview_model.insertRow(4)
        #self.add_execution()

        # add a column into the ex table for actions
        self.ex_right_ex_tableview_model.insertColumn(5)
        self.ex_right_ex_tableview_model.setHeaderData(5, Qt.Horizontal, "Actions")
        for row in range(self.ex_right_ex_tableview_model.rowCount()):
            self.setup_ex_right_ex_actions_column()
            self.ex_right_ex_index = self.ex_right_ex_tableview.model().index(row, 5)
            self.ex_right_ex_tableview.setIndexWidget(self.ex_right_ex_index, self.ex_right_ex_widget)

        self.ex_right_ts_tableview_model = QSqlTableModel()
        self.ex_right_ts_tableview_model.setTable("TestSet")
        self.ex_right_ts_tableview_model.setEditStrategy(QSqlTableModel.OnRowChange)
        self.ex_right_ts_tableview_model.select()
        self.ex_right_ts_tableview.setModel(self.ex_right_ts_tableview_model)
        self.ex_right_ts_tableview.verticalHeader().setVisible(False)



    def add_execution(self):
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
        self.listdata = ['Executions', 'Test Sets', 'Variables', 'Machines']
        for row in self.listdata:
            item = QStandardItem(row)
            #Set item AlignCenter
            #item.setTextAlignment(QtCore.Qt.AlignCenter)
            model.appendRow(item)
        return model
    def ex_left_listview_on_clicked(self, index):
        current_row=index.row()
        current_listdata=self.listdata[current_row]
        print("You are selecting row "+str(current_row))
        self.ex_right_content_tabwidget.removeTab(0)
        if current_listdata=="Executions":
            self.ex_right_content_tabwidget.addTab(self.ex_right_content_allex_tab, "All Executions")
        elif current_listdata=="Test Sets":
            self.ex_right_content_tabwidget.addTab(self.ex_right_content_allts_tab, "All Test Sets")
        elif current_listdata == "Variables":
            self.ex_right_content_tabwidget.addTab(self.ex_right_content_allva_tab, "Variables")
        elif current_listdata == "Machines":
            self.ex_right_content_tabwidget.addTab(self.ex_right_content_allma_tab, "Machines")
        QTabBar.setTabButton(self.ex_right_content_tabwidget.tabBar(), 0, QTabBar.RightSide, None)
