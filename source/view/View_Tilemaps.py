import PIL
import PIL.Image
import wx

from model.Model_Tile import Model_Tile
from model.Model_Tilemap import Model_Tilemap
from view.View_Common import View_Common
from view.View_Tabs import TabTilemaps

from pubsub import pub
from PIL import Image

class View_Tilemaps:
    TILE_IMAGE_PIXEL_HEIGHT = 100
    TILE_IMAGE_PIXEL_WIDTH = 100

    TILEMAP_IMAGE_PIXEL_HEIGHT = 400
    TILEMAP_IMAGE_PIXEL_WIDTH = 400

    TILESET_IMAGE_PIXEL_HEIGHT = 200
    TILESET_IMAGE_PIXEL_WIDTH = 200

    def __init__(self, frame : wx.Frame, notebook : wx.Notebook):
        self.frame = frame
        self.tabPage = notebook.GetPage(TabTilemaps.TILEMAPS_TAB_INDEX)

        # tilemaps list box
        self.listBoxTilemaps = wx.ListBox(self.tabPage , size = (View_Common.LISTBOX_WIDTH, View_Common.LISTBOX_HEIGHT),
                                          style = wx.LB_SINGLE|wx.LB_HSCROLL)
        self.frame.Bind(wx.EVT_LISTBOX, self.onListBox, self.listBoxTilemaps)

        # tilemap image
        verticalBoxTilemapImage = wx.BoxSizer(wx.VERTICAL)
        labelTilemap = wx.StaticText(self.tabPage, label="Tilemap:")
        self.tilemapImage = wx.StaticBitmap(self.tabPage, wx.ID_ANY, wx.NullBitmap,
                                            size=(self.TILEMAP_IMAGE_PIXEL_WIDTH, self.TILEMAP_IMAGE_PIXEL_HEIGHT))
        self.tilemapImage.Bind(wx.EVT_LEFT_DOWN, self.onTilemapImageClick)
        verticalBoxTilemapImage.Add(labelTilemap)
        verticalBoxTilemapImage.Add(self.tilemapImage)

        # tile image
        verticalBoxTileImage = wx.BoxSizer(wx.VERTICAL)
        labelTile = wx.StaticText(self.tabPage, label="Tile:")
        self.tileImage = wx.StaticBitmap(self.tabPage, wx.ID_ANY, wx.NullBitmap,
                                         size=(self.TILE_IMAGE_PIXEL_WIDTH, self.TILE_IMAGE_PIXEL_HEIGHT))
        self.tileImage.Bind(wx.EVT_LEFT_DOWN, self.onTileImageClick)
        verticalBoxTileImage.Add(labelTile)
        verticalBoxTileImage.Add(self.tileImage)

        # mirror horizontal checkBox
        horizontalBoxMirrorHorizontal = wx.BoxSizer(wx.HORIZONTAL)
        labelMirrorHorizontal = wx.StaticText(self.tabPage, label="Mirror Horizontal: ")
        self.checkBoxMirrorHorizontal = wx.CheckBox(self.tabPage)
        horizontalBoxMirrorHorizontal.Add(labelMirrorHorizontal, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        horizontalBoxMirrorHorizontal.Add(self.checkBoxMirrorHorizontal, wx.EXPAND|wx.ALL)
        
        # mirror vertical checkBox
        horizontalBoxMirrorVertical = wx.BoxSizer(wx.HORIZONTAL)
        labelMirrorVertical = wx.StaticText(self.tabPage, label="Mirror Vertical: ")
        self.checkBoxMirrorVertical = wx.CheckBox(self.tabPage)
        horizontalBoxMirrorVertical.Add(labelMirrorVertical, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        horizontalBoxMirrorVertical.Add(self.checkBoxMirrorVertical, wx.EXPAND|wx.ALL)

        # over player checkBox
        horizontalBoxOverPlayer = wx.BoxSizer(wx.HORIZONTAL)
        labelOverPlayer = wx.StaticText(self.tabPage, label="Over Player: ")
        self.checkBoxOverPlayer = wx.CheckBox(self.tabPage)
        horizontalBoxOverPlayer.Add(labelOverPlayer, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        horizontalBoxOverPlayer.Add(self.checkBoxOverPlayer, wx.EXPAND|wx.ALL)

        # palette id spinCtrl
        horizontalBoxPaletteId = wx.BoxSizer(wx.HORIZONTAL)
        labelPaletteId = wx.StaticText(self.tabPage, label="Palette ID: ")
        self.spinCtrlPaletteId = wx.SpinCtrl(self.tabPage, style=wx.SP_ARROW_KEYS)
        self.spinCtrlPaletteId.SetMin(0)
        self.spinCtrlPaletteId.SetMax(7)
        horizontalBoxPaletteId.Add(labelPaletteId, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        horizontalBoxPaletteId.Add(self.spinCtrlPaletteId, wx.EXPAND|wx.ALL)

        # tileset id spinCtrl
        horizontalBoxTilesetId = wx.BoxSizer(wx.HORIZONTAL)
        labelTilesetId = wx.StaticText(self.tabPage, label="Tileset ID: ")
        self.spinCtrlTilesetId = wx.SpinCtrl(self.tabPage, style=wx.SP_ARROW_KEYS)
        self.spinCtrlTilesetId.SetMin(0)
        self.spinCtrlTilesetId.SetMax(1)
        horizontalBoxTilesetId.Add(labelTilesetId, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        horizontalBoxTilesetId.Add(self.spinCtrlTilesetId, wx.EXPAND|wx.ALL)

        # tile type comboBox
        horizontalBoxTileType = wx.BoxSizer(wx.HORIZONTAL)
        labelTileType = wx.StaticText(self.tabPage, label="Type: ")
        self.comboBoxTileType = wx.ComboBox(self.tabPage, style=wx.CB_READONLY, choices=Model_Tile.TILE_TYPE_NAMES)
        horizontalBoxTileType.Add(labelTileType, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        horizontalBoxTileType.Add(self.comboBoxTileType, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        
        # tile properties
        verticalBoxTileProperties = wx.BoxSizer(wx.VERTICAL)
        labelTileProperties = wx.StaticText(self.tabPage, label="Tile Properties:")
        verticalBoxTileProperties.Add(labelTileProperties, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        verticalBoxTileProperties.Add(horizontalBoxMirrorHorizontal, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        verticalBoxTileProperties.Add(horizontalBoxMirrorVertical, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        verticalBoxTileProperties.Add(horizontalBoxOverPlayer, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        verticalBoxTileProperties.Add(horizontalBoxPaletteId, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        verticalBoxTileProperties.Add(horizontalBoxTilesetId, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        verticalBoxTileProperties.Add(horizontalBoxTileType, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)

        # tile editor horizontal box
        horizontalBoxTileEditor= wx.BoxSizer(wx.HORIZONTAL)
        horizontalBoxTileEditor.Add(verticalBoxTileImage, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        horizontalBoxTileEditor.Add(verticalBoxTileProperties, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)

        # tileset image
        verticalBoxTilesetImage = wx.BoxSizer(wx.VERTICAL)
        labelTileset = wx.StaticText(self.tabPage, label="Tileset:")
        self.tilesetImage = wx.StaticBitmap(self.tabPage, wx.ID_ANY, wx.NullBitmap,
                                         size=(self.TILESET_IMAGE_PIXEL_WIDTH, self.TILESET_IMAGE_PIXEL_HEIGHT))
        self.tilesetImage.Bind(wx.EVT_LEFT_DOWN, self.onTileImageClick)
        verticalBoxTilesetImage.Add(labelTileset)
        verticalBoxTilesetImage.Add(self.tilesetImage)   
        
        # tile editor
        verticalBoxTileEditor = wx.BoxSizer(wx.VERTICAL)
        labelTileEditor = wx.StaticText(self.tabPage, label="Tile Editor:")
        verticalBoxTileEditor.Add(labelTileEditor)
        verticalBoxTileEditor.Add(horizontalBoxTileEditor)
        verticalBoxTileEditor.Add(verticalBoxTilesetImage)

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
        x, y = event.GetPosition()
        tileClickedX = int(x / (self.TILE_IMAGE_PIXEL_WIDTH / Model_Tilemap.TILEMAP_TILE_PIECE_WIDTH))
        tileClickedY = int(y / (self.TILE_IMAGE_PIXEL_HEIGHT / Model_Tilemap.TILEMAP_TILE_PIECE_HEIGHT))
        selectedTilePiece = (tileClickedY * Model_Tilemap.TILEMAP_TILE_PIECE_WIDTH) + tileClickedX

        pub.sendMessage("tilemaps_update_tile", tileIndex=self.selectedTileIndex, tilePieceIndex=selectedTilePiece)

    def onTilemapImageClick(self, event):
        x, y = event.GetPosition()
        tilemapClickedX = int(x / (self.TILEMAP_IMAGE_PIXEL_WIDTH / Model_Tilemap.TILEMAP_TILE_WIDTH))
        tilemapClickedY = int(y / (self.TILEMAP_IMAGE_PIXEL_HEIGHT / Model_Tilemap.TILEMAP_TILE_HEIGHT))
        self.selectedTileIndex = (tilemapClickedY * Model_Tilemap.TILEMAP_TILE_WIDTH) + tilemapClickedX

        pub.sendMessage("tilemaps_update_tile", tileIndex=self.selectedTileIndex, tilePieceIndex=0)

    def update(self, tilemapImage : PIL.Image):
        sizedImage = tilemapImage.resize((self.TILEMAP_IMAGE_PIXEL_WIDTH, self.TILEMAP_IMAGE_PIXEL_HEIGHT), Image.Resampling.NEAREST)
        wx_image = wx.EmptyImage(sizedImage.size[0], sizedImage.size[1])
        wx_image.SetData(sizedImage.convert("RGB").tobytes())
        bitmap = wx.BitmapFromImage(wx_image)
        self.tilemapImage.SetBitmap(bitmap)
        self.tilemapImage.Sizer

    def updateTile(self, tileImage : PIL.Image, tileProperties : Model_Tile):
        # update the tile image
        sizedImage = tileImage.resize((self.TILE_IMAGE_PIXEL_WIDTH, self.TILE_IMAGE_PIXEL_HEIGHT), Image.Resampling.NEAREST)
        wx_image = wx.EmptyImage(sizedImage.size[0], sizedImage.size[1])
        wx_image.SetData(sizedImage.convert("RGB").tobytes())
        bitmap = wx.BitmapFromImage(wx_image)
        self.tileImage.SetBitmap(bitmap)
        self.tileImage.Sizer

        # update the tile property controls
        self.checkBoxMirrorHorizontal.SetValue(tileProperties.isMirroredX)
        self.checkBoxMirrorVertical.SetValue(tileProperties.isMirroredY)
        self.checkBoxOverPlayer.SetValue(tileProperties.isOverPlayer)
        self.spinCtrlPaletteId.SetValue(tileProperties.paletteId)
        self.spinCtrlTilesetId.SetValue(tileProperties.tilesetId)
        self.comboBoxTileType.SetSelection(tileProperties.type)