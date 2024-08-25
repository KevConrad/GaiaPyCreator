import PIL
import PIL.Image
import wx

from view.View_Common import View_Common

from pubsub import pub
from PIL import Image

class View_Tilesets:
    def __init__(self, frame : wx.Frame, notebook : wx.Notebook):
        self.frame = frame
        self.tabPage = notebook.GetPage(9)

        self.labelTileset = wx.StaticText(self.tabPage, label="Tileset:")
        horizontalBoxTileset = wx.BoxSizer(wx.HORIZONTAL)
        horizontalBoxTileset.Add(self.labelTileset, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)

        self.tilesetImage = wx.StaticBitmap(self.tabPage, wx.ID_ANY, wx.NullBitmap)

        verticalBoxTilesetData = wx.BoxSizer(wx.VERTICAL)
        verticalBoxTilesetData.Add(horizontalBoxTileset)
        verticalBoxTilesetData.Add(self.tilesetImage)

        self.listBoxTilesets = wx.ListBox(self.tabPage , size = (View_Common.LISTBOX_WIDTH, View_Common.LISTBOX_HEIGHT),
                                          style = wx.LB_SINGLE|wx.LB_HSCROLL)
        self.horizontalBox = wx.BoxSizer(wx.HORIZONTAL)
        self.horizontalBox.Add(self.listBoxTilesets, 0, wx.EXPAND)

        self.horizontalBox.Add(verticalBoxTilesetData)
        
        self.tabPage.SetSizer(self.horizontalBox) 
        self.tabPage.Fit() 

        self.frame.Bind(wx.EVT_LISTBOX, self.onListBox, self.listBoxTilesets) 
        self.frame.Show(True)

    def load(self, tilesetNames):
        self.listBoxTilesets.Set(tilesetNames)

    def onListBox(self, event):
        selectedIndex = self.listBoxTilesets.GetSelection()
        pub.sendMessage("tilesets_update", tilesetIndex=selectedIndex)

    def update(self, tilesetImage : PIL.Image):
        sizedImage = tilesetImage.resize((256, 256), Image.Resampling.LANCZOS)
        wx_image = wx.EmptyImage(sizedImage.size[0], sizedImage.size[1])
        wx_image.SetData(sizedImage.convert("RGB").tobytes())
        bitmap = wx.BitmapFromImage(wx_image)
        self.tilesetImage.SetBitmap(bitmap)
        self.tilesetImage.Sizer