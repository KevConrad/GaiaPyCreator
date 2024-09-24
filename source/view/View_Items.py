import wx

from view.View_Common import View_Common
from view.View_Tabs import TabItems

class View_Items:
    def __init__(self, frame : wx.Frame, notebook : wx.Notebook):
        self.frame = frame
        self.tabPage = notebook.GetPage(TabItems.ITEMS_TAB_INDEX)

        self.labelItemName = wx.StaticText(self.tabPage, label="Name:")
        self.textCtrlItemName = wx.TextCtrl(self.tabPage, value="", size=(200, 24))
        horizontalBoxItemName = wx.BoxSizer(wx.HORIZONTAL)
        horizontalBoxItemName.Add(self.labelItemName, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,)
        horizontalBoxItemName.Add(self.textCtrlItemName, wx.EXPAND|wx.ALL)

        self.labelItemDescription = wx.StaticText(self.tabPage, label="Description:")
        self.textCtrlItemDescription = wx.TextCtrl(self.tabPage, value="", size=(200, 80), style=wx.TE_MULTILINE)
        horizontalBoxItemDescription = wx.BoxSizer(wx.HORIZONTAL)
        horizontalBoxItemDescription.Add(self.labelItemDescription, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,)
        horizontalBoxItemDescription.Add(self.textCtrlItemDescription, wx.EXPAND|wx.ALL)

        self.labelItemIsRemovable = wx.StaticText(self.tabPage, label="Removable:")
        self.checkBoxItemIsRemovable = wx.CheckBox(self.tabPage)
        horizontalBoxItemIsRemovable = wx.BoxSizer(wx.HORIZONTAL)
        horizontalBoxItemIsRemovable.Add(self.labelItemIsRemovable, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        horizontalBoxItemIsRemovable.Add(self.checkBoxItemIsRemovable, wx.EXPAND|wx.ALL)

        self.labelItemFindMessage = wx.StaticText(self.tabPage, label="Find Message:")
        self.textCtrlItemFindMessage = wx.TextCtrl(self.tabPage, value="", size=(200, 80), style=wx.TE_MULTILINE)
        horizontalBoxItemFindMessage = wx.BoxSizer(wx.HORIZONTAL)
        horizontalBoxItemFindMessage.Add(self.labelItemFindMessage, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,)
        horizontalBoxItemFindMessage.Add(self.textCtrlItemFindMessage, wx.EXPAND|wx.ALL)

        verticalBoxItemData = wx.BoxSizer(wx.VERTICAL)
        verticalBoxItemData.Add(horizontalBoxItemName)
        verticalBoxItemData.Add(horizontalBoxItemDescription)
        verticalBoxItemData.Add(horizontalBoxItemIsRemovable)
        verticalBoxItemData.Add(horizontalBoxItemFindMessage)

        self.listBoxItems = wx.ListBox(self.tabPage , size = (View_Common.LISTBOX_WIDTH, View_Common.LISTBOX_HEIGHT),
                                       style = wx.LB_SINGLE|wx.LB_HSCROLL)
        horizontalBox = wx.BoxSizer(wx.HORIZONTAL)
        horizontalBox.Add(self.listBoxItems, 0, wx.EXPAND)
        
        horizontalBox.Add(verticalBoxItemData)
        
        self.tabPage.SetSizer(horizontalBox) 
        self.tabPage.Fit() 

        self.frame.Bind(wx.EVT_LISTBOX, self.onListBox, self.listBoxItems) 
        self.frame.Show(True)

    def load(self, itemNames, itemDescriptions, itemRemovableFlags, itemFindMessages):
        self.listBoxItems.Set(itemNames)
        self.textCtrlItemName.Value = ""
        self.itemDescriptions = itemDescriptions
        self.itemRemovableFlags = itemRemovableFlags
        self.itemFindMessages = itemFindMessages

    def onListBox(self, event):
        selectedIndex = self.listBoxItems.GetSelection()
        self.textCtrlItemName.Value = event.GetEventObject().GetStringSelection()
        self.textCtrlItemDescription.Value = self.itemDescriptions[selectedIndex]
        self.checkBoxItemIsRemovable.SetValue(self.itemRemovableFlags[selectedIndex])
        self.textCtrlItemFindMessage.Value = self.itemFindMessages[selectedIndex]