# This file contains the class that represents the tab for editing map treasures.
# This class is responsible for displaying the treasure data of the selected map.
import wx
import wx.lib.scrolledpanel

from model.Model_Map import Model_Map

class View_MapTabTreasures(wx.Panel):
    SPRITES_TAB_INDEX = 2

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        text = wx.StaticText(self, -1, "Edit map treasure data.", (20,20))
