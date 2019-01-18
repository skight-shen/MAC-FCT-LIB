import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QGridLayout, QPushButton, QMessageBox
from mainWindow import Ui_MainWindow
#from ingenuity.GUI.model.Treemodel import TreeModel


class MyApp(QMainWindow, Ui_MainWindow):
    def __init__(self, sm_remote=None):
        super(MyApp, self).__init__()
        self.setupUi(self)
        self.gridLayout_5 = QGridLayout(self.tab_failureOverview)
        self.gridLayout.setObjectName("gridLayout_5")
        self.gridLayout_5.addWidget(self.tableview_failure, 0, 0, 1, 1)

        # self.mymodule = TreeModel()
        # self.tableview_test.setModel(self.mymodule)
        # #self.tableview_test.header().setStyleSheet(header)
        # self.tableview_test.verticalScrollBar().setStyleSheet(verticalscrollbar)
        # self.tableview_test.horizontalScrollBar().setStyleSheet(verticalscrollbar)
        #
        # # self.mydelegate = TreeViewDelegate()
        # # self.treeView.setItemDelegate(self.mydelegate)
        # self.tableview_test.setAlternatingRowColors(True)
        # self.tableview_test.setStyleSheet(qssTree)


        self.bt_start.clicked.connect(self.startButton)
        self.bt_abort.clicked.connect(self.abortButton)
        self.bt_loop.clicked.connect(self.loopButton)

    def startButton(self):
        QMessageBox.information(None, "Title", "Content", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        return

    def abortButton(self):
        return

    def loopButton(self):
        return

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
