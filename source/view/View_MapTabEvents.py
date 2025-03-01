# This file contains the View_MapTabEvents class, which is a panel that is displayed in the notebook of the main window. It allows the user to edit the event data of the map.
# This class is responsible for displaying the event data of the selected map.
import wx
import wx.lib.scrolledpanel

from model.Model_Map import Model_Map

class View_MapTabEvents(wx.Panel):
    EVENTS_TAB_INDEX = 1

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        text = wx.StaticText(self, -1, "Edit map event data.", (20,20))
