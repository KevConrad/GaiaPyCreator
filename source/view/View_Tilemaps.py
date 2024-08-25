import PIL
import PIL.Image
import wx

from view.View_Common import View_Common

from pubsub import pub
from PIL import Image

class View_Tilemaps:
    def __init__(self, frame : wx.Frame, notebook : wx.Notebook):
        self.frame = frame
        self.tabPage = notebook.GetPage(8)

        self.labelTilemap = wx.StaticText(self.tabPage, label="Tilemap:")
        horizontalBoxTilemap = wx.BoxSizer(wx.HORIZONTAL)
        horizontalBoxTilemap.Add(self.labelTilemap, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)

        self.tilemapImage = wx.StaticBitmap(self.tabPage, wx.ID_ANY, wx.NullBitmap)

        verticalBoxItemData = wx.BoxSizer(wx.VERTICAL)
        verticalBoxItemData.Add(horizontalBoxTilemap)

        self.listBoxTilemaps = wx.ListBox(self.tabPage , size = (View_Common.LISTBOX_WIDTH, View_Common.LISTBOX_HEIGHT),
                                          style = wx.LB_SINGLE|wx.LB_HSCROLL)
        horizontalBox = wx.BoxSizer(wx.HORIZONTAL)
        horizontalBox.Add(self.listBoxTilemaps, 0, wx.EXPAND)
        
        horizontalBox.Add(verticalBoxItemData)
        
        self.tabPage.SetSizer(horizontalBox)
        self.tabPage.Fit()

        self.frame.Bind(wx.EVT_LISTBOX, self.onListBox, self.listBoxTilemaps)
        self.frame.Show(True)

    def load(self, tilemapNames):
        self.listBoxTilemaps.Set(tilemapNames)

    def onListBox(self, event):
        selectedIndex = self.listBoxTilemaps.GetSelection()
        pub.sendMessage("tilemaps_update", tilemapIndex=selectedIndex)

    def update(self, tilemapImage : PIL.Image):
        sizedImage = tilemapImage.resize((256, 256), Image.Resampling.LANCZOS)
        wx_image = wx.EmptyImage(sizedImage.size[0], sizedImage.size[1])
        wx_image.SetData(sizedImage.convert("RGB").tobytes())
        bitmap = wx.BitmapFromImage(wx_image)
        self.tilemapImage.SetBitmap(bitmap)
        self.tilemapImage.Sizer