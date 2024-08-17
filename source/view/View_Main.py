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
from .View_Tilesets import View_Tilesets

class View_Main(wx.Frame):
    def __init__(self, parent=None) -> None:
        wx.Frame.__init__(self, parent, -1, "GaiaTheCreator", size=(800, 600))
        
        self.menuBar = View_MenuBar(self)
        self.statusBar = View_StatusBar(self)
        self.tabs = View_Tabs(self)
        self.items = View_Items(self, self.tabs.notebook)
        self.tilesets = View_Tilesets(self, self.tabs.notebook)

        #pub.subscribe(self.updateProgressBar, "progressBar_update")

    def initProgressBar(self, message):
        #self.progressDialog = wx.ProgressDialog("LoadProject", message, maximum=100, parent=None,
        #                                        style=wx.PD_APP_MODAL|wx.PD_AUTO_HIDE)
        pass

    def updateProgressBar(self, updateValue):
        print("Progress: " + str(updateValue))
        #self.progressDialog.Update(value = updateValue)
        


