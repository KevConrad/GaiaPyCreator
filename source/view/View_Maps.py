import PIL
import PIL.Image
import wx

from model.Model_Map import Model_Map
from model.Model_Tile import Model_Tile
from model.Model_Tilemap import Model_Tilemap
from view.View_Common import View_Common
from view.View_Tabs import TabMaps

from pubsub import pub
from PIL import Image

class View_Maps:
    MAP_IMAGE_PIXEL_HEIGHT = 400
    MAP_IMAGE_PIXEL_WIDTH = 400

    def __init__(self, frame : wx.Frame, notebook : wx.Notebook):
        self.frame = frame
        self.tabPage = notebook.GetPage(TabMaps.MAPS_TAB_INDEX)

        # maps list box
        self.listBoxMaps = wx.ListBox(self.tabPage , size = (View_Common.LISTBOX_WIDTH, View_Common.LISTBOX_HEIGHT),
                                      style = wx.LB_SINGLE|wx.LB_HSCROLL)
        self.frame.Bind(wx.EVT_LISTBOX, self.onListBox, self.listBoxMaps)

        # map image
        verticalBoxMapImage = wx.BoxSizer(wx.VERTICAL)
        labelMap = wx.StaticText(self.tabPage, label="Map:")
        self.mapImage = wx.StaticBitmap(self.tabPage, wx.ID_ANY, wx.NullBitmap,
                                            size=(self.MAP_IMAGE_PIXEL_WIDTH, self.MAP_IMAGE_PIXEL_HEIGHT))
        self.mapImage.Bind(wx.EVT_LEFT_DOWN, self.onTilemapImageClick)
        verticalBoxMapImage.Add(labelMap)
        verticalBoxMapImage.Add(self.mapImage)

        horizontalBox = wx.BoxSizer(wx.HORIZONTAL)
        horizontalBox.Add(self.listBoxMaps, 0, wx.EXPAND)
        horizontalBox.Add(verticalBoxMapImage)
        
        self.tabPage.SetSizer(horizontalBox)
        self.tabPage.Fit()

        self.frame.Show(True)

    def load(self, mapNames):
        self.listBoxMaps.Set(mapNames)

    def onListBox(self, event):
        selectedIndex = self.listBoxMaps.GetSelection()
        pub.sendMessage("maps_update", mapIndex=selectedIndex)

