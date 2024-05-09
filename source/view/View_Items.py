import wx

class View_Items:
    def __init__(self, frame : wx.Frame, notebook : wx.Notebook):
        self.frame = frame
        self.tabPage = notebook.GetPage(1)

        self.textCtrlItemName = wx.TextCtrl(self.tabPage, pos = (200, 0), value="", size=(128, 24), style=wx.TE_READONLY)
        self.listBoxItems = wx.ListBox(self.tabPage , size = (200,500), style = wx.LB_SINGLE)

        horizontalBox = wx.BoxSizer(wx.HORIZONTAL)
        horizontalBox.Add(self.listBoxItems, 0, wx.EXPAND)
        
        verticalBox = wx.BoxSizer(wx.VERTICAL) 
        verticalBox.Add(self.textCtrlItemName, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5)
        horizontalBox.Add(verticalBox)
        
        self.tabPage.SetSizer(horizontalBox) 
        self.tabPage.Fit() 

        self.frame.Bind(wx.EVT_LISTBOX, self.onListBox, self.listBoxItems) 
        self.frame.Show(True)

    def load(self, itemNames):
        self.listBoxItems.Set(itemNames)
        self.textCtrlItemName.Value = ""

    def onListBox(self, event):
        self.textCtrlItemName.Value = event.GetEventObject().GetStringSelection()