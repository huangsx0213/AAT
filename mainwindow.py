from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import QTabBar

from ui_mainwindow import Ui_MainWindow
from mainwindow_ui import MainWindow_Ui
class MainWindow2(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow2, self).__init__(parent)
        self.setupUi(self)
class MainWindow(QtWidgets.QTabWidget, MainWindow_Ui):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        # List view data and action
        self.ex_list_view_model = QStandardItemModel()
        # Load the data to the model
        self.ex_list_view_model = self.ex_leftmenu_listview_loadModelData(self.ex_list_view_model)
        # SConnect the model to the listView
        self.ex_left_menu_listview.setModel(self.ex_list_view_model)
        self.ex_left_menu_listview.clicked.connect(self.ex_left_listview_on_clicked)

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
            self.ex_right_content_tabwidget.addTab(self.ex_right_content_allex_tab, "All Test Sets")
        elif current_listdata == "Variables":
            self.ex_right_content_tabwidget.addTab(self.ex_right_content_allva_tab, "Variables")
        elif current_listdata == "Machines":
            self.ex_right_content_tabwidget.addTab(self.ex_right_content_allma_tab, "Machines")
        QTabBar.setTabButton(self.ex_right_content_tabwidget.tabBar(), 0, QTabBar.RightSide, None)
