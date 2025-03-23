# This file contains the class that represents the tab for editing map sprites.
# This class is responsible for displaying the sprite data of the selected map.
import wx

from model.Model_Map import Model_Map

class View_MapTabSprites(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        text = wx.StaticText(self, -1, "Edit map sprite data.", (20,20))
