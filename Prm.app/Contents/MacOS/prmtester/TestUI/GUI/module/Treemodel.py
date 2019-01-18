#!/usr/bin/env python


from PyQt5.QtCore import (QAbstractItemModel, QFile, QIODevice,QSize,
        QItemSelectionModel, QModelIndex, Qt,QVariant)
from PyQt5.QtWidgets import QItemDelegate,QStyleOptionViewItem,QApplication,QStyle,QTreeView
from PyQt5.QtGui import QBrush,QColor,QFont,QPen,QFontMetrics


#HEAD = ("GROUP","TID","LL","UL","UNIT","UUT1","UUT2","UUT3","UUT4","UUT5","UUT6","FUNCTION","PARA1","PARA2","TIMEOUT","DESCRIPTION")
HEAD = ("GROUP","TID","LSL","USL","UNIT","UUT1","UUT2","UUT3","UUT4","r1","r2","r3","r4")

class TreeItem(object):
    def __init__(self, data=None, parent=None):
        self.parentItem = parent
        self.itemData = data
        self.childItems = []

    def child(self, row):
        return self.childItems[row]

    def childCount(self):
        return len(self.childItems)

    def childNumber(self):
        if self.parentItem != None:
            return self.parentItem.childItems.index(self)
        return 0

    def columnCount(self):
        return len(self.itemData)

    def data(self, column):
        return self.itemData[column]

    def insertChildren(self, position, count, columns):
        if position < 0 or position > len(self.childItems):
            return False

        for row in range(count):
            data = [None for v in range(columns)]
            item = TreeItem(data, self)
            self.childItems.insert(position, item)

        return True

    def insertColumns(self, position, columns):
        if position < 0 or position > len(self.itemData):
            return False

        for column in range(columns):
            self.itemData.insert(position, None)

        for child in self.childItems:
            child.insertColumns(position, columns)

        return True

    def parent(self):
        return self.parentItem

    def removeChildren(self, position, count):
        if position < 0 or position + count > len(self.childItems):
            return False

        for row in range(count):
            self.childItems.pop(position)

        return True

    def removeColumns(self, position, columns):
        if position < 0 or position + columns > len(self.itemData):
            return False

        for column in range(columns):
            self.itemData.pop(position)

        for child in self.childItems:
            child.removeColumns(position, columns)

        return True

    def setData(self, column, value):
        if column < 0 or column >= len(self.itemData):
            return False

        self.itemData[column] = value

        return True


