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

        pub.subscribe(self.pushProjectLoaded, "project_loaded")
        pub.subscribe(self.pushRomLoaded, "rom_opened")

    def pushProjectLoaded(self, projectPath):
        projectName = re.search('/(.+?).gtc', projectPath)
        self.statusbar.PushStatusText("Loaded project " + projectName + ".")

    def pushRomLoaded(self, romPath):
        print("Loaded ROM file")
        self.statusbar.PushStatusText("Loaded ROM file.")