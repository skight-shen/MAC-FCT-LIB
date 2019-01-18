#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'prmeasure'

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import csv, os, fcntl, json

path = os.path.abspath(__file__)
functionPath = '/'.join(path.split('/')[:-4]) + '/TestEngine/Driver/FunctionList.json'
instructionPath = '/'.join(path.split('/')[:-4]) + '/TestEngine/Driver/instruction.json'

from Common.Singleton import Singleton

GROUP, TID, DSP, FUNC, TIMEOUT, PARA1, PARA2, UNIT, LOW, HIGH, KEY, VAL = range(12)


# from sigliten import CurrentItem

class Inc(object):
    __slots__ = ("_net_r", "net_w")

    def __init__(self):
        self._net_r = dict(readJSON(instructionPath))
        self.net_w = dict(readJSON(functionPath))

    def getDetails(self, key):
        if key in self._net_r:
            return self._net_r[key]
        else:
            return [""]

    def setToNetdict(self, net, value):
        self.net_w[net] = value

    def getNetFromDict(self, net):
        return self.net_w.get(net)

    def removeFromDict(self, net):
        if net in self.net_w:
            self.net_w.pop(net)


class Item(object):
    __slots__ = ("group", "tid", "dsp", "func", "timeout", "para1", "para2", "unit", "low", "high", "key", "val")

    def __init__(self, group='', tid='', dsp='', func='', timeout='', para1='', para2='', unit='', low='', high='',
                 key='', val=''):
        self.group = group
        self.tid = tid
        self.dsp = dsp
        self.func = func
        self.timeout = timeout
        self.para1 = para1
        self.para2 = para2
        self.unit = unit
        self.low = low
        self.high = high
        self.key = key
        self.val = val

    def __hash__(self):
        return super(Item, self).__hash__()

    def __len__(self):
        return 12


# class Instruction(object):
#     __slots__ = ("_cmd", "_lenth")
#     def __init__(self,cmd = list(),lenth=0):
#         self._cmd = cmd
#         self._lenth = lenth
#
#     def getCmd(self):
#         return self._cmd
#
#     def setCmdByItem(self,value):
#         self._cmd.append(value)
#
#
#     def setCmdByList(self,cmd):
#         self._cmd = cmd
#
#     def setLenth(self,len):
#         self._lenth = len
#
#     def getLenth(self):
#         return self._lenth


def readJSON(path):
    f = open(path, 'r')
    fcntl.flock(f.fileno(), fcntl.LOCK_EX)
    # fcntl.fcntl(f, fcntl.LOCK_UN)
    jsonData = json.load(f)
    f.close()
    return jsonData


class CurrentItem(object):
    """
    CurrentItem is a Singleton
    """
    __metaclass__ = Singleton

    def __init__(self):
        self._item = Item()
        self._row = None
        self._flag = False

    def getCurrentItem(self):
        return self._item

    def setCurrentItem(self, item):
        if isinstance(item, Item):
            self._item = item
            return True
        else:
            return False

    def getCurrentRow(self):
        return self._row

    def setCurrentRow(self, row):
        self._row = row

    def isFinished(self):
        return self._flag

    def setFinishedFlag(self, flag):
        self._flag = flag


class MyTableView(QTableView):
    mydict = pyqtSignal(dict)

    # sig = pyqtSignal(int)
    def __init__(self, arg=None):
        super(MyTableView, self).__init__(arg)
        self.mode = TableViewModel()
        self.groupname = []
        self.setAcceptDrops(True)
        self.scrollToBottom()
        # self.property_table.verticalHeader().setVisible(False)

        # self.tableView.setMouseTracking(True)
        # self.tableView.entered.connect(self.showToolTip)

    # def currentChanged(self, QModelIndex, QModelIndex_1):
    #     row= QModelIndex.row()
    #     self.sig.emit(row)

    def dragEnterEvent(self, e):
        if e.mimeData().hasFormat("text/uri-list"):
            e.accept()
        elif e.mimeData().hasText():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        ci = CurrentItem()
        ci.setFinishedFlag(False)
        name = e.mimeData().text()
        filename = name.split('/')
        path = '/'.join(filename[2::])
        data = []
        if '.csv' in path:
            try:
                with open(path, "r") as f:
                    reader = csv.reader(f)
                    for line in reader:
                        data.append(
                            Item(group=line[0], tid=line[1], dsp=line[2], func=line[3], timeout=line[4], para1=line[5],
                                 para2=line[6], unit=line[7], low=line[8], high=line[9], key=line[10], val=line[11]))
                        # data.append(line)
                        # print line
                if self.mode.mylist is None:
                    self.mode.mylist = data[1::]
                else:
                    self.mode.beginResetModel()
                    self.mode.mylist = None
                    self.mode.endResetModel()
                    self.mode.mylist = data[1::]
                self.mode.header = data[0]
                self.setAlternatingRowColors(True)
                self.setModel(self.mode)
                self.mode.beginResetModel()
                self.mode.endResetModel()
                self.groupname = self.mode.getGroupName()
                temp = {}
                temp.setdefault('groupname', self.groupname)
                temp.setdefault("header", self.mode.header)
                temp.setdefault("context", self.mode.mylist)
                self.mydict.emit(temp)
            except Exception:
                pass

            # print self.groupname
        else:
            try:
                data = e.mimeData().text()
                row = self.indexAt(e.pos()).row()
                count = len(self.mode.mylist)
                if row != -1:
                    self.mode.insertRows(row, data)
                else:
                    self.mode.insertRows(count, data)
            except TypeError:
                pass

    def dragMoveEvent(self, e):
        pass


