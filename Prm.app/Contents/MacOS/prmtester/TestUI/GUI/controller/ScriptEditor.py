from TestUI.GUI.view.ScriptEditor import Ui_Form
from PyQt5.QtWidgets import QWidget,QApplication,QComboBox,QMessageBox,QDesktopWidget
import sys,os
from TestUI.GUI.module.selfTableView import MyTableView,TableViewModel,QTreeWidgetItem,QTreeWidget,QTableView,QTableWidgetItem,QHeaderView,Item,CurrentItem
import json,csv

from TestUI.GUI.module.selfTableView import functionPath,Inc


from TestEngine.Driver.Method import Command



path = "/".join(os.path.abspath(__file__).split('/')[:-4])
savecsvPath = path + '/TestScript.csv'




class MyQTreeWidget(QTreeWidget):
    def __init__(self):
        super(MyQTreeWidget,self).__init__()

        self.setAcceptDrops(False)

    def dragEnterEvent(self, e):
        #currentItem
        item = self.currentItem()
        #item  = self.selectedItems()
        #print item.text(0),item.text(1)
        e.mimeData().setText(item.text(0))
        #print e


    def dropEvent(self, e):
        pass

    def dragMoveEvent(self,e):
        pass

COMBOBOX = [["cmd1","port1"],["cmd2","port2"],["cmd3","port3"],
            ["cmd4", "port4"], ["cmd5", "port5"], ["cmd6", "port6"]]


