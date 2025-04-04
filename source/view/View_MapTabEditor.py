# This file contains the class View_MapTabEditor, which is a panel that allows the user to edit the map.
# This class is responsible for displaying the map editor.
import wx

from model.Model_Map import Model_Map

class View_MapTabEditor(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        
        # map layer selection radio buttons
        self.radioButtonLayer0 = wx.RadioButton(self, label="BG1 Layer", style=wx.RB_GROUP)
        self.radioButtonLayer1 = wx.RadioButton(self, label="BG2 Layer")
        # map layer selection sizer
        horizontalBoxLayerSelection = wx.BoxSizer(wx.HORIZONTAL)
        horizontalBoxLayerSelection.Add(self.radioButtonLayer0, flag=wx.ALIGN_LEFT|wx.ALL)
        horizontalBoxLayerSelection.Add(self.radioButtonLayer1, flag=wx.ALIGN_LEFT|wx.ALL)

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

        # map tilemap combo box
        labelMapTilemap = wx.StaticText(self, label="Tilemap:")
        self.comboBoxMapTilemap = wx.ComboBox(self, style=wx.CB_DROPDOWN|wx.CB_READONLY)
        horizontalBoxMapTilemap = wx.BoxSizer(wx.HORIZONTAL)
        horizontalBoxMapTilemap.Add(labelMapTilemap, flag=wx.ALIGN_LEFT|wx.ALL)
        horizontalBoxMapTilemap.Add(self.comboBoxMapTilemap, flag=wx.ALIGN_LEFT|wx.ALL)

        # map data
        self.verticalBoxMapData = wx.BoxSizer(wx.VERTICAL)
        labelMapData = wx.StaticText(self, label="Map Data:")
        self.verticalBoxMapData.Add(labelMapData)
        self.verticalBoxMapData.Add(horizontalBoxLayerSelection)
        self.verticalBoxMapData.Add(horizontalBoxMapSizeX)
        self.verticalBoxMapData.Add(horizontalBoxMapSizeY)
        self.verticalBoxMapData.Add(horizontalBoxMapTilemap)
        self.verticalBoxMapData.AddStretchSpacer(1)
        self.SetSizer(self.verticalBoxMapData)
        self.Fit()

    def load(self, tilemapNames : list):
        self.comboBoxMapTilemap.Set(tilemapNames)

    def update(self, mapData : Model_Map):
        self.spinCtrlMapSizeX.SetValue(mapData.sizeX)
        self.spinCtrlMapSizeY.SetValue(mapData.sizeY)
        self.comboBoxMapTilemap.SetSelection(mapData.mapDataTilemap[0].index)