class TableViewModel(QAbstractTableModel):

    def __init__(self, parent=None, mylist=None, state=None, header=None):
        super(TableViewModel, self).__init__(parent)
        # Keep track of which object are checked
        self.mylist = mylist
        self.state = state
        self.header = header

    def rowCount(self, QModelIndex):
        if self.mylist == None:
            return 100
        return len(self.mylist)

    def columnCount(self, QModelIndex):
        # return len(self.mylist[0])
        return 3

    def getGroupName(self):
        data = []
        try:
            for item in self.mylist:
                if item.group not in data:
                    data.append(item.group)
            return data

        except Exception:
            pass

    def data(self, index, role):
        if not index.isValid():
            return None
        try:
            item = self.mylist[index.row()]
            column = index.column()
            if role == Qt.DisplayRole:
                if column == 0:
                    return item.group
                # elif column == 1:
                #     return item.tid
                elif column == 1:
                    if item.para1 == "" and item.para2 == "":
                        return "{}()".format(item.func)
                    elif item.para1 == "" and item.para2 != "":
                        return "{}({})".format(item.func, item.para2)
                    elif item.para1 != "" and item.para2 == "":
                        return "{}({})".format(item.func, item.para1)
                    else:
                        return "{}({},{})".format(item.func, item.para1, item.para2)

                # elif column ==1:
                #     return
                # if column == GROUP:
                #     return item.group
                # elif column == TID:
                #     return item.tid
                # elif column == DSP:
                #     return item.dsp
                # elif column == FUNC:
                #     return item.func
                # elif column == TIMEOUT:
                #     return item.timeout
                # elif column == PARA1:
                #     return item.para1
                # elif column == PARA2:
                #     return item.para2
                # if column == UNIT:
                #     return item.unit
                # elif column == LOW:
                #     return item.low
                # elif column == HIGH:
                #     return item.high
                # elif column == KEY:
                #     return item.key
                # elif column == VAL:
                #     return item.val

                return QVariant(self.mylist[index.row()][index.column()])
            return QVariant()
        except Exception:
            return None

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                if section == 0:
                    return self.header.group
                # elif section ==1:
                #     return self.header.tid
                elif section == 1:
                    return self.header.func
                # if section == GROUP:
                #     return self.header.group
                # elif section == TID:
                #     return self.header.tid
                # elif section == DSP:
                #     return self.header.dsp
                # elif section == FUNC:
                #     return self.header.func
                # elif section == TIMEOUT:
                #     return self.header.timeout
                # elif section == PARA1:
                #     return self.header.para1
                # elif section == PARA2:
                #     return self.header.para2
                # if section == UNIT:
                #     return self.header.unit
                # elif section == LOW:
                #     return self.header.low
                # elif section == HIGH:
                #     return self.header.high
                # elif section == KEY:
                #     return self.header.key
                # elif section == VAL:
                #     return self.header.val
            elif orientation == Qt.Vertical:

                return str(section)
        return QVariant()

    def insertRows(self, position, data, rows=1, index=QModelIndex()):
        self.beginInsertRows(QModelIndex(), position, position + rows - 1)
        for row in range(rows):
            self.mylist.insert(position + row,
                               Item(func=data))
        self.endInsertRows()
        self.dirty = True
        return True

    def removeRows(self, position, rows=1, index=QModelIndex()):
        self.beginRemoveRows(QModelIndex(), position, position + rows - 1)
        self.mylist = (self.mylist[:position] +
                       self.mylist[position + rows:])
        self.endRemoveRows()
        self.dirty = True
        return True

    def headerClick(self, state):
        self.beginResetModel()
        # print index,state
        self.state = state

        self.endResetModel()
