from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QStandardItem, QStandardItemModel

from ui_mainwindow import Ui_MainWindow
from mainwindow_ui import MainWindow_Ui
class MainWindow2(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow2, self).__init__(parent)
        self.setupUi(self)

    #     self.Title.setText("hello Python")
    #     self.World.clicked.connect(self.onWorldClicked)
    #     self.China.clicked.connect(self.onChinaClicked)
    #     self.lineEdit.textChanged.connect(self.onlineEditTextChanged)
    #
    # def onWorldClicked(self, remark):
    #     print(remark)
    #     self.Title.setText("Hello World")
    #
    # def onChinaClicked(self):
    #     self.Title.setText("Hello China")
    #
    # def onlineEditTextChanged(self,p_str):
    #     self.Title.setText(p_str)
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
        a=index.row()
        b=self.listdata[a]
        print("You are selecting row "+str(a))
        print("You are selecting data " + b)