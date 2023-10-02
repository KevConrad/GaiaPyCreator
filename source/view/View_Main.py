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


