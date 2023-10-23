import wx

class View_Items:
    def __init__(self, frame : wx.Frame, notebook : wx.Notebook):
        self.frame = frame
        self.tabPage = notebook.GetPage(1)

    def load(self, itemNames):
        box = wx.BoxSizer(wx.HORIZONTAL)
        self.text = wx.TextCtrl(self.tabPage, style = wx.TE_MULTILINE) 
        
        listBoxItems = wx.ListBox(self.tabPage , size = (200,500), choices = itemNames, style = wx.LB_SINGLE)
		
        box.Add(listBoxItems, 0, wx.EXPAND) 
        box.Add(self.text, 1, wx.EXPAND) 
		
        self.tabPage.SetSizer(box) 
        self.tabPage.Fit() 
		
        self.frame.Bind(wx.EVT_LISTBOX, self.onListBox, listBoxItems) 
        self.frame.Show(True)

    def onListBox(self, event): 
        self.text.AppendText( "Current selection: "+event.GetEventObject().GetStringSelection()+"\n")