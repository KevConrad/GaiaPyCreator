import wx

from pubsub import pub

# notification
from pubsub.utils.notification import useNotifyByWriteFile
import sys

useNotifyByWriteFile(sys.stdout)

from .View_MenuBar import View_MenuBar

class View_Main(wx.Frame):
    def __init__(self, parent=None) -> None:
        wx.Frame.__init__(self, parent, -1, "GaiaTheCreator")
        
        menuBar = View_MenuBar(self)

        sizer = wx.BoxSizer(wx.VERTICAL)
        text = wx.StaticText(self, -1, "My Money")
        ctrl = wx.TextCtrl(self, -1, "")
        sizer.Add(text, 0, wx.EXPAND | wx.ALL)
        sizer.Add(ctrl, 0, wx.EXPAND | wx.ALL)

        self.moneyCtrl = ctrl
        ctrl.SetEditable(False)
        self.SetSizer(sizer)


