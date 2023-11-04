import wx

class View_Items:
    def __init__(self, frame : wx.Frame, notebook : wx.Notebook):
        self.frame = frame
        self.tabPage = notebook.GetPage(1)

    def load(self, itemNames):
        horizontalBox = wx.BoxSizer(wx.HORIZONTAL)
        verticalBox = wx.BoxSizer(wx.VERTICAL) 

        self.listBoxItems = wx.ListBox(self.tabPage , size = (200,500), choices = itemNames, style = wx.LB_SINGLE)
        horizontalBox.Add(self.listBoxItems, 0, wx.EXPAND)
        
        self.textCtrlItemName = wx.TextCtrl(self.tabPage, pos = (200, 0), value="Test", size=(128, 24)) 
        verticalBox.Add(self.textCtrlItemName, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5)

        horizontalBox.Add(verticalBox)
		
        self.tabPage.SetSizer(horizontalBox) 
        self.tabPage.Fit() 

        self.frame.Bind(wx.EVT_LISTBOX, self.onListBox, self.listBoxItems) 
        self.frame.Show(True)

    def onListBox(self, event): 
        self.textCtrlItemName.Value = event.GetEventObject().GetStringSelection()