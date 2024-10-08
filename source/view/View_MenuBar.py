import wx

from pubsub import pub

# notification
from pubsub.utils.notification import useNotifyByWriteFile
import sys

useNotifyByWriteFile(sys.stdout)

class View_MenuBar:
    def __init__(self, frame : wx.Frame):
        menuBar = wx.MenuBar()

        self.frame = frame

        menuBarProject = wx.Menu()
        menuBarProjectCreate = menuBarProject.Append(wx.ID_NEW, "Create...", "Create new project.")
        menuBarProjectOpen = menuBarProject.Append(wx.ID_OPEN, "Open...", "Open existing project.")
        menuBarProjectClose = menuBarProject.Append(wx.ID_CLOSE, "Close", "Close project.")

        frame.Bind(wx.EVT_MENU, self.closeProject, menuBarProjectClose)
        frame.Bind(wx.EVT_MENU, self.createProject, menuBarProjectCreate)
        frame.Bind(wx.EVT_MENU, self.openProject, menuBarProjectOpen)
        menuBar.Append(menuBarProject, "Project")

        frame.SetMenuBar(menuBar)

    def closeProject(self, parent=None):
        pub.sendMessage("project_close")

    def createProject(self, parent=None):
        defDir = ""

        dialog = wx.FileDialog(self.frame,
                               'Open ROM File',
                               defDir,
                               wildcard = "Illusion of Gaia ROM file (*.sfc)|*.sfc|Illusion of Gaia ROM file (*.smc)|*.smc",
                               style=wx.FD_OPEN)

        if dialog.ShowModal() == wx.ID_OK:
            self.romPath = dialog.GetPath()
            
            pub.sendMessage("rom_opened", romPath=self.romPath)

            dialog = wx.FileDialog(self.frame,
                                   'Save project File',
                                   defDir,
                                   wildcard = "GaiaTheCreator project file (*.json)|*.json",
                                   style=wx.FD_SAVE)
            
            if dialog.ShowModal() == wx.ID_OK:
                self.projectPath = dialog.GetPath()

                pub.sendMessage("project_save", projectPath=self.projectPath)
        return

    def openProject(self, parent=None):
        defDir = ""

        dialog = wx.FileDialog(self.frame,
                               'Open Project File',
                               defDir,
                               wildcard = "GaiaTheCreator project file (*.json)|*.json",
                               style=wx.FD_OPEN)
        
        if dialog.ShowModal() == wx.ID_OK:
            self.projectPath = dialog.GetPath()

            pub.sendMessage("project_open", projectPath=self.projectPath)

        return

