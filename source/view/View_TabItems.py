import wx

class View_TabItems:
    def __init__(self, frame : wx.Frame, notebook : wx.Notebook):

        box = wx.BoxSizer(wx.HORIZONTAL)

        tabPage = notebook.GetPage(1)

        self.text = wx.TextCtrl(tabPage, style = wx.TE_MULTILINE) 
         
        languages = ['C', 'C++', 'Java', 'Python', 'Perl', 'JavaScript', 'PHP', 'VB.NET','C#']   
        lst = wx.ListBox(tabPage , size = (100,-1), choices = languages, style = wx.LB_SINGLE)
		
        box.Add(lst,0,wx.EXPAND) 
        box.Add(self.text, 1, wx.EXPAND) 
		
        tabPage.SetSizer(box) 
        tabPage.Fit() 
		
        frame.Centre() 
        frame.Bind(wx.EVT_LISTBOX, self.onListBox, lst) 
        frame.Show(True)

    def onListBox(self, event): 
        self.text.AppendText( "Current selection: "+event.GetEventObject().GetStringSelection()+"\n")