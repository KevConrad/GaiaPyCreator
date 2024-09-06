import wx

from pubsub import pub

# notification
from pubsub.utils.notification import useNotifyByWriteFile
import sys

useNotifyByWriteFile(sys.stdout)

from .View_MenuBar import View_MenuBar
from .View_StatusBar import View_StatusBar
from .View_Tabs import View_Tabs
from .View_Items import View_Items
from .View_Tilemaps import View_Tilemaps
from .View_Tilesets import View_Tilesets

class View_Main(wx.Frame):
    def __init__(self, parent=None) -> None:
        wx.Frame.__init__(self, parent, -1, "GaiaTheCreator", size=(1000, 600))
        
        self.menuBar = View_MenuBar(self)
        self.statusBar = View_StatusBar(self)
        self.tabs = View_Tabs(self)
        self.items = View_Items(self, self.tabs.notebook)
        self.tilemaps = View_Tilemaps(self, self.tabs.notebook)
        self.tilesets = View_Tilesets(self, self.tabs.notebook)

