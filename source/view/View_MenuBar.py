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
        menuBarProjectCreate = menuBarProject.Append(wx.ID_NEW, "Create", "Create new project.")
        frame.Bind(wx.EVT_MENU, self.createNewProject, menuBarProjectCreate)
        menuBar.Append(menuBarProject, "Project")

        frame.SetMenuBar(menuBar)

    def createNewProject(self, parent=None):
        defDir = ""
        defFile = u""

        dialog = wx.FileDialog(self.frame,
                                'Open ROM File',
                                defDir, defFile,
                                'Illusion of Gaia ROM file (*.sfc)|*.sfc',
                                style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        dialog.ShowModal()
        
        return

    def openProject():
        filetypes = (
            ('GaiaTheCreator project file', '*.gtc'),
        )

        filename = fd.askopenfilename(
            title='Open GaiaTheCreator project file',
            initialdir='/',
            filetypes=filetypes)
        return

