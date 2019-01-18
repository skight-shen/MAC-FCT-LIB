# coding=utf-8

from TestUI.GUI.controller.main import UiMainWindow
from TestUI.GUI.controller.Passwd import EnterPwd
from TestUI.GUI.controller.Loop import Loop_Frame
# from TestUI.GUI.controller.ScriptEditor import InformGui
from TestUI.GUI.controller.SettingPwd import SetPwd
from PyQt5.QtCore import pyqtSignal, QObject
from Common.rpc_client import RPCClientWrapper
import zmq
import Common.zmqports as zmqports
from Common.publisher import ZmqPublisher


class GuiManager(QObject):
    """docstring for GuiManager"""
    sigOut = pyqtSignal(dict)

    def __init__(self, UpdateUI, DeleteUI):
        super(GuiManager, self).__init__()
        self.UpdateUI = UpdateUI
        self.DeleteUI = DeleteUI
        self.frameDict = {}  # used to upload the frame
        self.parent = None

        sm_proxy = RPCClientWrapper('tcp://localhost' + ':' + str(zmqports.SM_PORT),
                                    ZmqPublisher(zmq.Context().instance(),
                                                 "tcp://*:" + str(zmqports.SM_PROXY_PUB), 'SMProxy'))
        self.sm_remote = sm_proxy.remote_server()

    def GetFrame(self, tp):
        frame = self.frameDict.get(tp)
        if frame is None:
            frame = self.CreateFrame(tp)
            self.frameDict[tp] = frame
        return frame

    def CreateFrame(self, tp):
        if tp == 0:
            self.parent = UiMainWindow(parent=None, UpdateUI=self.UpdateUI, sm_remote=self.sm_remote)
            return self.parent
        elif tp == 1:
            return Loop_Frame(parent=self.parent, UpdateUI=self.UpdateUI, DeleteUI=self.DeleteUI,
                              sm_remote=self.sm_remote)
        elif tp == 2:
            return EnterPwd(parent=self.parent, UpdateUI=self.UpdateUI, DeleteUI=self.DeleteUI)
        # elif tp ==3:
        #     return InformGui(parent=self.parent,UpdateUI=self.UpdateUI,DeleteUI=self.DeleteUI)
        elif tp == 4:
            return SetPwd(parent=self.parent, UpdateUI=self.UpdateUI, DeleteUI=self.DeleteUI)

    def DeleateFrame(self, tp):
        frame = self.frameDict.get(tp)
        if frame is None:
            return None
        else:
            self.frameDict.pop(tp)
            return True
