from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon


class MainWindow_Ui(object):
    def setupUi(self, MainWindow):

        #settings of MainWindow,the QTabWidget.
        self.setWindowIcon(QIcon('.\images\logo.png'))
        self.resize(800, 600)
        self.setWindowTitle('AAT 2.0')

        # define the first tab and add it into the QTabWidget.
        self.execution_tab = QtWidgets.QWidget()
        self.execution_tab.setObjectName("tab")
        self.addTab(self.execution_tab, "Execution")

        # define the second tab and add it into the QTabWidget.
        self.testcase_tab = QtWidgets.QWidget()
        self.testcase_tab.setObjectName("tab1")
        self.addTab(self.testcase_tab, "TestCase")

        # define the third tab and add it into the QTabWidget.
        self.action_tab = QtWidgets.QWidget()
        self.action_tab.setObjectName("tab2")
        self.addTab(self.action_tab, "Action")