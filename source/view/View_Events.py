import wx

from view.View_Common import View_Common
from view.View_Tabs import TabEvents

class View_Events:
    def __init__(self, frame : wx.Frame, notebook : wx.Notebook):
        self.frame = frame
        self.tabPage = notebook.GetPage(TabEvents.EVENTS_TAB_INDEX)

        # events list box
        self.listBoxEvents = wx.ListBox(self.tabPage , size = (View_Common.LISTBOX_WIDTH, View_Common.LISTBOX_HEIGHT),
                                        style = wx.LB_SINGLE|wx.LB_HSCROLL)
        self.frame.Bind(wx.EVT_LISTBOX, self.onListBoxEvents, self.listBoxEvents)

        verticalBoxSpritesets = wx.BoxSizer(wx.VERTICAL)
        verticalBoxSpritesets.Add(self.listBoxEvents, 0, wx.EXPAND)
        
        horizontalBox = wx.BoxSizer(wx.HORIZONTAL)
        horizontalBox.Add(verticalBoxSpritesets, 0, wx.EXPAND)
        horizontalBox.AddSpacer(10)
        
        self.tabPage.SetSizer(horizontalBox)
        self.tabPage.Fit()

        self.frame.Show(True)

    def load(self, eventAddressList):
        self.eventNames = []
        for eventAddress in eventAddressList:
            eventName = "Event at 0x{:04X}".format(eventAddress)
            self.eventNames.append(eventName)
        self.listBoxEvents.Set(self.eventNames)

    def onListBoxEvents(self, event):
        selectedIndex = self.listBoxEvents.GetSelection()
