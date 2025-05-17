import PIL
import PIL.Image
import wx

from model.Model_Spritesets import Model_Spritesets
from model.Model_Spriteset import Model_Spriteset
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

        # sprite frame selection controls
        horizontalBoxSpriteFrameSelection = wx.BoxSizer(wx.HORIZONTAL)
        labelSpriteFrameSelection = wx.StaticText(self.tabPage, label="Sprite Frame: ")
        self.spinCtrlSpriteFrameCurrent = wx.SpinCtrl(self.tabPage, style=wx.SP_ARROW_KEYS)
        self.spinCtrlSpriteFrameCurrent.SetMin(0)
        self.spinCtrlSpriteFrameCurrent.SetMax(1024)
        self.spinCtrlSpriteFrameCurrent.Bind(wx.EVT_SPINCTRL, self.onSpriteFrameSelectionChanged)
        labelSpriteFrameSelectionSlash = wx.StaticText(self.tabPage, label=" / ")
        self.spinCtrlSpriteFrameCount = wx.SpinCtrl(self.tabPage, style=wx.SP_ARROW_KEYS)
        self.spinCtrlSpriteFrameCount.SetMin(0)
        self.spinCtrlSpriteFrameCount.SetMax(1024)
        horizontalBoxSpriteFrameSelection.Add(labelSpriteFrameSelection, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        horizontalBoxSpriteFrameSelection.Add(self.spinCtrlSpriteFrameCurrent, wx.EXPAND|wx.ALL)
        horizontalBoxSpriteFrameSelection.Add(labelSpriteFrameSelectionSlash, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        horizontalBoxSpriteFrameSelection.Add(self.spinCtrlSpriteFrameCount, wx.EXPAND|wx.ALL)

        # sprite frame list box
        self.listBoxSpriteFrame = wx.ListBox(self.tabPage , size = (View_Common.LISTBOX_WIDTH, View_Common.LISTBOX_HEIGHT / 2),
        style = wx.LB_SINGLE|wx.LB_HSCROLL)
        self.frame.Bind(wx.EVT_LISTBOX, self.onListBoxSprites, self.listBoxSpriteFrame)
        verticalBoxSpriteFrame = wx.BoxSizer(wx.VERTICAL)
        verticalBoxSpriteFrame.Add(horizontalBoxSpriteFrameSelection, 0, wx.EXPAND)
        verticalBoxSpriteFrame.Add(self.listBoxSpriteFrame, 0, wx.EXPAND)

        horizontalBox = wx.BoxSizer(wx.HORIZONTAL)
        horizontalBox.Add(verticalBoxSpritesets, 0, wx.EXPAND)
        horizontalBox.AddSpacer(10)
        horizontalBox.Add(verticalBoxSprites, 0, wx.EXPAND)
        horizontalBox.AddSpacer(10)
        horizontalBox.Add(verticalBoxSpriteFrame, 0, wx.EXPAND)
        
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
        pub.sendMessage("sprites_update_spriteset", spritesetIndex=selectedIndex)

    def onListBoxSprites(self, event):
        selectedIndex = self.listBoxSprites.GetSelection()
        pub.sendMessage("sprites_update_sprite", spriteIndex=selectedIndex)

    def onSpriteFrameSelectionChanged(self, event):
        pass

    def updateSpriteset(self, spritesetData : Model_Spriteset):
        self.spritesetData = spritesetData

        # select sprite 0 from the list box
        self.listBoxSprites.SetSelection(0)

        # clear the sprite frame list box
        self.listBoxSpriteFrame.Clear()
        # update the sprite frame list box
        for spriteFrame in range(len(self.spritesetData.spriteFrames)):
            self.listBoxSpriteFrame.Append("Frame " + str(spriteFrame))

        # select the sprite frame from sprite 0
        self.listBoxSpriteFrame.SetSelection(self.spritesetData.sprites[0].frameData[0].frameId)

    def updateSprite(self, spriteIndex : int):
        # update the sprite frame selection
        self.spinCtrlSpriteFrameCount.SetValue(len(self.spritesetData.sprites[spriteIndex].frameData))
        self.spinCtrlSpriteFrameCurrent.SetValue(0)

        # select the sprite frame
        self.listBoxSpriteFrame.SetSelection(self.spritesetData.sprites[spriteIndex].frameData[0].frameId)
        
