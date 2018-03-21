from PyQt5.QtCore import Qt, QAbstractItemModel, QModelIndex
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtSql import QSqlTableModel, QSqlRelationalTableModel, QSqlRelation, QSqlRelationalDelegate, QSqlQuery
from PyQt5.QtWidgets import QLineEdit

from UserInterface.MainWindow_UI import MainWindow_UI


class Node(object):

    def __init__(self, name,parent=None,checkStatus=Qt.Unchecked):

        self._name = name
        self._children = []
        self._parent = parent
        self._checkStatus=checkStatus

        if parent is not None:
            parent.addChild(self)

    def typeInfo(self):
        return "TestCase"

    def addChild(self, child):
        self._children.append(child)

    def insertChild(self, position, child):

        if position < 0 or position > len(self._children):
            return False

        self._children.insert(position, child)
        child._parent = self
        return True

    def removeChild(self, position):

        if position < 0 or position > len(self._children):
            return False

        child = self._children.pop(position)
        child._parent = None

        return True

    def name(self):
        return self._name

    def setName(self, name):
        self._name = name
    def checkStatus(self):
        return self._checkStatus

    def setCheckStatus(self, checkStatus):
        self._checkStatus = checkStatus
    def child(self, row):
        return self._children[row]

    def childCount(self):
        return len(self._children)

    def parent(self):
        return self._parent

    def row(self):
        if self._parent is not None:
            return self._parent._children.index(self)

    def log(self, tabLevel=-1):

        output = ""
        tabLevel += 1

        for i in range(tabLevel):
            output += "\t\t"

        output += "@------" + self._name + "\n"

        for child in self._children:
            output += child.log(tabLevel)

        tabLevel -= 1

        return output

    def __repr__(self):
        return self.log()


class FolderNode(Node):

    def __init__(self, name, parent=None,checkStatus=Qt.Unchecked):
        super(FolderNode, self).__init__(name, parent,checkStatus)

    def typeInfo(self):
        return "FolderNode"
