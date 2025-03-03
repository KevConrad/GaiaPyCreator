# This file contains the class that represents the Exits tab in the Map tab of the main window.
# This class is responsible for displaying the exit data of the selected map.
import wx
import wx.lib.scrolledpanel

from model.Model_Map import Model_Map

class View_MapTabExits(wx.Panel):
    EXITS_TAB_INDEX = 2

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        
        # exit selection controls
        horizontalBoxExitSelection = wx.BoxSizer(wx.HORIZONTAL)
        labelExitSelection = wx.StaticText(self, label="Exit: ")
        self.spinCtrlExitCurrent = wx.SpinCtrl(self, style=wx.SP_ARROW_KEYS)
        self.spinCtrlExitCurrent.SetMin(0)
        self.spinCtrlExitCurrent.SetMax(1024)
        self.spinCtrlExitCurrent.Bind(wx.EVT_SPINCTRL, self.onExitSelectionChanged)
        labelExitSelectionSlash = wx.StaticText(self, label=" / ")
        self.spinCtrlExitCount = wx.SpinCtrl(self, style=wx.SP_ARROW_KEYS)
        self.spinCtrlExitCount.SetMin(0)
        self.spinCtrlExitCount.SetMax(1024)
        horizontalBoxExitSelection.Add(labelExitSelection, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        horizontalBoxExitSelection.Add(self.spinCtrlExitCurrent, wx.EXPAND|wx.ALL)
        horizontalBoxExitSelection.Add(labelExitSelectionSlash, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        horizontalBoxExitSelection.Add(self.spinCtrlExitCount, wx.EXPAND|wx.ALL)

        # exit position controls
        horizontalBoxExitPosition = wx.BoxSizer(wx.HORIZONTAL)
        labelExitPositionX = wx.StaticText(self, label="Position X: ")
        self.spinCtrlExitPositionX = wx.SpinCtrl(self, style=wx.SP_ARROW_KEYS)
        self.spinCtrlExitPositionX.SetMin(0)
        self.spinCtrlExitPositionX.SetMax(1024)
        labelExitPositionY = wx.StaticText(self, label="Position Y: ")
        self.spinCtrlExitPositionY = wx.SpinCtrl(self, style=wx.SP_ARROW_KEYS)
        self.spinCtrlExitPositionY.SetMin(0)
        self.spinCtrlExitPositionY.SetMax(1024)
        horizontalBoxExitPosition.Add(labelExitPositionX, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        horizontalBoxExitPosition.Add(self.spinCtrlExitPositionX, wx.EXPAND|wx.ALL)
        horizontalBoxExitPosition.Add(labelExitPositionY, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        horizontalBoxExitPosition.Add(self.spinCtrlExitPositionY, wx.EXPAND|wx.ALL)

        # exit data
        self.verticalBoxExitData = wx.BoxSizer(wx.VERTICAL)
        labelExitData = wx.StaticText(self, label="Exit Data:")
        self.verticalBoxExitData.Add(labelExitData)
        self.verticalBoxExitData.Add(horizontalBoxExitSelection)
        self.verticalBoxExitData.Add(horizontalBoxExitPosition)

        self.SetSizer(self.verticalBoxExitData)
        self.Fit()

    def onExitSelectionChanged(self, event):
        self.updateSelectedExit(self.spinCtrlExitCurrent.GetValue())
    
    def update(self, mapData : Model_Map, exitIndex):
        self.mapData = mapData
        
        self.spinCtrlExitCurrent.SetValue(0)
        self.spinCtrlExitCount.SetValue(len(self.mapData.exits.exits))
        self.updateSelectedExit(exitIndex)

    def updateSelectedExit(self, exitIndex):
        if exitIndex < 0 or exitIndex >= len(self.mapData.exits.exits):
            return
        
        exitData = self.mapData.exits.exits[exitIndex]
        self.spinCtrlExitPositionX.SetValue(exitData.positionX)
        self.spinCtrlExitPositionY.SetValue(exitData.positionY)