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
    SPRITE_IMAGE_PIXEL_HEIGHT = 230
    SPRITE_IMAGE_PIXEL_WIDTH = 230

    def __init__(self, frame : wx.Frame, notebook : wx.Notebook):
        self.frame = frame
        self.tabPage = notebook.GetPage(TabSprites.SPRITES_TAB_INDEX)

        ### spritesets

        # spritesets label
        labelSpritesets = wx.StaticText(self.tabPage, label="Spritesets", style=wx.ALIGN_CENTRE)
        # spritesets list box
        self.listBoxSpritesets = wx.ListBox(self.tabPage , size = (View_Common.LISTBOX_WIDTH, View_Common.LISTBOX_HEIGHT),
                                          style = wx.LB_SINGLE|wx.LB_HSCROLL)
        self.frame.Bind(wx.EVT_LISTBOX, self.onListBoxSpritesets, self.listBoxSpritesets)

        verticalBoxSpritesets = wx.BoxSizer(wx.VERTICAL)
        verticalBoxSpritesets.Add(labelSpritesets, 0, wx.EXPAND)
        verticalBoxSpritesets.Add(self.listBoxSpritesets, 0, wx.EXPAND)

        ### sprites

        # sprites label and list box
        labelSprites = wx.StaticText(self.tabPage, label="Sprites", style=wx.ALIGN_CENTRE)
        self.listBoxSprites = wx.ListBox(self.tabPage , size = (View_Common.LISTBOX_WIDTH, View_Common.LISTBOX_HEIGHT),
                                          style = wx.LB_SINGLE|wx.LB_HSCROLL)
        self.frame.Bind(wx.EVT_LISTBOX, self.onListBoxSprites, self.listBoxSprites)
        verticalBoxSprites = wx.BoxSizer(wx.VERTICAL)
        verticalBoxSprites.Add(labelSprites, 0, wx.EXPAND)
        verticalBoxSprites.Add(self.listBoxSprites, 0, wx.EXPAND)

        ### sprite frames

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

        # sprite frame property controls
        verticalBoxSpriteFrameProperties = wx.BoxSizer(wx.VERTICAL)
        verticalBoxSpriteFrameProperties.Add(horizontalBoxSpriteDuration, 0, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        verticalBoxSpriteFrameProperties.Add(horizontalBoxSpriteFrameOffsetX, 0, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        verticalBoxSpriteFrameProperties.Add(horizontalBoxSpriteFrameOffsetY, 0, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)

        horizontalBoxSpriteFrameEditor = wx.BoxSizer(wx.HORIZONTAL)
        horizontalBoxSpriteFrameEditor.Add(self.listBoxSpriteFrame, 0, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        horizontalBoxSpriteFrameEditor.Add(verticalBoxSpriteFrameProperties, 0, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)

        verticalBoxSpriteFrame = wx.BoxSizer(wx.VERTICAL)
        verticalBoxSpriteFrame.Add(horizontalBoxSpriteFrameSelection, 0, wx.EXPAND)
        verticalBoxSpriteFrame.Add(horizontalBoxSpriteFrameEditor, 0, wx.EXPAND)

        ### Sprite Frame Editor

        # sprite frame tile selection controls
        horizontalBoxSpriteFrameTileSelection = wx.BoxSizer(wx.HORIZONTAL)
        labelSpriteFrameTileSelection = wx.StaticText(self.tabPage, label="Tile: ")
        self.spinCtrlSpriteFrameTileCurrent = wx.SpinCtrl(self.tabPage, style=wx.SP_ARROW_KEYS)
        self.spinCtrlSpriteFrameTileCurrent.SetMin(1)
        self.spinCtrlSpriteFrameTileCurrent.SetMax(1024)
        self.spinCtrlSpriteFrameTileCurrent.Bind(wx.EVT_SPINCTRL, self.onSpriteFrameTileSelectionChanged)
        labelSpriteFrameTileSelectionSlash = wx.StaticText(self.tabPage, label=" / ")
        self.spinCtrlSpriteFrameTileCount = wx.SpinCtrl(self.tabPage, style=wx.SP_ARROW_KEYS)
        self.spinCtrlSpriteFrameTileCount.SetMin(1)
        self.spinCtrlSpriteFrameTileCount.SetMax(1024)
        horizontalBoxSpriteFrameTileSelection.Add(labelSpriteFrameTileSelection, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        horizontalBoxSpriteFrameTileSelection.Add(self.spinCtrlSpriteFrameTileCurrent, wx.EXPAND|wx.ALL)
        horizontalBoxSpriteFrameTileSelection.Add(labelSpriteFrameTileSelectionSlash, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        horizontalBoxSpriteFrameTileSelection.Add(self.spinCtrlSpriteFrameTileCount, wx.EXPAND|wx.ALL)

        # sprite frame editor image
        self.scrolledWindowMap = wx.ScrolledWindow(self.tabPage, wx.ID_ANY,
                                                   size=(self.SPRITE_IMAGE_PIXEL_WIDTH, self.SPRITE_IMAGE_PIXEL_HEIGHT))
        self.scrolledWindowMap.SetScrollbars(1, 1, self.SPRITE_IMAGE_PIXEL_WIDTH, self.SPRITE_IMAGE_PIXEL_HEIGHT)
        self.scrolledWindowMap.SetBackgroundColour(wx.Colour(0, 0, 0))

        # sprite frame tile properties controls
        self.checkboxSpriteFrameTileCutout = wx.CheckBox(self.tabPage, label="Cutout")
        self.checkboxSpriteFrameTileMirrorX = wx.CheckBox(self.tabPage, label="Mirror X")
        self.checkboxSpriteFrameTileMirrorY = wx.CheckBox(self.tabPage, label="Mirror Y")
        # sprite frame tile offfset x controls
        horizontalBoxSpriteFrameTileOffsetX = wx.BoxSizer(wx.HORIZONTAL)
        labelSpriteFrameTileOffsetX = wx.StaticText(self.tabPage, label="Offset X: ")
        self.spinCtrlSpriteFrameTileOffsetX = wx.SpinCtrl(self.tabPage, style=wx.SP_ARROW_KEYS)
        self.spinCtrlSpriteFrameTileOffsetX.SetMin(0)
        self.spinCtrlSpriteFrameTileOffsetX.SetMax(255)
        horizontalBoxSpriteFrameTileOffsetX.Add(labelSpriteFrameTileOffsetX, 0, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        horizontalBoxSpriteFrameTileOffsetX.Add(self.spinCtrlSpriteFrameTileOffsetX, 0, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        # sprite frame tile offfset y controls
        horizontalBoxSpriteFrameTileOffsetY = wx.BoxSizer(wx.HORIZONTAL)
        labelSpriteFrameTileOffsetY = wx.StaticText(self.tabPage, label="Offset Y: ")
        self.spinCtrlSpriteFrameTileOffsetY = wx.SpinCtrl(self.tabPage, style=wx.SP_ARROW_KEYS)
        self.spinCtrlSpriteFrameTileOffsetY.SetMin(0)
        self.spinCtrlSpriteFrameTileOffsetY.SetMax(255)
        horizontalBoxSpriteFrameTileOffsetY.Add(labelSpriteFrameTileOffsetY, 0, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        horizontalBoxSpriteFrameTileOffsetY.Add(self.spinCtrlSpriteFrameTileOffsetY, 0, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        # sprite frame tile palette index controls
        horizontalBoxSpriteFrameTilePaletteIndex = wx.BoxSizer(wx.HORIZONTAL)
        labelSpriteFrameTilePaletteIndex = wx.StaticText(self.tabPage, label="Palette ID: ")
        self.spinCtrlSpriteFrameTilePaletteIndex = wx.SpinCtrl(self.tabPage, style=wx.SP_ARROW_KEYS)
        self.spinCtrlSpriteFrameTilePaletteIndex.SetMin(0)
        self.spinCtrlSpriteFrameTilePaletteIndex.SetMax(255)
        horizontalBoxSpriteFrameTilePaletteIndex.Add(labelSpriteFrameTilePaletteIndex, 0, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        horizontalBoxSpriteFrameTilePaletteIndex.Add(self.spinCtrlSpriteFrameTilePaletteIndex, 0, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        # sprite frame tile tileset index controls
        horizontalBoxSpriteFrameTileTilesetIndex = wx.BoxSizer(wx.HORIZONTAL)
        labelSpriteFrameTileTilesetIndex = wx.StaticText(self.tabPage, label="Tileset ID: ")
        self.spinCtrlSpriteFrameTileTilesetIndex = wx.SpinCtrl(self.tabPage, style=wx.SP_ARROW_KEYS)
        self.spinCtrlSpriteFrameTileTilesetIndex.SetMin(0)
        self.spinCtrlSpriteFrameTileTilesetIndex.SetMax(255)
        horizontalBoxSpriteFrameTileTilesetIndex.Add(labelSpriteFrameTileTilesetIndex, 0, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        horizontalBoxSpriteFrameTileTilesetIndex.Add(self.spinCtrlSpriteFrameTileTilesetIndex, 0, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        # sprite frame tile byte1 controls
        horizontalBoxSpriteFrameTileByte1Index = wx.BoxSizer(wx.HORIZONTAL)
        labelSpriteFrameTileByte1Index = wx.StaticText(self.tabPage, label="Byte 1: ")
        self.spinCtrlSpriteFrameTileByte1Index = wx.SpinCtrl(self.tabPage, style=wx.SP_ARROW_KEYS)
        self.spinCtrlSpriteFrameTileByte1Index.SetMin(0)
        self.spinCtrlSpriteFrameTileByte1Index.SetMax(255)
        horizontalBoxSpriteFrameTileByte1Index.Add(labelSpriteFrameTileByte1Index, 0, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        horizontalBoxSpriteFrameTileByte1Index.Add(self.spinCtrlSpriteFrameTileByte1Index, 0, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        # sprite frame tile byte2 controls
        horizontalBoxSpriteFrameTileByte2Index = wx.BoxSizer(wx.HORIZONTAL)
        labelSpriteFrameTileByte2Index = wx.StaticText(self.tabPage, label="Byte 2: ")
        self.spinCtrlSpriteFrameTileByte2Index = wx.SpinCtrl(self.tabPage, style=wx.SP_ARROW_KEYS)
        self.spinCtrlSpriteFrameTileByte2Index.SetMin(0)
        self.spinCtrlSpriteFrameTileByte2Index.SetMax(255)
        horizontalBoxSpriteFrameTileByte2Index.Add(labelSpriteFrameTileByte2Index, 0, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        horizontalBoxSpriteFrameTileByte2Index.Add(self.spinCtrlSpriteFrameTileByte2Index, 0, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)

        verticalBoxSpriteFrameTileProperties = wx.BoxSizer(wx.VERTICAL)
        verticalBoxSpriteFrameTileProperties.Add(self.checkboxSpriteFrameTileCutout, 0, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        verticalBoxSpriteFrameTileProperties.Add(self.checkboxSpriteFrameTileMirrorX, 0, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        verticalBoxSpriteFrameTileProperties.Add(self.checkboxSpriteFrameTileMirrorY, 0, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        verticalBoxSpriteFrameTileProperties.Add(horizontalBoxSpriteFrameTileOffsetX, 0, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        verticalBoxSpriteFrameTileProperties.Add(horizontalBoxSpriteFrameTileOffsetY, 0, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        verticalBoxSpriteFrameTileProperties.Add(horizontalBoxSpriteFrameTilePaletteIndex, 0, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        verticalBoxSpriteFrameTileProperties.Add(horizontalBoxSpriteFrameTileTilesetIndex, 0, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        verticalBoxSpriteFrameTileProperties.Add(horizontalBoxSpriteFrameTileByte1Index, 0, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        verticalBoxSpriteFrameTileProperties.Add(horizontalBoxSpriteFrameTileByte2Index, 0, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)

        horizontalBoxSpriteFrameTileEditor = wx.BoxSizer(wx.HORIZONTAL)
        horizontalBoxSpriteFrameTileEditor.Add(self.scrolledWindowMap, 0, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        horizontalBoxSpriteFrameTileEditor.Add(verticalBoxSpriteFrameTileProperties, 0, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        
        verticalBoxSpriteFrameImage = wx.BoxSizer(wx.VERTICAL)
        verticalBoxSpriteFrameImage.Add(horizontalBoxSpriteFrameTileSelection, 0, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        verticalBoxSpriteFrameImage.Add(horizontalBoxSpriteFrameTileEditor, 0, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)

        verticalBoxSpriteEditor = wx.BoxSizer(wx.VERTICAL)
        verticalBoxSpriteEditor.Add(verticalBoxSpriteFrame, 0, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        verticalBoxSpriteEditor.Add(verticalBoxSpriteFrameImage, 0, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)

        # create sprite image
        self.displayedSpriteImage = wx.StaticBitmap(self.scrolledWindowMap, wx.ID_ANY, wx.NullBitmap,
                                                    size=(self.SPRITE_IMAGE_PIXEL_WIDTH, self.SPRITE_IMAGE_PIXEL_HEIGHT))

        horizontalBox = wx.BoxSizer(wx.HORIZONTAL)
        horizontalBox.Add(verticalBoxSpritesets, 0, wx.EXPAND)
        horizontalBox.AddSpacer(10)
        horizontalBox.Add(verticalBoxSprites, 0, wx.EXPAND)
        horizontalBox.AddSpacer(10)
        horizontalBox.Add(verticalBoxSpriteEditor, 0, wx.EXPAND)
        
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
        self.spriteIndex = self.listBoxSprites.GetSelection()
        self.frameIndex = self.spritesetData.sprites[self.spriteIndex].frameData[0].frameId
        # update the sprite frame selection
        self.spinCtrlSpriteFrameCount.SetValue(len(self.spritesetData.sprites[self.spriteIndex].frameData))
        self.spinCtrlSpriteFrameCurrent.SetValue(1)
        self.spinCtrlSpriteFrameCurrent.SetMax(len(self.spritesetData.sprites[self.spriteIndex].frameData))
        
        # update sprite frame data
        self.updateSpriteFrame()

        pub.sendMessage("sprites_update_sprite", spriteFrameIndex=self.frameIndex)

    def onSpriteFrameSelectionChanged(self, event):
        spriteFrameIndex = self.spinCtrlSpriteFrameCurrent.GetValue() - 1
        self.frameIndex = self.spritesetData.sprites[self.spriteIndex].frameData[spriteFrameIndex].frameId
        pub.sendMessage("sprites_update_sprite", spriteFrameIndex=self.frameIndex)
        self.updateSpriteFrame()

    def onSpriteFrameTileSelectionChanged(self, event):
        self.spriteFrameTileIndex = self.spinCtrlSpriteFrameTileCurrent.GetValue() - 1
        self.updateSpriteFrameTile()

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

    def updateSpriteImage(self, spriteImage : PIL.Image.Image):
        magnification = 2
        magnificationX = self.SPRITE_IMAGE_PIXEL_WIDTH * magnification
        magnificationY = self.SPRITE_IMAGE_PIXEL_HEIGHT * magnification
        sizedImage = spriteImage.resize((magnificationX, magnificationY), PIL.Image.NEAREST)
        wx_image = wx.Image(sizedImage.size[0], sizedImage.size[1])
        wx_image.SetData(sizedImage.convert("RGB").tobytes())
        bitmap = wx.Bitmap(wx_image)
        self.displayedSpriteImage.SetBitmap(bitmap)

    def updateSpriteFrame(self):
        # update the selected sprite frame
        self.listBoxSpriteFrame.SetSelection(self.frameIndex)

        # update the sprite frame properties
        self.spinCtrlSpriteFrameDuration.SetValue(self.spritesetData.sprites[self.spriteIndex].frameData[0].duration)
        self.spinCtrlSpriteFrameOffsetX.SetValue(self.spritesetData.spriteFrames[self.frameIndex].offsetX)
        self.spinCtrlSpriteFrameOffsetY.SetValue(self.spritesetData.spriteFrames[self.frameIndex].offsetY)

        # update the sprite frame tile selection
        self.spinCtrlSpriteFrameTileCount.SetValue(self.spritesetData.spriteFrames[self.frameIndex].tileCount)
        self.spinCtrlSpriteFrameTileCurrent.SetValue(1)
        self.spinCtrlSpriteFrameTileCurrent.SetMax(self.spritesetData.spriteFrames[self.frameIndex].tileCount)
        self.spriteFrameTileIndex = 0

        self.updateSpriteFrameTile()
    
    def updateSpriteFrameTile(self):
        # update the sprite frame tile properties
        self.checkboxSpriteFrameTileCutout.SetValue(self.spritesetData.spriteFrames[self.frameIndex].tileData[self.spriteFrameTileIndex].tileCutout)
        self.checkboxSpriteFrameTileMirrorX.SetValue(self.spritesetData.spriteFrames[self.frameIndex].tileData[self.spriteFrameTileIndex].tileMirrorX)
        self.checkboxSpriteFrameTileMirrorY.SetValue(self.spritesetData.spriteFrames[self.frameIndex].tileData[self.spriteFrameTileIndex].tileMirrorY)
        self.spinCtrlSpriteFrameTileOffsetX.SetValue(self.spritesetData.spriteFrames[self.frameIndex].tileData[self.spriteFrameTileIndex].tileOffsetX)
        self.spinCtrlSpriteFrameTileOffsetY.SetValue(self.spritesetData.spriteFrames[self.frameIndex].tileData[self.spriteFrameTileIndex].tileOffsetY)
        self.spinCtrlSpriteFrameTilePaletteIndex.SetValue(self.spritesetData.spriteFrames[self.frameIndex].tileData[self.spriteFrameTileIndex].tilePaletteId)
        self.spinCtrlSpriteFrameTileTilesetIndex.SetValue(self.spritesetData.spriteFrames[self.frameIndex].tileData[self.spriteFrameTileIndex].tilesetId)
        self.spinCtrlSpriteFrameTileByte1Index.SetValue(hex(self.spritesetData.spriteFrames[self.frameIndex].tileData[self.spriteFrameTileIndex].byte1))
        self.spinCtrlSpriteFrameTileByte2Index.SetValue(hex(self.spritesetData.spriteFrames[self.frameIndex].tileData[self.spriteFrameTileIndex].byte2))


        
        
