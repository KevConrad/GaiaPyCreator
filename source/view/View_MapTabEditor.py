# This file contains the class View_MapTabEditor, which is a panel that allows the user to edit the map.
# This class is responsible for displaying the map editor.
import wx

from model.Model_Map import Model_Map

class View_MapTabEditor(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        text = wx.StaticText(self, -1, "Edit map.", (20,20))
