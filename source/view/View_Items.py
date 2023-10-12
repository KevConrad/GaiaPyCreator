import wx

class View_Items:
    def __init__(self, frame : wx.Frame, notebook : wx.Notebook):
        self.frame = frame
        self.tabPage = notebook.GetPage(1)

    def load(self):
        box = wx.BoxSizer(wx.HORIZONTAL)
        self.text = wx.TextCtrl(self.tabPage, style = wx.TE_MULTILINE) 
         
        languages = ['C', 'C++', 'Java', 'Python', 'Perl', 'JavaScript', 'PHP', 'VB.NET','C#']   
        lst = wx.ListBox(self.tabPage , size = (100,-1), choices = languages, style = wx.LB_SINGLE)
		
        box.Add(lst,0,wx.EXPAND) 
        box.Add(self.text, 1, wx.EXPAND) 
		
        self.tabPage.SetSizer(box) 
        self.tabPage.Fit() 
		
        self.frame.Bind(wx.EVT_LISTBOX, self.onListBox, lst) 
        self.frame.Show(True)

    def onListBox(self, event): 
        self.text.AppendText( "Current selection: "+event.GetEventObject().GetStringSelection()+"\n")