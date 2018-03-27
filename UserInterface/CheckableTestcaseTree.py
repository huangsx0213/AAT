from PyQt5.QtCore import Qt, QAbstractItemModel, QModelIndex
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtSql import QSqlQuery


class CheckableTestcaseNode(object):

    def __init__(self, testcase_id, case_name, testset_id, parent=None, checkStatus=Qt.Unchecked):

        self._children = []
        self._parent = parent
        self._checkStatus = checkStatus
        self._case_name = case_name
        self._testcase_id = testcase_id
        self._testset_id = testset_id

        if parent is not None:
            parent.addChild(self)

    def children(self):
        return self._children

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

    def caseName(self):
        return self._case_name

    def setCaseName(self, name):
        self._case_name = name

    def testcaseId(self):
        return self._testcase_id

    def setTestCaseId(self, id):
        self._testcase_id = id

    def testsetId(self):
        return self._testset_id

    def testseId(self, id):
        self._testset_id = id

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

        output += "@------" + self._case_name + "\n"

        for child in self._children:
            output += child.log(tabLevel)

        tabLevel -= 1

        return output

    def __repr__(self):
        return self.log()


class CheckalbeTestcaseFolderNode(CheckableTestcaseNode):

    def __init__(self, id, name, id2, parent=None, checkStatus=Qt.Unchecked):
        super(CheckalbeTestcaseFolderNode, self).__init__(id, name, id2, parent, checkStatus)

    def typeInfo(self):
        return "FolderNode"


class CheckableTestCaseTreeModel(QAbstractItemModel):
    """INPUTS: Node, QObject"""

    def __init__(self, root, parent=None):
        super(CheckableTestCaseTreeModel, self).__init__(parent)
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
                return node.caseName()
        if role == Qt.CheckStateRole:
            if index.column() == 0:
                if node.childCount() <= 0:
                    if node.checkStatus() == Qt.Checked:
                        return Qt.Checked
                    elif node.checkStatus() == Qt.Unchecked:
                        return Qt.Unchecked
                else:
                    sql = "SELECT count(TestcaseId) FROM TestsetTestcase where TestsetId = '" + str(
                        str(
                            node.testsetId())) + "' and TestcaseId in ( select Id from testcase where tags='" + node.caseName() + "')"
                    # print(sql)
                    query3 = QSqlQuery(sql)
                    query3.next()
                    row_count = query3.value(0)
                    # print(row_count)
                    if row_count == node.childCount():
                        return Qt.Checked
                    elif row_count > 0 and row_count < node.childCount():
                        return Qt.PartiallyChecked
                    else:
                        return Qt.Unchecked

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
                node.setCaseName(value)
                return True
            if role == Qt.CheckStateRole:
                if value == Qt.Checked:
                    node.setCheckStatus(Qt.Checked)
                    sql = "select * from testsettestcase where testsetId = '" + str(
                        node.testsetId()) + "' and testcaseId = '" + str(node.testcaseId()) + "'"
                    # print(sql)
                    query = QSqlQuery(sql)
                    query.last()
                    tem = query.at()
                    item_count = query.at() + 1
                    query.first()
                    query.previous()
                    if item_count < 0 and str(node.testcaseId()) != "0":
                        sql = "insert into testsettestcase (testsetId,testcaseId) values(" + str(
                            node.testsetId()) + "," + str(node.testcaseId()) + ")"
                        # print(sql)
                        QSqlQuery(sql)

                else:
                    node.setCheckStatus(Qt.Unchecked)
                    sql = "select * from testsettestcase where testsetId = '" + str(
                        node.testsetId()) + "' and testcaseId = '" + str(node.testcaseId()) + "'"
                    # print(sql)
                    query = QSqlQuery(sql)
                    query.last()
                    tem = query.at()
                    item_count = query.at() + 1
                    query.first()
                    query.previous()
                    if item_count > 0:
                        sql = "delete from testsettestcase where  testsetId = '" + str(
                            node.testsetId()) + "' and testcaseId = '" + str(node.testcaseId()) + "'"
                        # print(sql)
                        QSqlQuery(sql)

                if node.childCount() > 0:
                    for i in range(0, node.childCount()):
                        child = self.index(i, 0, index)
                        self.setData(child, value, role=Qt.CheckStateRole)

                self.dataChanged.emit(index, index)
                self.dataChanged.emit(self.parent(index), self.parent(index))

                return True
        return False

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsUserCheckable

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
