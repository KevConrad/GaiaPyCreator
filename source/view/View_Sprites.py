import PIL
import PIL.Image
import wx

from model.Model_Spritesets import Model_Spritesets
from view.View_Common import View_Common
from view.View_Tabs import TabSprites

from pubsub import pub
from PIL import Image

class View_Sprites:

    def __init__(self, frame : wx.Frame, notebook : wx.Notebook):
        self.frame = frame
        self.tabPage = notebook.GetPage(TabSprites.SPRITES_TAB_INDEX)

        # spritesets label
        labelSpritesets = wx.StaticText(self.tabPage, label="Spritesets", style=wx.ALIGN_CENTRE)
        # spritesets list box
        self.listBoxSpritesets = wx.ListBox(self.tabPage , size = (View_Common.LISTBOX_WIDTH, View_Common.LISTBOX_HEIGHT),
                                          style = wx.LB_SINGLE|wx.LB_HSCROLL)
        self.frame.Bind(wx.EVT_LISTBOX, self.onListBoxSpritesets, self.listBoxSpritesets)

        verticalBoxSpritesets = wx.BoxSizer(wx.VERTICAL)
        verticalBoxSpritesets.Add(labelSpritesets, 0, wx.EXPAND)
        verticalBoxSpritesets.Add(self.listBoxSpritesets, 0, wx.EXPAND)

        # sprites label and list box
        labelSprites = wx.StaticText(self.tabPage, label="Sprites", style=wx.ALIGN_CENTRE)
        self.listBoxSprites = wx.ListBox(self.tabPage , size = (View_Common.LISTBOX_WIDTH, View_Common.LISTBOX_HEIGHT),
                                          style = wx.LB_SINGLE|wx.LB_HSCROLL)
        self.frame.Bind(wx.EVT_LISTBOX, self.onListBoxSprites, self.listBoxSprites)
        verticalBoxSprites = wx.BoxSizer(wx.VERTICAL)
        verticalBoxSprites.Add(labelSprites, 0, wx.EXPAND)
        verticalBoxSprites.Add(self.listBoxSprites, 0, wx.EXPAND)

        horizontalBox = wx.BoxSizer(wx.HORIZONTAL)
        horizontalBox.Add(verticalBoxSpritesets, 0, wx.EXPAND)
        horizontalBox.AddSpacer(10)
        horizontalBox.Add(verticalBoxSprites, 0, wx.EXPAND)
        
        self.tabPage.SetSizer(horizontalBox)
        self.tabPage.Fit()

        self.frame.Show(True)

    def load(self, spritesets : Model_Spritesets):
        self.spritesets = spritesets
        self.listBoxSpritesets.Set(self.spritesets.spritesetNames)

    def onListBoxSpritesets(self, event):
        selectedIndex = self.listBoxSpritesets.GetSelection()
        self.listBoxSprites.Set(self.spritesets.spritesets[selectedIndex].spriteNames)
        # send message to update the sprites
        pub.sendMessage("spritesets_update", spritesetIndex=selectedIndex)

    def onListBoxSprites(self, event):
        selectedIndex = self.listBoxSprites.GetSelection()
        pub.sendMessage("sprites_update", spriteIndex=selectedIndex)

    def update(self):
        pass
