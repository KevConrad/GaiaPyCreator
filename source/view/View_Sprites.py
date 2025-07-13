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
    SPRITE_IMAGE_PIXEL_HEIGHT = 300
    SPRITE_IMAGE_PIXEL_WIDTH = 300

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
        self.spinCtrlSpriteFrameCurrent.SetMin(1)
        self.spinCtrlSpriteFrameCurrent.SetMax(1024)
        self.spinCtrlSpriteFrameCurrent.Bind(wx.EVT_SPINCTRL, self.onSpriteFrameSelectionChanged)
        labelSpriteFrameSelectionSlash = wx.StaticText(self.tabPage, label=" / ")
        self.spinCtrlSpriteFrameCount = wx.SpinCtrl(self.tabPage, style=wx.SP_ARROW_KEYS)
        self.spinCtrlSpriteFrameCount.SetMin(1)
        self.spinCtrlSpriteFrameCount.SetMax(1024)
        horizontalBoxSpriteFrameSelection.Add(labelSpriteFrameSelection, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        horizontalBoxSpriteFrameSelection.Add(self.spinCtrlSpriteFrameCurrent, wx.EXPAND|wx.ALL)
        horizontalBoxSpriteFrameSelection.Add(labelSpriteFrameSelectionSlash, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        horizontalBoxSpriteFrameSelection.Add(self.spinCtrlSpriteFrameCount, wx.EXPAND|wx.ALL)

        # sprite frame list box
        self.listBoxSpriteFrame = wx.ListBox(self.tabPage , size = (View_Common.LISTBOX_WIDTH, View_Common.LISTBOX_HEIGHT / 2),
        style = wx.LB_SINGLE|wx.LB_HSCROLL)
        self.frame.Bind(wx.EVT_LISTBOX, self.onListBoxSprites, self.listBoxSpriteFrame)


        # sprite frame editor label
        labelSpriteFrameEditor = wx.StaticText(self.tabPage, label="Sprite Frame Editor", style=wx.ALIGN_LEFT)
        # sprite frame editor image
        self.scrolledWindowMap = wx.ScrolledWindow(self.tabPage, wx.ID_ANY,
                                                   size=(self.SPRITE_IMAGE_PIXEL_WIDTH, self.SPRITE_IMAGE_PIXEL_HEIGHT))
        self.scrolledWindowMap.SetScrollbars(1, 1, self.SPRITE_IMAGE_PIXEL_WIDTH, self.SPRITE_IMAGE_PIXEL_HEIGHT)
        self.scrolledWindowMap.SetBackgroundColour(wx.Colour(0, 0, 0))  

        # horizontal box for sprite frame editor
        horizontalBoxSpriteFrameEditor = wx.BoxSizer(wx.HORIZONTAL)
        horizontalBoxSpriteFrameEditor.Add(self.scrolledWindowMap, 0, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)

        # create sprite image
        self.displayedSpriteImage = wx.StaticBitmap(self.scrolledWindowMap, wx.ID_ANY, wx.NullBitmap,
                                                 size=(self.SPRITE_IMAGE_PIXEL_WIDTH, self.SPRITE_IMAGE_PIXEL_HEIGHT))

        verticalBoxSpriteFrame = wx.BoxSizer(wx.VERTICAL)
        verticalBoxSpriteFrame.Add(horizontalBoxSpriteFrameSelection, 0, wx.EXPAND)
        verticalBoxSpriteFrame.Add(self.listBoxSpriteFrame, 0, wx.EXPAND)
        verticalBoxSpriteFrame.Add(labelSpriteFrameEditor, 0, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        verticalBoxSpriteFrame.Add(horizontalBoxSpriteFrameEditor, 0, wx.EXPAND)

        # sprite frame property controls
        verticalBoxSpriteFrameProperties = wx.BoxSizer(wx.VERTICAL)
        # sprite frame duration controls
        horizontalBoxSpriteDuration= wx.BoxSizer(wx.HORIZONTAL)
        # sprite frame duration label
        labelSpriteFrameDuration = wx.StaticText(self.tabPage, label="Duration: ")
        # sprite frame duration spin control
        self.spinCtrlSpriteFrameDuration = wx.SpinCtrl(self.tabPage, style=wx.SP_ARROW_KEYS)
        self.spinCtrlSpriteFrameDuration.SetMin(0)
        self.spinCtrlSpriteFrameDuration.SetMax(1024)

        horizontalBoxSpriteDuration.Add(labelSpriteFrameDuration, 0, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        horizontalBoxSpriteDuration.Add(self.spinCtrlSpriteFrameDuration, 0, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)

        # sprite frame offfset x controls
        horizontalBoxSpriteFrameOffsetX = wx.BoxSizer(wx.HORIZONTAL)
        # sprite frame offset x label
        labelSpriteFrameOffsetX = wx.StaticText(self.tabPage, label="Offset X: ")
        # sprite frame offset x spin control
        self.spinCtrlSpriteFrameOffsetX = wx.SpinCtrl(self.tabPage, style=wx.SP_ARROW_KEYS)
        self.spinCtrlSpriteFrameOffsetX.SetMin(0)
        self.spinCtrlSpriteFrameOffsetX.SetMax(255)

        horizontalBoxSpriteFrameOffsetX.Add(labelSpriteFrameOffsetX, 0, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        horizontalBoxSpriteFrameOffsetX.Add(self.spinCtrlSpriteFrameOffsetX, 0, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)

        # sprite frame position y controls
        horizontalBoxSpriteFrameOffsetY = wx.BoxSizer(wx.HORIZONTAL)
        # sprite frame position y label
        labelSpriteFrameOffsetY = wx.StaticText(self.tabPage, label="Offset Y: ")
        # sprite frame position y spin control
        self.spinCtrlSpriteFrameOffsetY = wx.SpinCtrl(self.tabPage, style=wx.SP_ARROW_KEYS)
        self.spinCtrlSpriteFrameOffsetY.SetMin(0)
        self.spinCtrlSpriteFrameOffsetY.SetMax(255)

        horizontalBoxSpriteFrameOffsetY.Add(labelSpriteFrameOffsetY, 0, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        horizontalBoxSpriteFrameOffsetY.Add(self.spinCtrlSpriteFrameOffsetY, 0, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)

        verticalBoxSpriteFrameProperties.Add(horizontalBoxSpriteDuration, 0, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        verticalBoxSpriteFrameProperties.Add(horizontalBoxSpriteFrameOffsetX, 0, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        verticalBoxSpriteFrameProperties.Add(horizontalBoxSpriteFrameOffsetY, 0, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)

        horizontalBox = wx.BoxSizer(wx.HORIZONTAL)
        horizontalBox.Add(verticalBoxSpritesets, 0, wx.EXPAND)
        horizontalBox.AddSpacer(10)
        horizontalBox.Add(verticalBoxSprites, 0, wx.EXPAND)
        horizontalBox.AddSpacer(10)
        horizontalBox.Add(verticalBoxSpriteFrame, 0, wx.EXPAND)
        horizontalBox.AddSpacer(10)
        horizontalBox.Add(verticalBoxSpriteFrameProperties, 0, wx.EXPAND)
        
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
        spriteFrameIndex = self.spinCtrlSpriteFrameCurrent.GetValue() - 1
        self.updateSpriteFrame(spriteFrameIndex)

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
        self. spriteIndex = spriteIndex
        # update the sprite frame selection
        self.spinCtrlSpriteFrameCount.SetValue(len(self.spritesetData.sprites[spriteIndex].frameData))
        self.spinCtrlSpriteFrameCurrent.SetValue(1)
        self.spinCtrlSpriteFrameCurrent.SetMax(len(self.spritesetData.sprites[spriteIndex].frameData))

        # update sprite frame data
        self.updateSpriteFrame(0)

    def updateSpriteFrame(self, spriteFrameIndex : int):
        # select the sprite frame
        frameId = self.spritesetData.sprites[self.spriteIndex].frameData[spriteFrameIndex].frameId
        self.listBoxSpriteFrame.SetSelection(frameId)

        # update the sprite frame properties
        self.spinCtrlSpriteFrameDuration.SetValue(self.spritesetData.sprites[self.spriteIndex].frameData[0].duration)
        self.spinCtrlSpriteFrameOffsetX.SetValue(self.spritesetData.spriteFrames[frameId].offsetX)
        self.spinCtrlSpriteFrameOffsetY.SetValue(self.spritesetData.spriteFrames[frameId].offsetY)

        
        
