import sys
from PyQt5.QtWidgets import (QApplication, QHeaderView, QStyle, QStyleOptionButton, QTableView, QCheckBox,
                             QItemDelegate)
from PyQt5.QtCore import (pyqtSignal, Qt, QAbstractTableModel, QModelIndex, QRect, QVariant, QSize)
from PyQt5.QtGui import QBrush, QColor, QFont, QPen, QFontMetrics, QTextDocument


#
# GROUPNAME,TID,UPLIMIT,LOWLIMIT,UNIT,UUT1,UUT2,UUT3,UUT4 = range(9)
#
#
#
# class TestItem(object):
#
#     def __init__(self,groupname='',tid='',uplimit='',lowlimit='',unit='',uut1='',uut2='',uut3='',uut4=''):
#         self.groupname = groupname
#         self.tid = tid
#         self.uplimit = uplimit
#         self.lowlimit = lowlimit
#         self.unit = unit
#         self.uut1 = uut1
#         self.uut2 = uut2
#         self.uut3 = uut3
#         self.uut4 = uut4
#
#     def __hash__(self):
#         return super(TestItem,self).__hash__()
#
#
#
# class TableViewModel(QAbstractTableModel):
#
#     def __init__(self,state=None):
#         super(TableViewModel, self).__init__()
#         # Keep track of which object are checked
#         self.testitem = []
#         self.state = state
#
#     def rowCount(self, index=QModelIndex()):
#         return len(self.testitem)
#
#     def columnCount(self, index=QModelIndex()):
#         return 9
#
#
#     def data(self, index, role):
#         if (not index.isValid() or
#             not (0 <= index.row() < len(self.testitem))):
#             return QVariant()
#         item = self.testitem[index.row()]
#         column = index.column()
#         if role == Qt.DisplayRole:
#             if column == GROUPNAME:
#                 return item.groupname
#             elif column == TID:
#                 return item.tid
#             elif column == UPLIMIT:
#                 return item.uplimit
#             elif column ==LOWLIMIT:
#                 return item.lowlimit
#             elif column == UNIT:
#                 return item.unit
#             elif column == UUT1:
#                 return item.uut1
#             elif column == UUT2:
#                 return item.uut2
#             elif column == UUT3:
#                 return item.uut3
#             elif column == UUT4:
#                 return item.uut4
#         elif role == Qt.TextColorRole:#Qt.BackgroundRole:
#             if 'FAIL' in item.uut1 or item.uut2 or item.uut3 or item.uut4:
#                 return QVariant(QColor(Qt.red))
#             elif 'PASS' in item.uut1 or item.uut2 or item.uut3 or item.uut4:
#                 return QVariant(QColor(Qt.green))
#             elif 'ERROR' in item.uut1 or item.uut2 or item.uut3 or item.uut4:
#                 return QVariant(QColor(Qt.red))
#         return QVariant()
#
#     def headerData(self, section, orientation, role):
#         if role == Qt.TextAlignmentRole:
#             if orientation == Qt.Horizontal:
#                 return QVariant(int(Qt.AlignLeft|Qt.AlignVCenter))
#             return QVariant(int(Qt.AlignRight|Qt.AlignVCenter))
#         if role != Qt.DisplayRole:
#             return QVariant()
#         if role == Qt.DisplayRole:
#             if orientation == Qt.Horizontal:
#                 if section == GROUPNAME:
#                     return QVariant('Group')
#                 elif section == TID:
#                     return QVariant('Tid')
#                 elif section ==UPLIMIT:
#                     return QVariant('Uplimit')
#                 if section == LOWLIMIT:
#                     return QVariant('Lowlimit')
#                 if section == UNIT:
#                     return QVariant('Unit')
#                 elif section == UUT1:
#                     return QVariant('UUT1')
#                 elif section ==UUT2:
#                     return QVariant('UUT2')
#                 if section == UUT3:
#                     return QVariant('UUT3')
#                 elif section == UUT4:
#                     return QVariant('UUT4')
#         return QVariant()
#
#     def headerClick(self,state):
#         self.beginResetModel()
#         #print index,state
#         self.state = state
#
#         self.endResetModel()


class CheckBoxHeader(QHeaderView):
    clicked = pyqtSignal(dict)
    _x_offset = 3
    _y_offset = 0
    _width = 20
    _height = 20

    def __init__(self, orientation=Qt.Horizontal, parent=None, state=None):
        super(CheckBoxHeader, self).__init__(orientation, parent)
        self.state = state
        # self.setStyleSheet("QHeaderView::section{background-color:green;color: black;};")

    def paintSection(self, painter, rect, logicalIndex):
        painter.save()
        super(CheckBoxHeader, self).paintSection(painter, rect, logicalIndex)

        painter.restore()
        self._y_offset = int((rect.height() - self._width) / 2.)
        if logicalIndex == 5:
            self._self(painter, rect, logicalIndex)
        # elif logicalIndex == 6:
        #     self._self(painter, rect, logicalIndex)
        # elif logicalIndex == 7:
        #     self._self(painter, rect, logicalIndex)
        # elif logicalIndex == 8:
        #     self._self(painter, rect, logicalIndex)

    def mousePressEvent(self, event):
        index = self.logicalIndexAt(event.pos())
        if 5 == index:
            self._selevent(index, event)
        # elif 6 == index:
        #     self._selevent(index, event)
        # elif 7 == index:
        #     self._selevent(index, event)
        # elif 8 == index:
        #     self._selevent(index, event)
        super(CheckBoxHeader, self).mousePressEvent(event)

    def _self(self, painter, rect, logicalIndex):
        option = QStyleOptionButton()
        option.rect = QRect(rect.x() + self._x_offset, rect.y() + self._y_offset, self._width, self._height)
        option.state = QStyle.State_Enabled | QStyle.State_Active
        if self.state.get(logicalIndex):
            option.state |= QStyle.State_On
        else:
            option.state |= QStyle.State_Off
        self.style().drawControl(QStyle.CE_CheckBox, option, painter)

    def _selevent(self, index, event):
        # x = self.sectionPosition(index)
        x = self.sectionViewportPosition(index)
        # x = event.pos().x()
        if x + self._x_offset < event.pos().x() < x + self._x_offset + self._width and self._y_offset < event.pos().y() < self._y_offset + self._height:
            if self.state.get(index):
                self.state[index] = False
            else:
                self.state[index] = True
            self.clicked.emit(self.state)
            self.update()


