import wx

from pubsub import pub

# notification
from pubsub.utils.notification import useNotifyByWriteFile
import sys

import re

useNotifyByWriteFile(sys.stdout)

class View_StatusBar(wx.Frame):
    def __init__(self, frame : wx.Frame):
        self.statusbar = frame.CreateStatusBar(1)
        self.statusbar.SetStatusText("No project loaded.")

    def pushStatus(self, message):
        self.statusbar.PushStatusText(message)