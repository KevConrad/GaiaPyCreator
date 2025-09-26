# This file contains the class that represents the tab for editing map treasures.
# This class is responsible for displaying the treasure data of the selected map.
import wx

from model.Model_Map import Model_Map

from pubsub import pub

class View_MapTabTreasures(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        
        # treasure selection controls
        horizontalBoxTreasureSelection = wx.BoxSizer(wx.HORIZONTAL)
        labelTreasureSelection = wx.StaticText(self, label="Treasure: ")
        self.spinCtrlTreasureCurrent = wx.SpinCtrl(self, style=wx.SP_ARROW_KEYS)
        self.spinCtrlTreasureCurrent.SetMin(0)
        self.spinCtrlTreasureCurrent.SetMax(1024)
        self.spinCtrlTreasureCurrent.Bind(wx.EVT_SPINCTRL, self.onTreasureSelectionChanged)
        labelTreasureSelectionSlash = wx.StaticText(self, label=" / ")
        self.spinCtrlTreasureCount = wx.SpinCtrl(self, style=wx.SP_ARROW_KEYS)
        self.spinCtrlTreasureCount.SetMin(0)
        self.spinCtrlTreasureCount.SetMax(1024)
        horizontalBoxTreasureSelection.Add(labelTreasureSelection, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        horizontalBoxTreasureSelection.Add(self.spinCtrlTreasureCurrent, wx.EXPAND|wx.ALL)
        horizontalBoxTreasureSelection.Add(labelTreasureSelectionSlash, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        horizontalBoxTreasureSelection.Add(self.spinCtrlTreasureCount, wx.EXPAND|wx.ALL)

        # treasure x position controls
        horizontalBoxTreasurePositionX = wx.BoxSizer(wx.HORIZONTAL)
        labelTreasurePositionX = wx.StaticText(self, label="Position X: ")
        self.spinCtrlTreasurePositionX = wx.SpinCtrl(self, style=wx.SP_ARROW_KEYS)
        self.spinCtrlTreasurePositionX.SetMin(0)
        self.spinCtrlTreasurePositionX.SetMax(1024)
        horizontalBoxTreasurePositionX.Add(labelTreasurePositionX, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        horizontalBoxTreasurePositionX.Add(self.spinCtrlTreasurePositionX, wx.EXPAND|wx.ALL)

        # treasure y position controls
        horizontalBoxTreasurePositionY = wx.BoxSizer(wx.HORIZONTAL)
        labelTreasurePositionY = wx.StaticText(self, label="Position Y: ")
        self.spinCtrlTreasurePositionY = wx.SpinCtrl(self, style=wx.SP_ARROW_KEYS)
        self.spinCtrlTreasurePositionY.SetMin(0)
        self.spinCtrlTreasurePositionY.SetMax(1024)
        horizontalBoxTreasurePositionY.Add(labelTreasurePositionY, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        horizontalBoxTreasurePositionY.Add(self.spinCtrlTreasurePositionY, wx.EXPAND|wx.ALL)

        # treasure item index controls
        horizontalBoxTreasureItemIndex = wx.BoxSizer(wx.HORIZONTAL)
        labelTreasureItemIndex = wx.StaticText(self, label="Item Index: ")
        self.spinCtrlTreasureItemIndex = wx.SpinCtrl(self, style=wx.SP_ARROW_KEYS)
        self.spinCtrlTreasureItemIndex.SetMin(0)
        self.spinCtrlTreasureItemIndex.SetMax(255)
        horizontalBoxTreasureItemIndex.Add(labelTreasureItemIndex, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        horizontalBoxTreasureItemIndex.Add(self.spinCtrlTreasureItemIndex, wx.EXPAND|wx.ALL)

        # treasure item play music checkbox
        horizontalBoxTreasurePlayMusic = wx.BoxSizer(wx.HORIZONTAL)
        self.checkBoxTreasurePlayMusic = wx.CheckBox(self, label="Play Music: ")
        horizontalBoxTreasurePlayMusic.Add(self.checkBoxTreasurePlayMusic, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)

        # treasure data
        self.verticalBoxTreasureData = wx.BoxSizer(wx.VERTICAL)
        self.verticalBoxTreasureData.Add(horizontalBoxTreasureSelection)
        self.verticalBoxTreasureData.Add(horizontalBoxTreasurePositionX)
        self.verticalBoxTreasureData.Add(horizontalBoxTreasurePositionY)
        self.verticalBoxTreasureData.Add(horizontalBoxTreasureItemIndex)
        self.verticalBoxTreasureData.Add(horizontalBoxTreasurePlayMusic)

        self.SetSizer(self.verticalBoxTreasureData)
        self.Fit()

    def onTreasureSelectionChanged(self, event):
        treasureIndex = self.spinCtrlTreasureCurrent.GetValue() - 1
        self.updateSelectedTreasure(treasureIndex)
        pub.sendMessage("maps_update_treasure", selectedTreasureIndex = treasureIndex)

    def update(self, mapData : Model_Map):
        self.mapData = mapData
        
        self.spinCtrlTreasureCurrent.SetMax(len(self.mapData.treasures.treasures))

        if (len(self.mapData.treasures.treasures) > 0):
            self.spinCtrlTreasureCurrent.SetMin(1)
            self.spinCtrlTreasureCurrent.SetValue(1)
            self.updateSelectedTreasure(0)
        else:
            self.spinCtrlTreasureCurrent.SetMin(0)
            self.spinCtrlTreasureCurrent.SetValue(0)
            self.updateSelectedTreasure(-1)
        
        self.spinCtrlTreasureCount.SetValue(len(self.mapData.treasures.treasures))

    def updateSelectedTreasure(self, treasureIndex):
        if (treasureIndex >= 0):
            treasureData = self.mapData.treasures.treasures[treasureIndex]
            self.spinCtrlTreasurePositionX.Enable()
            self.spinCtrlTreasurePositionX.SetValue(treasureData.positionX)
            self.spinCtrlTreasurePositionY.Enable()
            self.spinCtrlTreasurePositionY.SetValue(treasureData.positionY)
            self.spinCtrlTreasureItemIndex.Enable()
            self.spinCtrlTreasureItemIndex.SetValue(treasureData.itemIndex)
            self.checkBoxTreasurePlayMusic.Enable()
            self.checkBoxTreasurePlayMusic.SetValue(treasureData.isMusicPlayed)
        else:
            self.spinCtrlTreasurePositionX.SetValue(0)
            self.spinCtrlTreasurePositionX.Disable()
            self.spinCtrlTreasurePositionY.SetValue(0)
            self.spinCtrlTreasurePositionY.Disable()
            self.spinCtrlTreasureItemIndex.SetValue(0)
            self.spinCtrlTreasureItemIndex.Disable()
            self.checkBoxTreasurePlayMusic.SetValue(False)
            self.checkBoxTreasurePlayMusic.Disable()