class InformGui(QWidget,Ui_Form):
    cmd_class = dict()
    cmd_doc = dict()

    cmb = dict()
    cmb_instruction = dict()
    unit = ["", "V", "mV", "A", "mA", "Hz", "kHz", "Mhz", "dB", "S", "mS"]
    ci = CurrentItem()
    inc = Inc()
    def __init__(self,parent = None,UpdateUI=None,DeleteUI=None):
        super(InformGui,self).__init__(parent=None)
        self.UpdateUI=UpdateUI
        self.DeleteUI = DeleteUI
        self.par = parent
        self.setupUi(self)
        self.initCombBox()
        self.initTableview()
        self.initTree()
        self.bt_remove.clicked.connect(self.removeItem)
        self.bt_save.clicked.connect(self.saveScript)
        self.center()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)

    def initCombBox(self):
        self.cmb["group"] = QComboBox()
        self.cmb["group"].setEditable(True)
        self.cmb["para2"] = QComboBox()
        self.cmb["para2"].setEditable(True)
        self.cmb["unit"] = QComboBox()
        self.cmb["unit"].setEditable(True)
        self.cmb["group"].currentTextChanged.connect(self.cmbBoxChanged)
        self.cmb["para2"].currentTextChanged.connect(self.cmbBoxChanged)
        self.cmb["unit"].currentTextChanged.connect(self.cmbBoxChanged)
        for i in COMBOBOX:
            for x in i:
                self.cmb_instruction[x] = QComboBox()
                self.cmb_instruction[x].setEditable(True)
                self.cmb_instruction[x].currentTextChanged.connect(self.cmbInstructionBoxChanged)




        # a = QComboBox()
        # a.currentIndexChanged()

    def initTree(self):
        self.cmd_tree = MyQTreeWidget()
        self.cmd_tree.setHeaderLabel("CommandTree")
        self.cmd_tree.clicked.connect(self.treeclick)
        self.cmdlayout.addWidget(self.cmd_tree)
        root = QTreeWidgetItem(self.cmd_tree)
        root.setText(0, 'root')
        root.setExpanded(True)
        self.get_modules_public_methonds(Command)
        for key in self.cmd_class:
            child = QTreeWidgetItem(root)
            child.setText(0,key)
            for item in self.cmd_class[key]:
                grandchild = QTreeWidgetItem(child)
                grandchild.setText(0,item)
        # for key in self.ci.net:
        #     child = QTreeWidgetItem(root)
        #     child.setText(0,key)
        #     for item in self.ci.net[key]:
        #         grandchild = QTreeWidgetItem(child)
        #         grandchild.setText(0,self.ci.net[key][item])
        self.cmd_tree.addTopLevelItem(root)
        self.cmd_tree.setDragEnabled(True)
        # self.cmd_tree.setDefaultDropAction()
        self.cmd_tree.setAcceptDrops(True)
        self.cmd_tree.setDropIndicatorShown(True)

    def initTableview(self):
        self.tableView = MyTableView()


        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableView.setSelectionBehavior(QTableView.SelectRows)
        self.tableView.clicked.connect(self.getDetails)

        self.property_table.setRowCount(20)
        self.property_table.setColumnWidth(0,120)
        self.property_table.verticalHeader().setVisible(False)
        self.property_table.itemChanged.connect(self.propertyItemChanged)
        #self.property_table.resizeRowsToContents()
        self.property_table.horizontalHeader().setStretchLastSection(True)
        self.para_table.setRowCount(30)
        self.para_table.setColumnWidth(0, 120)
        self.para_table.verticalHeader().setVisible(False)
        #self.para_table.resizeRowsToContents()
        self.para_table.horizontalHeader().setStretchLastSection(True)
        self.para_table.itemChanged.connect(self.paraItemChanged)
        self.mainlayout.addWidget(self.tableView)
        self.tableView.mydict.connect(self.initTb)

        #Create 3 comboxs



        # self.tableView.setMouseTracking(True)
        # self.tableView.entered.connect(self.showToolTip)
        # self.tableView.setMouseTracking(True)
        # self.tableView.entered.connect(self.showToolTip)

    def initTb(self,data):
        if isinstance(data,dict):
            if isinstance(data['header'],Item):
                #column 1
                newItem = QTableWidgetItem(data['header'].group)
                self.para_table.setItem(0,0,newItem)
                newItem = QTableWidgetItem(data['header'].tid)
                self.para_table.setItem(1, 0, newItem)
                newItem = QTableWidgetItem(data['header'].dsp)
                self.para_table.setItem(2, 0, newItem)
                newItem = QTableWidgetItem(data['header'].timeout)
                self.para_table.setItem(3, 0, newItem)
                newItem = QTableWidgetItem(data['header'].unit)
                self.para_table.setItem(4, 0, newItem)
                newItem = QTableWidgetItem(data['header'].low)
                self.para_table.setItem(5, 0, newItem)
                newItem = QTableWidgetItem(data['header'].high)
                self.para_table.setItem(6, 0, newItem)

                newItem = QTableWidgetItem(data['header'].para1)
                self.property_table.setItem(0, 0, newItem)
                newItem = QTableWidgetItem(data['header'].para2)
                self.property_table.setItem(1, 0, newItem)
                newItem = QTableWidgetItem("Cmd1")
                self.property_table.setItem(2, 0, newItem)
                newItem = QTableWidgetItem("Cmd2")
                self.property_table.setItem(3, 0, newItem)
                newItem = QTableWidgetItem("Cmd3")
                self.property_table.setItem(4, 0, newItem)
                newItem = QTableWidgetItem("Cmd4")
                self.property_table.setItem(5, 0, newItem)
                newItem = QTableWidgetItem("Cmd5")
                self.property_table.setItem(6, 0, newItem)
                newItem = QTableWidgetItem("Cmd6")
                self.property_table.setItem(7, 0, newItem)

                #column 2
                self.cmb["group"].clear()
                self.cmb["group"].addItem("")
                self.cmb["group"].addItems(self.tableView.groupname)
                self.para_table.setCellWidget(0,1,self.cmb["group"])

                self.cmb["unit"].clear()
                self.cmb["unit"].addItems(self.unit)
                self.para_table.setCellWidget(4,1,self.cmb["unit"])
                self.property_table.setCellWidget(1,1,self.cmb["para2"])

                for index,item in enumerate(COMBOBOX):
                    self.cmb_instruction[item[0]].clear()
                    self.cmb_instruction[item[0]].addItem("")
                    self.cmb_instruction[item[0]].addItems(self.inc.getDetails("cmd"))
                    self.property_table.setCellWidget(2+index, 1, self.cmb_instruction[item[0]])

                    self.cmb_instruction[item[1]].clear()
                    self.cmb_instruction[item[1]].addItem("")
                    self.cmb_instruction[item[1]].addItems(self.inc.getDetails("port"))
                    self.property_table.setCellWidget(2 + index,2, self.cmb_instruction[item[1]])


                        # self.instruction[x] = QComboBox()
                        # self.instruction[x].setEditable(True)
                        # self.instruction[x].currentIndexChanged.connect(self.allComboBoxChanged)


    def cmbInstructionBoxChanged(self):
        if self.ci.isFinished():
            #self.ci.setFinishedFlag(False)
            item = self.ci.getCurrentItem()
            if item.para2 !="":
                data = []
                for i in COMBOBOX:
                    temp = {}
                    value =self.cmb_instruction[i[0]].currentText()
                    key = self.cmb_instruction[i[1]].currentText()
                    # if key=="" or value=="":
                    #     break
                    if key!="":
                        temp[key] = value
                        data.append(temp)

                self.inc.setToNetdict(item.para2,data)
            #self.ci.setFinishedFlag(True)

    def cmbBoxChanged(self):
        if self.ci.isFinished():
            #self.ci.setFinishedFlag(False)
            row = self.ci.getCurrentRow()
            item = self.ci.getCurrentItem()
            item.group=self.cmb["group"].currentText()
            item.para2 = self.cmb["para2"].currentText()
            item.unit = self.cmb["unit"].currentText()
            self.tableView.mode.mylist[row] = item
            index = self.tableView.mode.index(row, 0)
            index1 = self.tableView.mode.index(row, 11)
            self.tableView.dataChanged(index, index1)
            self.dsp_text.clear()
            self.dsp_text.append("Tid: " + item.tid)
            if item.low == "":
                self.dsp_text.append("LowLimit: " + item.low)
            else:
                self.dsp_text.append("LowLimit: " + item.low + item.unit)
            if item.high == "":
                self.dsp_text.append("UpLimit: " + item.high)
            else:
                self.dsp_text.append("UpLimit: " + item.high + item.unit)
            self.dsp_text.append("Description: " + item.dsp)
            #self.ci.setFinishedFlag(True)



    def propertyItemChanged(self):
        if self.ci.isFinished():
            #self.ci.setFinishedFlag(False)
            row = self.ci.getCurrentRow()
            item = self.ci.getCurrentItem()
            item.para1 =  self.property_table.item(0,1).text()
            self.tableView.mode.mylist[row] = item
            index = self.tableView.mode.index(row, 0)
            index1 = self.tableView.mode.index(row, 11)
            self.tableView.dataChanged(index, index1)
            #self.ci.setFinishedFlag(True)


    def paraItemChanged(self):
        if self.ci.isFinished():
            #self.ci.setFinishedFlag(False)
            row = self.ci.getCurrentRow()
            item = self.ci.getCurrentItem()
            item.tid = self.para_table.item(1, 1).text()
            item.dsp = self.para_table.item(2, 1).text()
            item.timeout = self.para_table.item(3, 1).text()
            item.low = self.para_table.item(5, 1).text()
            item.high = self.para_table.item(6, 1).text()
            self.tableView.mode.mylist[row] = item
            index = self.tableView.mode.index(row, 0)
            index1 = self.tableView.mode.index(row, 11)
            self.tableView.dataChanged(index, index1)

            self.dsp_text.clear()
            self.dsp_text.append("Tid: " + item.tid)
            if item.low == "":
                self.dsp_text.append("LowLimit: " + item.low)
            else:
                self.dsp_text.append("LowLimit: " + item.low + item.unit)
            if item.high == "":
                self.dsp_text.append("UpLimit: " + item.high)
            else:
                self.dsp_text.append("UpLimit: " + item.high + item.unit)
            self.dsp_text.append("Description: " + item.dsp)
            #self.ci.setFinishedFlag(True)

            #self.ci.inc


    def getDetails(self):
        try:
            row = self.tableView.currentIndex().row()
            #self.inc.getDetails("cmd")
            if isinstance(self.tableView.mode.mylist[row], Item):
                self.ci.setFinishedFlag(False)
                self.ci.setCurrentRow(row)
                self.ci.setCurrentItem(self.tableView.mode.mylist[row])

                item = self.ci.getCurrentItem()

                self.cmb["group"].setCurrentText(item.group)
                newItem = QTableWidgetItem(item.tid)
                self.para_table.setItem(1, 1, newItem)
                newItem = QTableWidgetItem(item.dsp)
                self.para_table.setItem(2, 1, newItem)
                newItem = QTableWidgetItem(item.timeout)
                self.para_table.setItem(3, 1, newItem)

                self.cmb["unit"].setCurrentText(item.unit)
                newItem = QTableWidgetItem(item.low)
                self.para_table.setItem(5, 1, newItem)
                newItem = QTableWidgetItem(item.high)
                self.para_table.setItem(6, 1, newItem)
                newItem = QTableWidgetItem(item.para1)
                self.property_table.setItem(0, 1, newItem)
                newItem = QTableWidgetItem(item.para2)
                self.property_table.setItem(1, 1, newItem)

                self.cmb["para2"].clear()
                self.cmb["para2"].addItem("")
                self.cmb["para2"].addItems(self.inc.getDetails("net"))
                self.cmb["para2"].setCurrentText(item.para2)

                show = self.inc.getNetFromDict(item.para2)
                if show:
                    for index, x in enumerate(show):
                        self.cmb_instruction[COMBOBOX[index][0]].setCurrentText(x.values()[0])
                        self.cmb_instruction[COMBOBOX[index][1]].setCurrentText(x.keys()[0])
                else:
                    for it in COMBOBOX:
                        self.cmb_instruction[it[0]].setCurrentText("")
                        self.cmb_instruction[it[1]].setCurrentText("")


                self.dsp_text.clear()
                self.dsp_text.append("Tid: " + item.tid)
                if item.low == "":
                    self.dsp_text.append("LowLimit: " + item.low)
                else:
                    self.dsp_text.append("LowLimit: " + item.low + item.unit)
                if item.high == "":
                    self.dsp_text.append("UpLimit: " + item.high)
                else:
                    self.dsp_text.append("UpLimit: " + item.high + item.unit)
                self.dsp_text.append("Description: " + item.dsp)

                self.ci.setFinishedFlag(True)
        except Exception:
            pass

    def treeclick(self):
        key =  self.cmd_tree.selectedItems()[0].text(0)

        if key in self.cmd_doc.get("doc"):
            self.dsp_text.clear()
            self.dsp_text.append("Function: " + key)
            self.dsp_text.append("description: " + self.cmd_doc.get("doc")[key])


    def get_modules_public_methonds(self,DM):
        methodName = dir(DM)
        func = []
        doc = {}
        for name in methodName:
            try:
                m = getattr(DM,name)
                if hasattr(m,'_rpc_public_name'):
                    func.append(name)
                    if m.__doc__:
                        doc.setdefault(name,m.__doc__)
                    else:
                        doc.setdefault(name,"")
            except:
                pass
        self.cmd_class.setdefault(DM.__name__,func)
        self.cmd_doc.setdefault("doc",doc)
        # print self.cmd_class["doc"]
        #print self.cmd_class

    def removeItem(self):
        index = self.tableView.currentIndex()
        if not index.isValid():
            return
        row = self.ci.getCurrentRow()
        item = self.ci.getCurrentItem()
        if (QMessageBox.question(self, "TestItem - Remove",
                                 "Remove GroupName:{}----TID:{}?".format(item.group,item.tid),
                                 QMessageBox.Yes | QMessageBox.No) ==
                QMessageBox.No):
            return
        self.inc.removeFromDict(item.para2)
        self.tableView.mode.removeRows(row)



    def saveScript(self):
        if (QMessageBox.question(self, "Save Script",
                                 "Are you sure to save the current Script?",
                                 QMessageBox.Yes | QMessageBox.No) ==
                QMessageBox.No):
            return

        with open(functionPath, "w") as f:
            f.write(json.dumps(self.inc.net_w, sort_keys=True, indent=4, separators=(',', ':')))


        if self.tableView.mode.mylist ==None:
            return
        print savecsvPath
        with open(savecsvPath,'w') as f:
            writer = csv.writer(f)
            head = self.tableView.mode.header
            h = [head.group,head.tid,head.dsp,head.func,head.timeout,head.para1,head.para2,head.unit,head.low,head.high,head.key,head.val]
            writer.writerow(h)
            for item in self.tableView.mode.mylist:
                data = [item.group,item.tid,item.dsp,item.func,item.timeout,item.para1,item.para2,item.unit,item.low,item.high,item.key,item.val]
                writer.writerow(data)


    #
    # def closeEvent(self, QCloseEvent):
    #     #self.saveScript()
    #     self.par.show()
    #     self.DeleteUI(3)



        #self.resizeColumns()


if __name__=='__main__':
    app = QApplication(sys.argv)
    labelDemo = InformGui()
    labelDemo.show()
    sys.exit(app.exec_())