class TreeModel(QAbstractItemModel):
    def __init__(self, headers=HEAD, data=None, parent=None):
        super(TreeModel, self).__init__(parent)

        rootData = [header for header in headers]
        self.rootItem = TreeItem(rootData)
        self.setupModelData(data, self.rootItem)


    def columnCount(self, parent=QModelIndex()):
        return self.rootItem.columnCount()

    def data(self, index, role):
        if not index.isValid():
            return None

        if role == Qt.DisplayRole: #and role != Qt.EditRole:
            #return None
        # value = index.data(Qt.DisplayRole)
        #
        # if index.column() in (5, 6, 7, 8, 9, 10):
        #     if "Miss" in value or "Time Out" in value or 'FAIL' in value:
        #         return QColor(Qt.red)
        #     else:
        #         painter.setPen(QPen(Qt.blue))

            item = self.getItem(index)
            return item.data(index.column())
        elif role == Qt.TextColorRole:
            #try:
            item = self.getItem(index)
            value = item.data(index.column())
            if value!=None:
                if index.column() in (5, 6,7,8):
                    result = item.data(index.column()+4)
                    if  result:
                        return QColor(Qt.blue)
                    else:
                        return QColor(Qt.red)
        elif role == Qt.TextAlignmentRole:
            if index.column() == 1:
                return int(Qt.AlignLeft)  # Qt.AlignLeft|Qt.AlignVCenter)
            else:
                return int(Qt.AlignHCenter)#Qt.AlignLeft|Qt.AlignVCenter)

            # except Exception:
            #     return  QVariant()



    # def flags(self, index):
    #     if not index.isValid():
    #         return 0
    #
    #     return Qt.ItemIsEditable | super(TreeModel, self).flags(index)

    def getItem(self, index):
        if index.isValid():
            item = index.internalPointer()
            if item:
                return item

        return self.rootItem

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.rootItem.data(section)
        elif role == Qt.TextAlignmentRole:
            return int(Qt.AlignHCenter)#Qt.AlignLeft|Qt.AlignVCenter)

        return None

    def index(self, row, column, parent=QModelIndex()):
        if parent.isValid() and parent.column() != 0:
            return QModelIndex()

        parentItem = self.getItem(parent)
        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QModelIndex()


    def insertColumns(self, position, columns, parent=QModelIndex()):
        self.beginInsertColumns(parent, position, position + columns - 1)
        success = self.rootItem.insertColumns(position, columns)
        self.endInsertColumns()

        return success

    def insertRows(self, position, rows, parent=QModelIndex()):
        parentItem = self.getItem(parent)
        self.beginInsertRows(parent, position, position + rows - 1)
        success = parentItem.insertChildren(position, rows,
                self.rootItem.columnCount())
        self.endInsertRows()

        return success

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()

        childItem = self.getItem(index)
        parentItem = childItem.parent()

        if parentItem == self.rootItem:
            return QModelIndex()

        return self.createIndex(parentItem.childNumber(), 0, parentItem)

    def removeColumns(self, position, columns, parent=QModelIndex()):
        self.beginRemoveColumns(parent, position, position + columns - 1)
        success = self.rootItem.removeColumns(position, columns)
        self.endRemoveColumns()

        if self.rootItem.columnCount() == 0:
            self.removeRows(0, self.rowCount())

        return success

    def removeRows(self, position, rows, parent=QModelIndex()):
        parentItem = self.getItem(parent)

        self.beginRemoveRows(parent, position, position + rows - 1)
        success = parentItem.removeChildren(position, rows)
        self.endRemoveRows()

        return success

    def rowCount(self, parent=QModelIndex()):
        parentItem = self.getItem(parent)

        return parentItem.childCount()

    def setData(self, index, value, role=Qt.EditRole):
        if role != Qt.EditRole:
            return False

        item = self.getItem(index)
        result = item.setData(index.column(), value)

        if result:
            self.dataChanged.emit(index, index)

        return result

    def setHeaderData(self, section, orientation, value, role=Qt.EditRole):
        if role != Qt.EditRole or orientation != Qt.Horizontal:
            return False

        result = self.rootItem.setData(section, value)
        if result:
            self.headerDataChanged.emit(orientation, section, section)

        return result

    def setupModelData(self,rowdata,parent):
        if not isinstance(rowdata,list):
            print "the model is wrong!!!!!"
            return False
        parent.childItems = []
        number = 0
        index = 0
        while number<len(rowdata):
            if number==0:
                parent.insertChildren(0,1,self.rootItem.columnCount())
            group = parent.child(parent.childCount()-1).data(0)
           # print group, rowdata[number].get("GROUP")
            if group == rowdata[number].get("GROUP"):
                parent.child(parent.childCount()-1).insertChildren(index, 1, self.rootItem.columnCount())
            else:
                if number>0:
                    parent.insertChildren(parent.childCount(), 1, self.rootItem.columnCount())
                index = 0
                parent.child(parent.childCount()-1).setData(0, rowdata[number].get("GROUP"))
                parent.child(parent.childCount()-1).insertChildren(index, 1, self.rootItem.columnCount())
            #for col,item in enumerate(rowdata[number]):
            parent.child(parent.childCount() - 1).child(index).setData(0,rowdata[number].get("row"))
            parent.child(parent.childCount() - 1).child(index).setData(1, rowdata[number].get("TID"))
            parent.child(parent.childCount() - 1).child(index).setData(2, rowdata[number].get("LOW"))
            parent.child(parent.childCount() - 1).child(index).setData(3, rowdata[number].get("HIGH"))
            parent.child(parent.childCount() - 1).child(index).setData(4, rowdata[number].get("UNIT"))
            parent.child(parent.childCount() - 1).child(index).setData(5, "")
            parent.child(parent.childCount() - 1).child(index).setData(6, "")
            parent.child(parent.childCount() - 1).child(index).setData(7, "")
            parent.child(parent.childCount() - 1).child(index).setData(8, "")
            parent.child(parent.childCount() - 1).child(index).setData(9, "")
            parent.child(parent.childCount() - 1).child(index).setData(10, "")
            parent.child(parent.childCount() - 1).child(index).setData(11, "")
            parent.child(parent.childCount() - 1).child(index).setData(12, "")
            # parent.child(parent.childCount() - 1).child(index).setData(13, "")
            # parent.child(parent.childCount() - 1).child(index).setData(14, "")
            # parent.child(parent.childCount() - 1).child(index).setData(15, "")
            # parent.child(parent.childCount() - 1).child(index).setData(16, "")





            # parent.child(parent.childCount() - 1).child(index).setData(11, rowdata[number].get("FUNCTION"))
            # parent.child(parent.childCount() - 1).child(index).setData(12, rowdata[number].get("PARAM1"))
            # parent.child(parent.childCount() - 1).child(index).setData(13, rowdata[number].get("PARAM2"))
            # parent.child(parent.childCount() - 1).child(index).setData(14, rowdata[number].get("TIMEOUT"))
            # parent.child(parent.childCount() - 1).child(index).setData(15, rowdata[number].get("DESCRIPTION"))
            index += 1
            number += 1

class TreeViewDelegate(QItemDelegate):
    def __init__(self, parent=None, *args):
        QItemDelegate.__init__(self, parent, *args)


    def paint(self, painter, option, index):
        value = index.data(Qt.DisplayRole)
        if option.state & QStyle.State_Selected:
            painter.setBrush(QBrush(Qt.lightGray))
            #painter.fillRect(option.rect, option.palette.highlight())
        else:
            painter.setBrush(QBrush(Qt.white))

        #painter.drawRect(option.rect)
        QFont.setPointSize(option.font,14)
        # if index.column()>0:
        option.displayAlignment = Qt.AlignCenter #Qt.AlignLeft |
        painter.setPen(QPen(Qt.lightGray))
        painter.drawRect(option.rect)
        # else:
        #     QItemDelegate.paint(self, painter, option, index)

        if value:
            if index.column() in (5,6,7,8,9,10):
                #QFont.setBold(option.font, True)
                #print value,index.data(6)
                if  "Miss" in value or "Time Out" in value or 'FAIL' in value:
                    painter.setPen(QPen(Qt.red))
                else:
                    painter.setPen(QPen(Qt.blue))
                painter.setFont(QFont('Simsun',14))
                painter.drawText(option.rect,Qt.AlignCenter, value)
                # else:
                #     painter.setPen(QPen(Qt.darkBlue))
                #fm = QFontMetrics(QFont())

                #QApplication.style().drawItemText(painter,option.rect, option.displayAlignment,QApplication.palette(),True, value)
            else:
                QItemDelegate.paint(self,painter,option,index)
        else:
            QItemDelegate.paint(self, painter, option, index)

    def sizeHint(self, option, index):
        return QSize(100,30)



