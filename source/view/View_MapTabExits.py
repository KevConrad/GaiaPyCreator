# This file contains the class that represents the Exits tab in the Map tab of the main window.
# This class is responsible for displaying the exit data of the selected map.
import wx

from model.Model_MapExit import Model_MapExit
from model.Model_Map import Model_Map

class View_MapTabExits(wx.Panel):

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

        # exit x position controls
        horizontalBoxExitPositionX = wx.BoxSizer(wx.HORIZONTAL)
        labelExitPositionX = wx.StaticText(self, label="Position X: ")
        self.spinCtrlExitPositionX = wx.SpinCtrl(self, style=wx.SP_ARROW_KEYS)
        self.spinCtrlExitPositionX.SetMin(0)
        self.spinCtrlExitPositionX.SetMax(1024)
        horizontalBoxExitPositionX.Add(labelExitPositionX, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        horizontalBoxExitPositionX.Add(self.spinCtrlExitPositionX, wx.EXPAND|wx.ALL)

        # exit y position controls
        horizontalBoxExitPositionY = wx.BoxSizer(wx.HORIZONTAL)
        labelExitPositionY = wx.StaticText(self, label="Position Y: ")
        self.spinCtrlExitPositionY = wx.SpinCtrl(self, style=wx.SP_ARROW_KEYS)
        self.spinCtrlExitPositionY.SetMin(0)
        self.spinCtrlExitPositionY.SetMax(1024)
        horizontalBoxExitPositionY.Add(labelExitPositionY, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        horizontalBoxExitPositionY.Add(self.spinCtrlExitPositionY, wx.EXPAND|wx.ALL)

        # exit width controls
        horizontalBoxExitWidth = wx.BoxSizer(wx.HORIZONTAL)
        labelExitWidth = wx.StaticText(self, label="Width: ")
        self.spinCtrlExitWidth = wx.SpinCtrl(self, style=wx.SP_ARROW_KEYS)
        self.spinCtrlExitWidth.SetMin(0)
        self.spinCtrlExitWidth.SetMax(1024)
        horizontalBoxExitWidth.Add(labelExitWidth, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        horizontalBoxExitWidth.Add(self.spinCtrlExitWidth, wx.EXPAND|wx.ALL)

        # exit height controls
        horizontalBoxExitHeight = wx.BoxSizer(wx.HORIZONTAL)
        labelExitHeight = wx.StaticText(self, label="Height: ")
        self.spinCtrlExitHeight = wx.SpinCtrl(self, style=wx.SP_ARROW_KEYS)
        self.spinCtrlExitHeight.SetMin(0)
        self.spinCtrlExitHeight.SetMax(1024)
        horizontalBoxExitHeight.Add(labelExitHeight, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        horizontalBoxExitHeight.Add(self.spinCtrlExitHeight, wx.EXPAND|wx.ALL)
        
        # edit type controls
        horizontalBoxExitType = wx.BoxSizer(wx.HORIZONTAL)
        labelExitType = wx.StaticText(self, label="Type: ")
        labelExitTypeTeleport = wx.StaticText(self, label="Teleport")
        self.checkBoxExitTypeTeleport = wx.CheckBox(self)
        labelExitTypeStairs = wx.StaticText(self, label="Stairs")
        self.checkBoxExitTypeStairs = wx.CheckBox(self)
        horizontalBoxExitType.Add(labelExitType, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        horizontalBoxExitType.Add(labelExitTypeTeleport, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        horizontalBoxExitType.Add(self.checkBoxExitTypeTeleport, wx.EXPAND|wx.ALL)
        horizontalBoxExitType.Add(labelExitTypeStairs, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        horizontalBoxExitType.Add(self.checkBoxExitTypeStairs, wx.EXPAND|wx.ALL)

        # exit data
        self.verticalBoxExitData = wx.BoxSizer(wx.VERTICAL)
        labelExitData = wx.StaticText(self, label="Exit Data:")
        self.verticalBoxExitData.Add(labelExitData)
        self.verticalBoxExitData.Add(horizontalBoxExitSelection)
        self.verticalBoxExitData.Add(horizontalBoxExitPositionX)
        self.verticalBoxExitData.Add(horizontalBoxExitPositionY)
        self.verticalBoxExitData.Add(horizontalBoxExitWidth)
        self.verticalBoxExitData.Add(horizontalBoxExitHeight)
        self.verticalBoxExitData.Add(horizontalBoxExitType)

        self.SetSizer(self.verticalBoxExitData)
        self.Fit()

    def onExitSelectionChanged(self, event):
        self.updateSelectedExit(self.spinCtrlExitCurrent.GetValue())
    
    def update(self, mapData : Model_Map):
        self.mapData = mapData
        
        if (len(self.mapData.exits.exits) > 0):
            self.spinCtrlExitCurrent.SetMin(1)
            self.spinCtrlExitCurrent.SetValue(1)
            self.updateSelectedExit(1)
        else:
            self.spinCtrlExitCurrent.SetMin(0)
            self.spinCtrlExitCurrent.SetValue(0)
            self.updateSelectedExit(0)
        
        self.spinCtrlExitCurrent.SetMax(len(self.mapData.exits.exits))
        self.spinCtrlExitCount.SetValue(len(self.mapData.exits.exits))
        
    def updateSelectedExit(self, exitIndex):
        if exitIndex < 0 or exitIndex > len(self.mapData.exits.exits):
            return
        
        if (exitIndex > 0):
            exitIndex -= 1
            exitData = self.mapData.exits.exits[exitIndex]
            self.spinCtrlExitPositionX.SetValue(exitData.positionX)
            self.spinCtrlExitPositionY.SetValue(exitData.positionY)
            self.spinCtrlExitWidth.SetValue(exitData.width)
            self.spinCtrlExitHeight.SetValue(exitData.height)

            if exitData.type == Model_MapExit.ExitType.TELEPORT:
                self.checkBoxExitTypeTeleport.SetValue(True)
                self.checkBoxExitTypeStairs.SetValue(False)
            elif exitData.type == Model_MapExit.ExitType.STAIRS:
                self.checkBoxExitTypeTeleport.SetValue(False)
                self.checkBoxExitTypeStairs.SetValue(True)
            else:
                self.checkBoxExitTypeTeleport.SetValue(False)
                self.checkBoxExitTypeStairs.SetValue(False)
        else:
            self.spinCtrlExitPositionX.SetValue(0)
            self.spinCtrlExitPositionY.SetValue(0)
            self.spinCtrlExitWidth.SetValue(0)
            self.spinCtrlExitHeight.SetValue(0)
            self.checkBoxExitTypeTeleport.SetValue(False)
            self.checkBoxExitTypeStairs.SetValue(False)