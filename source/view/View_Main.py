import wx

from pubsub import pub

# notification
from pubsub.utils.notification import useNotifyByWriteFile
import sys

useNotifyByWriteFile(sys.stdout)

from .View_MenuBar import View_MenuBar
from .View_StatusBar import View_StatusBar
from .View_Tabs import View_Tabs
from .View_TabItems import View_TabItems

class View_Main(wx.Frame):
    def __init__(self, parent=None) -> None:
        wx.Frame.__init__(self, parent, -1, "GaiaTheCreator", size=(800, 600))
        
        self.menuBar = View_MenuBar(self)
        self.statusBar = View_StatusBar(self)
        self.tabs = View_Tabs(self)
        self.tabItems = View_TabItems(self, self.tabs.notebook)


