import PIL
import PIL.Image
import wx

from model.Model_Tilemap import Model_Tilemap
from view.View_Common import View_Common
from view.View_Tabs import TabTilemaps

from pubsub import pub
from PIL import Image

class View_Tilemaps:
    TILEMAP_IMAGE_PIXEL_HEIGHT = 400
    TILEMAP_IMAGE_PIXEL_WIDTH = 400

    TILE_IMAGE_PIXEL_HEIGHT = 100
    TILE_IMAGE_PIXEL_WIDTH = 100

    def __init__(self, frame : wx.Frame, notebook : wx.Notebook):
        self.frame = frame
        self.tabPage = notebook.GetPage(TabTilemaps.TILEMAP_TAB_INDEX)

        # tilemaps list box
        self.listBoxTilemaps = wx.ListBox(self.tabPage , size = (View_Common.LISTBOX_WIDTH, View_Common.LISTBOX_HEIGHT),
                                          style = wx.LB_SINGLE|wx.LB_HSCROLL)
        self.frame.Bind(wx.EVT_LISTBOX, self.onListBox, self.listBoxTilemaps)

        # tilemap image
        verticalBoxTilemapImage = wx.BoxSizer(wx.VERTICAL)
        labelTilemap = wx.StaticText(self.tabPage, label="Tilemap:")
        self.tilemapImage = wx.StaticBitmap(self.tabPage, wx.ID_ANY, wx.NullBitmap, size=(400, 400))
        self.tilemapImage.Bind(wx.EVT_LEFT_DOWN, self.onTilemapImageClick)
        
        verticalBoxTilemapImage.Add(labelTilemap)
        verticalBoxTilemapImage.Add(self.tilemapImage)

        # tile image
        verticalBoxTileImage = wx.BoxSizer(wx.VERTICAL)
        labelTile = wx.StaticText(self.tabPage, label="Tile:")
        self.tileImage = wx.StaticBitmap(self.tabPage, wx.ID_ANY, wx.NullBitmap, size=(100, 100))
        self.tileImage.Bind(wx.EVT_LEFT_DOWN, self.onTileImageClick)

        verticalBoxTileImage.Add(labelTile)
        verticalBoxTileImage.Add(self.tileImage)

        # mirror horizontal checkbox
        horizontalBoxMirrorHorizontal = wx.BoxSizer(wx.HORIZONTAL)
        labelMirrorHorizontal = wx.StaticText(self.tabPage, label="Mirror Horizontal: ")
        checkBoxMirrorHorizontal = wx.CheckBox(self.tabPage)
        horizontalBoxMirrorHorizontal.Add(labelMirrorHorizontal, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        horizontalBoxMirrorHorizontal.Add(checkBoxMirrorHorizontal, wx.EXPAND|wx.ALL)
        
        # mirror vertical checkbox
        horizontalBoxMirrorVertical = wx.BoxSizer(wx.HORIZONTAL)
        labelMirrorVertical = wx.StaticText(self.tabPage, label="Mirror Vertical: ")
        checkBoxMirrorHorizontal = wx.CheckBox(self.tabPage)
        horizontalBoxMirrorVertical.Add(labelMirrorVertical, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        horizontalBoxMirrorVertical.Add(checkBoxMirrorHorizontal, wx.EXPAND|wx.ALL)
        
        # tile properties
        verticalBoxTileProperties = wx.BoxSizer(wx.VERTICAL)
        labelTileProperties = wx.StaticText(self.tabPage, label="Tile Properties:")
        verticalBoxTileProperties.Add(labelTileProperties, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        verticalBoxTileProperties.Add(horizontalBoxMirrorHorizontal, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        verticalBoxTileProperties.Add(horizontalBoxMirrorVertical, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)

        # tile editor horizontal box
        horizontalBoxTileEditor= wx.BoxSizer(wx.HORIZONTAL)
        horizontalBoxTileEditor.Add(verticalBoxTileImage, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        horizontalBoxTileEditor.Add(verticalBoxTileProperties, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)        
        
        # tile editor
        verticalBoxTileEditor = wx.BoxSizer(wx.VERTICAL)
        labelTileEditor = wx.StaticText(self.tabPage, label="Tile Editor:")
        verticalBoxTileEditor.Add(labelTileEditor)
        verticalBoxTileEditor.Add(horizontalBoxTileEditor)

        horizontalBox = wx.BoxSizer(wx.HORIZONTAL)
        horizontalBox.Add(self.listBoxTilemaps, 0, wx.EXPAND)
        horizontalBox.Add(verticalBoxTilemapImage)
        horizontalBox.Add(verticalBoxTileEditor)
        
        self.tabPage.SetSizer(horizontalBox)
        self.tabPage.Fit()

        self.frame.Show(True)

    def load(self, tilemapNames):
        self.listBoxTilemaps.Set(tilemapNames)

    def onListBox(self, event):
        selectedIndex = self.listBoxTilemaps.GetSelection()
        pub.sendMessage("tilemaps_update", tilemapIndex=selectedIndex)

    def onTileImageClick(self, event):
        pass

    def onTilemapImageClick(self, event):
        x, y = event.GetPosition()
        tilemapClickedX = int(x / (self.TILEMAP_IMAGE_PIXEL_WIDTH / Model_Tilemap.TILEMAP_TILE_WIDTH))
        tilemapClickedY = int(y / (self.TILEMAP_IMAGE_PIXEL_HEIGHT / Model_Tilemap.TILEMAP_TILE_HEIGHT))
        selectedIndex = (tilemapClickedY * Model_Tilemap.TILEMAP_TILE_WIDTH) + tilemapClickedX

        pub.sendMessage("tilemaps_update_tile", tileIndex=selectedIndex)

    def update(self, tilemapImage : PIL.Image):
        sizedImage = tilemapImage.resize((self.TILEMAP_IMAGE_PIXEL_WIDTH, self.TILEMAP_IMAGE_PIXEL_HEIGHT), Image.Resampling.NEAREST)
        wx_image = wx.EmptyImage(sizedImage.size[0], sizedImage.size[1])
        wx_image.SetData(sizedImage.convert("RGB").tobytes())
        bitmap = wx.BitmapFromImage(wx_image)
        self.tilemapImage.SetBitmap(bitmap)
        self.tilemapImage.Sizer

    def updateTile(self, tileImage : PIL.Image):
        sizedImage = tileImage.resize((self.TILE_IMAGE_PIXEL_WIDTH, self.TILE_IMAGE_PIXEL_HEIGHT), Image.Resampling.NEAREST)
        wx_image = wx.EmptyImage(sizedImage.size[0], sizedImage.size[1])
        wx_image.SetData(sizedImage.convert("RGB").tobytes())
        bitmap = wx.BitmapFromImage(wx_image)
        self.tileImage.SetBitmap(bitmap)
        self.tileImage.Sizer