class TestCaseTreeModel(QAbstractItemModel):
    """INPUTS: Node, QObject"""

    def __init__(self, root, parent=None):
        super(TestCaseTreeModel, self).__init__(parent)
        self._rootNode = root

    """INPUTS: QModelIndex"""
    """OUTPUT: int"""

    def rowCount(self, parent):
        if not parent.isValid():
            parentNode = self._rootNode
        else:
            parentNode = parent.internalPointer()

        return parentNode.childCount()

    """INPUTS: QModelIndex"""
    """OUTPUT: int"""

    def columnCount(self, parent):
        return 1

    """INPUTS: QModelIndex, int"""
    """OUTPUT: QVariant, strings are cast to QString which is a QVariant"""

    def data(self, index, role):

        if not index.isValid():
            return None

        node = index.internalPointer()

        if role == Qt.DisplayRole or role == Qt.EditRole:
            if index.column() == 0:
                return node.name()
        if role == Qt.CheckStateRole:
            if index.column() == 0:
                if node.checkStatus()==Qt.Checked:
                    return Qt.Checked
                elif node.checkStatus()==Qt.Unchecked:
                    return Qt.Unchecked
                else:
                    return Qt.PartiallyChecked

        if role == Qt.DecorationRole:
            if index.column() == 0:
                typeInfo = node.typeInfo()

                if typeInfo == "FolderNode":
                    return QIcon(QPixmap("./Images/folder.png"))

                if typeInfo == "TestCase":
                    return QIcon(QPixmap("./Images/item.png"))

    """INPUTS: QModelIndex, QVariant, int (flag)"""

    def setData(self, index, value, role=Qt.EditRole):

        if index.isValid():
            node = index.internalPointer()
            if role == Qt.EditRole:
                node.setName(value)
                return True
            if role ==Qt.CheckStateRole:
                if value==Qt.Checked:
                    node.setCheckStatus(Qt.Checked)
                else:
                    node.setCheckStatus(Qt.Unchecked)
                self.dataChanged.emit(index, index)
                return True

        return False

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable|Qt.ItemIsUserCheckable

    """INPUTS: QModelIndex"""
    """OUTPUT: QModelIndex"""
    """Should return the parent of the node with the given QModelIndex"""

    def parent(self, index):

        node = self.getNode(index)
        parentNode = node.parent()

        if parentNode == self._rootNode:
            return QModelIndex()

        return self.createIndex(parentNode.row(), 0, parentNode)

    """INPUTS: int, int, QModelIndex"""
    """OUTPUT: QModelIndex"""
    """Should return a QModelIndex that corresponds to the given row, column and parent node"""

    def index(self, row, column, parent):

        parentNode = self.getNode(parent)

        childItem = parentNode.child(row)

        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QModelIndex()

    """CUSTOM"""
    """INPUTS: QModelIndex"""

    def getNode(self, index):
        if index.isValid():
            node = index.internalPointer()
            if node:
                return node

        return self._rootNode

    """INPUTS: int, Qt::Orientation, int"""
    """OUTPUT: QVariant, strings are cast to QString which is a QVariant"""
    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if section == 0:
                return "Choose the testcase:"
            else:
                return "Typeinfo"

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
        #self.testset_testcase_tableview_model.setRelation(2, QSqlRelation("TestCase", "Id", "Description"))
        self.testset_testcase_tableview_model.setHeaderData(1, Qt.Horizontal, "CaseName")
        #self.testset_testcase_tableview_model.setHeaderData(2, Qt.Horizontal, "CaseDescription")
        self.testset_testcase_tableview_model.setFilter("testsetId=1")
        #Qt.AscendingOrder or Qt.DescendingOrder
        self.testset_testcase_tableview_model.setSort(1,Qt.AscendingOrder)

        self.testset_testcase_tableview_model.select()
        self.testset_testcase_tableview.setModel(self.testset_testcase_tableview_model)
        self.testset_testcase_tableview.setItemDelegate(QSqlRelationalDelegate(self.testset_testcase_tableview))
        self.testset_testcase_tableview.verticalHeader().setVisible(False)
        self.testset_testcase_tableview.setColumnHidden(0, True)

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
            testset_id=data_row.value("Id")
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
            query = QSqlQuery("SELECT distinct Tags FROM TestCase where Tags is not Null")
            rootNode = Node("TestCases")
            while query.next():
                childNode0 = FolderNode(query.value(0), rootNode)
                sql="SELECT Id,Name FROM TestCase where Tags='"+query.value(0)+"'"
                print(sql)
                query1 = QSqlQuery(sql)
                query1.last()
                item_count = query1.at() + 1
                query1.first()
                query1.previous()
                tem=0
                while query1.next():
                    #print(query1.value(0))
                    #print(query1.value(1))
                    sql="SELECT TestcaseId FROM TestsetTestcase where TestsetId = '"+str(testset_id)+"' and TestcaseId = '"+str(query1.value(0))+"'"
                    print(sql)
                    query3 = QSqlQuery(sql)
                    query3.last()
                    row_count = query3.at() + 1
                    print(row_count)
                    if row_count ==1:
                        checked = Qt.Checked
                        tem=tem+1
                    else:
                        checked = Qt.Unchecked

                    childNode1 = Node(query1.value(1), childNode0,checked)

                if item_count==tem:
                    childNode0.setCheckStatus(Qt.Checked)
                elif tem>0:
                    childNode0.setCheckStatus(Qt.PartiallyChecked)
                else:
                    childNode0.setCheckStatus(Qt.Unchecked)

            sql2 = "SELECT Id,Name FROM TestCase where Tags is Null"
            query2 = QSqlQuery(sql2)
            while query2.next():
                sql = "SELECT TestcaseId FROM TestsetTestcase where TestsetId = '" + str(
                    testset_id) + "' and TestcaseId = '" + str(query2.value(0)) + "'"
                print(sql)
                query3 = QSqlQuery(sql)
                query3.last()
                row_count = query3.at() + 1
                print(row_count)
                if row_count == 1:
                    checked = Qt.Checked
                else:
                    checked = Qt.Unchecked
                childNode2 = Node(query2.value(1), rootNode,checked)
            print(rootNode)
            model = TestCaseTreeModel(rootNode)

            self.testset_details_testcases_treeview.setModel(model)

            # print(data_row.value("TestSet_Name_2"))
        # regenerate the actions_column
        self.testset_tableview_add_actions_column()