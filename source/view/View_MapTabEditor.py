# This file contains the class View_MapTabEditor, which is a panel that allows the user to edit the map.
# This class is responsible for displaying the map editor.
import PIL
import PIL.Image
import wx

from model.Model_Map import Model_Map
from model.Model_Tilemap import Model_Tilemap

from PIL import Image
from pubsub import pub

class View_MapTabEditor(wx.Panel):

    TILEMAP_IMAGE_PIXEL_HEIGHT = 300
    TILEMAP_IMAGE_PIXEL_WIDTH = 300

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        
        # map layer selection radio buttons
        self.radioButtonLayer0 = wx.RadioButton(self, label="BG1 Layer", style=wx.RB_GROUP)
        self.radioButtonLayer1 = wx.RadioButton(self, label="BG2 Layer")
        # bind function if map layer selection changed
        self.radioButtonLayer0.Bind(wx.EVT_RADIOBUTTON, self.onMapLayerSelectionChanged)
        self.radioButtonLayer1.Bind(wx.EVT_RADIOBUTTON, self.onMapLayerSelectionChanged)
        self.radioButtonLayer0.SetValue(True)
        self.selectedMapLayerIndex = 0

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
        self.comboBoxMapTilemap = wx.ComboBox(self, size=(256, 16), style=wx.CB_DROPDOWN|wx.CB_READONLY)
        horizontalBoxMapTilemap = wx.BoxSizer(wx.HORIZONTAL)
        horizontalBoxMapTilemap.Add(labelMapTilemap, flag=wx.ALIGN_LEFT|wx.ALL)
        horizontalBoxMapTilemap.Add(self.comboBoxMapTilemap, flag=wx.ALIGN_LEFT|wx.ALL)

        # map tilemap image
        verticalBoxTilemapImage = wx.BoxSizer(wx.VERTICAL)
        self.tilemapImage = wx.StaticBitmap(self, wx.ID_ANY, wx.NullBitmap,
                                            size=(self.TILEMAP_IMAGE_PIXEL_WIDTH, self.TILEMAP_IMAGE_PIXEL_HEIGHT))
        # bind function if mouse cursor over tilemap image
        self.tilemapImage.Bind(wx.EVT_MOTION, self.onMouseMoveOverTilemapImage)
        # bind function if mouse cursor over tilemap image and left button pressed
        self.tilemapImage.Bind(wx.EVT_LEFT_DOWN, self.onTilemapImageClick)

        # map data
        self.verticalBoxMapData = wx.BoxSizer(wx.VERTICAL)
        self.verticalBoxMapData.Add(horizontalBoxLayerSelection)
        self.verticalBoxMapData.Add(horizontalBoxMapSizeX)
        self.verticalBoxMapData.Add(horizontalBoxMapSizeY)
        self.verticalBoxMapData.Add(horizontalBoxMapTilemap)
        self.verticalBoxMapData.Add(self.tilemapImage, flag=wx.ALIGN_LEFT|wx.ALL)
        self.verticalBoxMapData.AddStretchSpacer(1)
        self.SetSizer(self.verticalBoxMapData)
        self.Fit()

        self.selectedTileIndex = 0
        self.tilemapSelectedPositionX = 0
        self.tilemapSelectedPositionY = 0

    def load(self, tilemapNames : list):
        self.comboBoxMapTilemap.Set(tilemapNames)

    def onMapLayerSelectionChanged(self, event):
        if self.radioButtonLayer0.GetValue() == True:
            self.selectedMapLayerIndex = 0
        else:
            self.selectedMapLayerIndex = 1

        self.update(self.mapData)

    def onMouseMoveOverTilemapImage(self, event):
        x, y = event.GetPosition()
        tilemapCurrentPositionX = int(x / (self.TILEMAP_IMAGE_PIXEL_WIDTH / Model_Tilemap.TILEMAP_TILE_WIDTH))
        tilemapCurrentPositionY = int(y / (self.TILEMAP_IMAGE_PIXEL_HEIGHT / Model_Tilemap.TILEMAP_TILE_HEIGHT))
        pub.sendMessage("maps_update_tilemapImage", mapLayerIndex=self.selectedMapLayerIndex, currentPositionX=tilemapCurrentPositionX, currentPositionY=tilemapCurrentPositionY,
                        selectedPositionX=self.tilemapSelectedPositionX, selectedPositionY=self.tilemapSelectedPositionY)

    def onTilemapImageClick(self, event):
        x, y = event.GetPosition()
        self.tilemapSelectedPositionX = int(x / (self.TILEMAP_IMAGE_PIXEL_WIDTH / Model_Tilemap.TILEMAP_TILE_WIDTH))
        self.tilemapSelectedPositionY = int(y / (self.TILEMAP_IMAGE_PIXEL_HEIGHT / Model_Tilemap.TILEMAP_TILE_HEIGHT))
        self.selectedTileIndex = (self.tilemapSelectedPositionY * Model_Tilemap.TILEMAP_TILE_WIDTH) + self.tilemapSelectedPositionX

        pub.sendMessage("maps_update_tilemapImage", mapLayerIndex=self.selectedMapLayerIndex, currentPositionX=self.tilemapSelectedPositionX, currentPositionY=self.tilemapSelectedPositionY,
                        selectedPositionX=self.tilemapSelectedPositionX, selectedPositionY=self.tilemapSelectedPositionY)
        
    def update(self, mapData : Model_Map):
        self.mapData = mapData

        if len(mapData.mapDataTilemap) >= 2:
            self.radioButtonLayer1.Enable()
        else:
            self.selectedMapLayerIndex = 0
            self.radioButtonLayer0.SetValue(True)
            self.radioButtonLayer1.SetValue(False)
            self.radioButtonLayer1.Disable()

        self.spinCtrlMapSizeX.SetValue(mapData.sizeX)
        self.spinCtrlMapSizeY.SetValue(mapData.sizeY)
        self.comboBoxMapTilemap.SetSelection(mapData.mapDataTilemap[self.selectedMapLayerIndex].index)

        self.tilemapSelectedPositionX = 0
        self.tilemapSelectedPositionY = 0

        pub.sendMessage("maps_update_tilemapImage", mapLayerIndex=self.selectedMapLayerIndex, currentPositionX=0, currentPositionY=0,
                        selectedPositionX=self.tilemapSelectedPositionX, selectedPositionY=self.tilemapSelectedPositionY)

    def updateTilemapImage(self, tilemapImage : PIL.Image):
        sizedImage = tilemapImage.resize((self.TILEMAP_IMAGE_PIXEL_WIDTH, self.TILEMAP_IMAGE_PIXEL_HEIGHT), Image.NEAREST)
        wx_image = wx.EmptyImage(sizedImage.size[0], sizedImage.size[1])
        wx_image.SetData(sizedImage.convert("RGB").tobytes())
        bitmap = wx.BitmapFromImage(wx_image)
        self.tilemapImage.SetBitmap(bitmap)