#
# import time
#
class TableViewModel(QAbstractTableModel):

    def __init__(self, parent=None, mylist=None, state=None):
        super(TableViewModel, self).__init__(parent)
        # Keep track of which object are checked
        self.mylist = mylist
        self.state = state

    def rowCount(self, QModelIndex):
        if self.mylist == None:
            return 1
        return len(self.mylist) + 1

    def columnCount(self, QModelIndex):
        # return len(self.mylist[0])
        return 9

    # def updateData(self,row):
    #     if row<0:
    #         return
    #     t0 = QModelIndex(row,5)
    #     t1 = QModelIndex(row,8)
    #     self.dataChanged(t0,t1)

    def data(self, index, role):
        if not index.isValid():
            return None
        try:
            if role == Qt.DisplayRole:
                # if index.column() >4:
                #     for item in(self.state.keys()):
                #         if index.column() == item and self.state[item] == False:
                #            return QVariant()
                return QVariant(self.mylist[index.row()][index.column()])
            # set color
            # elif role == Qt.TextColorRole:#Qt.BackgroundRole:
            #     if index.column() > 4:
            #         for item in(self.state.keys()):
            #             if index.column() == item and self.state[item] == False:
            #                 return QColor(237,237,237)
            #             if 'FAIL' in self.mylist[index.row()][index.column()]:
            #                 return QColor(Qt.red)
            #             elif 'PASS' in self.mylist[index.row()][index.column()]:
            #                 return QColor(Qt.green)
            #             elif 'ERROR' in self.mylist[index.row()][index.column()]:
            #                 return QColor(Qt.red)
            #     return QVariant()
            return QVariant()
        except Exception:
            return None

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                if section == 0:
                    return 'Group'
                elif section == 1:
                    return 'TestName'
                elif section == 2:
                    return 'Uplimit'
                if section == 3:
                    return 'Lowlimit'
                if section == 4:
                    return 'NetName'
                elif section == 5:
                    return 'UUT1'
                elif section == 6:
                    return 'UUT2'
                # if section == 7:
                #     return 'UUT3'
                # elif section == 8:
                #     return 'UUT4'

        return QVariant()

    def headerClick(self, state):
        self.beginResetModel()
        # print index,state
        self.state = state

        self.endResetModel()


class MyDelegate(QItemDelegate):
    def __init__(self, parent=None, *args):
        QItemDelegate.__init__(self, parent, *args)

    def paint(self, painter, option, index):
        value = index.data(Qt.DisplayRole)

        if value:
            if index.column() > 4:
                if "PASS" in value:
                    painter.setPen(QPen(Qt.blue))
                elif "FAIL" or "ERROR" or "Miss" or "Time Out" in value:
                    painter.setPen(QPen(Qt.red))
                fm = QFontMetrics(QFont())
                painter.drawText(option.rect, Qt.AlignCenter, value)
            else:
                QItemDelegate.paint(self, painter, option, index)

    # def sizeHint(self, option, index):
    #     fm = option.fontMetrics
    #     if index.column() ==1:
    #         return QSize(fm.width("9,999,999,999,999,999"),fm.height())
    #     else:
    #
    #
    #         #text = index.model().data(index)
    #         document = QTextDocument()
    #         document.setDefaultFont(option.font)
    #         return QSize(document.idealWidth()+5,fm.height())

    # painter.save()
    #
    # # set background color
    # painter.setPen(QPen(Qt.NoPen))
    # if option.state & QStyle.State_Selected:
    #     painter.setBrush(QBrush(Qt.blue))
    # else:
    #     # if index.row()%2==0:
    #     painter.setBrush(QBrush(Qt.white))
    #     # else:
    #     #     painter.setBrush(QBrush(Qt.lightGray))
    # painter.drawRect(option.rect)
    #
    # # set text color
    #
    # value = index.data(Qt.DisplayRole)
    # if value:
    #     # text = value.toString()
    #     if index.column() > 4:
    #         if "PASS" in value:
    #             painter.setPen(QPen(Qt.green))
    #         elif "FAIL" or "ERROR" in value:
    #             painter.setPen(QPen(Qt.red))
    #     else:
    #         painter.setPen(QPen(Qt.black))
    #     fm = QFontMetrics(QFont())
    #     timestampWidth = fm.width(value)
    #
    #     painter.drawText(option.rect, Qt.AlignLeft, value)
    #
    # painter.restore()


