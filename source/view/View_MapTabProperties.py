# This file contains the View_MapTabProperties class, which is a panel that contains the properties of the map.
# This class is responsible for displaying the properties of the selected map.
import wx

from model.Model_Map import Model_Map

class View_MapTabProperties(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        # map name controls
        self.labelName = wx.StaticText(self, label="Name:")
        self.textCtrlName = wx.TextCtrl(self, value="", size=(200, 24))
        horizontalBoxName = wx.BoxSizer(wx.HORIZONTAL)
        horizontalBoxName.Add(self.labelName, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,)
        horizontalBoxName.Add(self.textCtrlName, wx.EXPAND|wx.ALL)

        # map size X controls
        horizontalBoxMapSizeX = wx.BoxSizer(wx.HORIZONTAL)
        labelMapSizeX = wx.StaticText(self, label="Size X: ")
        self.spinCtrlMapSizeX = wx.SpinCtrl(self, style=wx.SP_ARROW_KEYS)
        self.spinCtrlMapSizeX.SetMin(0)
        self.spinCtrlMapSizeX.SetMax(1024)
        horizontalBoxMapSizeX.Add(labelMapSizeX, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        horizontalBoxMapSizeX.Add(self.spinCtrlMapSizeX, wx.EXPAND|wx.ALL)

        # map size Y controls
        horizontalBoxMapSizeY = wx.BoxSizer(wx.HORIZONTAL)
        labelMapSizeY = wx.StaticText(self, label="Size Y: ")
        self.spinCtrlMapSizeY = wx.SpinCtrl(self, style=wx.SP_ARROW_KEYS)
        self.spinCtrlMapSizeY.SetMin(0)
        self.spinCtrlMapSizeY.SetMax(1024)
        horizontalBoxMapSizeY.Add(labelMapSizeY, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        horizontalBoxMapSizeY.Add(self.spinCtrlMapSizeY, wx.EXPAND|wx.ALL)

        # map data
        self.verticalBoxMapData = wx.BoxSizer(wx.VERTICAL)
        labelMapData = wx.StaticText(self, label="Map Data:")
        self.verticalBoxMapData.Add(labelMapData)
        self.verticalBoxMapData.Add(horizontalBoxName)
        self.verticalBoxMapData.Add(horizontalBoxMapSizeX)
        self.verticalBoxMapData.Add(horizontalBoxMapSizeY)

        self.SetSizer(self.verticalBoxMapData)
        self.Fit()
    
    def update(self, mapData : Model_Map):
        self.textCtrlName.SetValue(mapData.events.displayedName)
        self.spinCtrlMapSizeX.SetValue(mapData.sizeX)
        self.spinCtrlMapSizeY.SetValue(mapData.sizeY)
