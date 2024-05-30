import wx

from view.View_Common import View_Common

class View_Tilesets:
    def __init__(self, frame : wx.Frame, notebook : wx.Notebook):
        self.frame = frame
        self.tabPage = notebook.GetPage(9)

        self.listBoxTilesets = wx.ListBox(self.tabPage , size = (View_Common.LISTBOX_WIDTH, View_Common.LISTBOX_HEIGHT),
                                          style = wx.LB_SINGLE|wx.LB_HSCROLL)
        horizontalBox = wx.BoxSizer(wx.HORIZONTAL)
        horizontalBox.Add(self.listBoxTilesets, 0, wx.EXPAND)
        
        self.tabPage.SetSizer(horizontalBox) 
        self.tabPage.Fit() 

        self.frame.Bind(wx.EVT_LISTBOX, self.onListBox, self.listBoxTilesets) 
        self.frame.Show(True)

    def load(self, tilesetNames):
        self.listBoxTilesets.Set(tilesetNames)

    def onListBox(self, event):
        selectedIndex = self.listBoxTilesets.GetSelection()