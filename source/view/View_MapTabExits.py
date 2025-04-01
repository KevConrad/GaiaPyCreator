# This file contains the class that represents the Exits tab in the Map tab of the main window.
# This class is responsible for displaying the exit data of the selected map.
import wx

from model.Model_MapExit import Model_MapExit
from model.Model_Map import Model_Map

from pubsub import pub

class TabExitStairs(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        text = wx.StaticText(self, -1, "Exit Stairs Data.", (20,20))

class TabExitTeleport(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        
        # map destination combobox
        horizontalBoxMapDestination = wx.BoxSizer(wx.HORIZONTAL)
        labelMapDestination = wx.StaticText(self, label="Map Destination: ")
        self.comboBoxMapDestination = wx.ComboBox(self, style=wx.CB_DROPDOWN)
        horizontalBoxMapDestination.Add(labelMapDestination, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        horizontalBoxMapDestination.Add(self.comboBoxMapDestination, wx.EXPAND|wx.ALL)

        # map position x controls
        horizontalBoxMapPositionX = wx.BoxSizer(wx.HORIZONTAL)
        labelMapPositionX = wx.StaticText(self, label="Position X: ")
        self.spinCtrlMapPositionX = wx.SpinCtrl(self, style=wx.SP_ARROW_KEYS)
        self.spinCtrlMapPositionX.SetMin(0)
        self.spinCtrlMapPositionX.SetMax(1024)
        horizontalBoxMapPositionX.Add(labelMapPositionX, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        horizontalBoxMapPositionX.Add(self.spinCtrlMapPositionX, wx.EXPAND|wx.ALL)

        # map pixel offset x controls
        horizontalBoxMapPixelOffsetX = wx.BoxSizer(wx.HORIZONTAL)
        labelMapPixelOffsetX = wx.StaticText(self, label="Pixel Offset X: ")
        self.spinCtrlMapPixelOffsetX = wx.SpinCtrl(self, style=wx.SP_ARROW_KEYS)
        self.spinCtrlMapPixelOffsetX.SetMin(0)
        self.spinCtrlMapPixelOffsetX.SetMax(15)
        horizontalBoxMapPixelOffsetX.Add(labelMapPixelOffsetX, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        horizontalBoxMapPixelOffsetX.Add(self.spinCtrlMapPixelOffsetX, wx.EXPAND|wx.ALL)
        
        # map position y controls
        horizontalBoxMapPositionY = wx.BoxSizer(wx.HORIZONTAL)
        labelMapPositionY = wx.StaticText(self, label="Position Y: ")
        self.spinCtrlMapPositionY = wx.SpinCtrl(self, style=wx.SP_ARROW_KEYS)
        self.spinCtrlMapPositionY.SetMin(0)
        self.spinCtrlMapPositionY.SetMax(1024)
        horizontalBoxMapPositionY.Add(labelMapPositionY, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        horizontalBoxMapPositionY.Add(self.spinCtrlMapPositionY, wx.EXPAND|wx.ALL)

        # map pixel offset y controls
        horizontalBoxMapPixelOffsetY = wx.BoxSizer(wx.HORIZONTAL)
        labelMapPixelOffsetY = wx.StaticText(self, label="Pixel Offset Y: ")
        self.spinCtrlMapPixelOffsetY = wx.SpinCtrl(self, style=wx.SP_ARROW_KEYS)
        self.spinCtrlMapPixelOffsetY.SetMin(0)
        self.spinCtrlMapPixelOffsetY.SetMax(15)
        horizontalBoxMapPixelOffsetY.Add(labelMapPixelOffsetY, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        horizontalBoxMapPixelOffsetY.Add(self.spinCtrlMapPixelOffsetY, wx.EXPAND|wx.ALL)

        # map player direction controls
        horizontalBoxMapPlayerDirection = wx.BoxSizer(wx.HORIZONTAL)
        labelMapPlayerDirection = wx.StaticText(self, label="Player Direction: ")
        self.comboBoxMapPlayerDirection = wx.ComboBox(self, style=wx.CB_DROPDOWN)
        self.comboBoxMapPlayerDirection.Append("Down")
        self.comboBoxMapPlayerDirection.Append("Left")
        self.comboBoxMapPlayerDirection.Append("Right")
        self.comboBoxMapPlayerDirection.Append("Up")
        horizontalBoxMapPlayerDirection.Add(labelMapPlayerDirection, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        horizontalBoxMapPlayerDirection.Add(self.comboBoxMapPlayerDirection, wx.EXPAND|wx.ALL)

        # map screen offset controls
        horizontalBoxMapScreenOffset = wx.BoxSizer(wx.HORIZONTAL) 
        labelMapScreenOffset = wx.StaticText(self, label="Screen Offset: ")
        self.spinCtrlMapScreenOffset = wx.SpinCtrl(self, style=wx.SP_ARROW_KEYS)
        self.spinCtrlMapScreenOffset.SetMin(0)
        self.spinCtrlMapScreenOffset.SetMax(1024)
        horizontalBoxMapScreenOffset.Add(labelMapScreenOffset, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        horizontalBoxMapScreenOffset.Add(self.spinCtrlMapScreenOffset, wx.EXPAND|wx.ALL)

        # map size X controls
        horizontalBoxMapSizeX = wx.BoxSizer(wx.HORIZONTAL)
        labelMapSizeX = wx.StaticText(self, label="Map Size X: ")
        self.spinCtrlMapSizeX = wx.SpinCtrl(self, style=wx.SP_ARROW_KEYS)
        self.spinCtrlMapSizeX.SetMin(0)
        self.spinCtrlMapSizeX.SetMax(1024)
        horizontalBoxMapSizeX.Add(labelMapSizeX, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        horizontalBoxMapSizeX.Add(self.spinCtrlMapSizeX, wx.EXPAND|wx.ALL)

        # map size Y controls
        horizontalBoxMapSizeY = wx.BoxSizer(wx.HORIZONTAL)
        labelMapSizeY = wx.StaticText(self, label="Map Size Y: ")
        self.spinCtrlMapSizeY = wx.SpinCtrl(self, style=wx.SP_ARROW_KEYS)
        self.spinCtrlMapSizeY.SetMin(0)
        self.spinCtrlMapSizeY.SetMax(1024)
        horizontalBoxMapSizeY.Add(labelMapSizeY, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        horizontalBoxMapSizeY.Add(self.spinCtrlMapSizeY, wx.EXPAND|wx.ALL)

        # exit data
        self.verticalBoxExitTeleportData = wx.BoxSizer(wx.VERTICAL)
        self.verticalBoxExitTeleportData.Add(horizontalBoxMapDestination)
        self.verticalBoxExitTeleportData.Add(horizontalBoxMapPositionX)
        self.verticalBoxExitTeleportData.Add(horizontalBoxMapPixelOffsetX)
        self.verticalBoxExitTeleportData.Add(horizontalBoxMapPositionY)
        self.verticalBoxExitTeleportData.Add(horizontalBoxMapPixelOffsetY)
        self.verticalBoxExitTeleportData.Add(horizontalBoxMapPlayerDirection)
        self.verticalBoxExitTeleportData.Add(horizontalBoxMapScreenOffset)
        self.verticalBoxExitTeleportData.Add(horizontalBoxMapSizeX)
        self.verticalBoxExitTeleportData.Add(horizontalBoxMapSizeY)

        self.SetSizer(self.verticalBoxExitTeleportData)
        self.Fit()

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
        
        # exit type controls
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

        # exit type tabControls
        self.exitTypeTabs = wx.Notebook(self, size=(400, 400))

        # Initiation of the tab windows:
        self.tabExitStairs = TabExitStairs(self.exitTypeTabs)
        self.tabExitTeleport = TabExitTeleport(self.exitTypeTabs)

        # Assigning names to tabs and adding them:
        self.exitTypeTabs.AddPage(self.tabExitStairs, "Stairs")
        self.exitTypeTabs.AddPage(self.tabExitTeleport, "Teleport")

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
        self.verticalBoxExitData.Add(self.exitTypeTabs)

        self.SetSizer(self.verticalBoxExitData)
        self.Fit()

    def load(self, mapNames):
        self.tabExitTeleport.comboBoxMapDestination.Set(mapNames)

    def onExitSelectionChanged(self, event):
        exitIndex = self.spinCtrlExitCurrent.GetValue() - 1
        self.updateSelectedExit(exitIndex)
        pub.sendMessage("maps_update_exit", selectedExitIndex = exitIndex)
    
    def update(self, mapData : Model_Map):
        self.mapData = mapData
        
        self.spinCtrlExitCurrent.SetMax(len(self.mapData.exits.exits))

        if (len(self.mapData.exits.exits) > 0):
            self.spinCtrlExitCurrent.SetMin(1)
            self.spinCtrlExitCurrent.SetValue(1)
            self.updateSelectedExit(0)
        else:
            self.spinCtrlExitCurrent.SetMin(0)
            self.spinCtrlExitCurrent.SetValue(0)
            self.updateSelectedExit(-1)
        
        self.spinCtrlExitCount.SetValue(len(self.mapData.exits.exits))
        
    def updateSelectedExit(self, exitIndex):
        if (exitIndex >= 0):
            exitData = self.mapData.exits.exits[exitIndex]
            self.spinCtrlExitPositionX.SetValue(exitData.positionX)
            self.spinCtrlExitPositionY.SetValue(exitData.positionY)
            self.spinCtrlExitWidth.SetValue(exitData.width)
            self.spinCtrlExitHeight.SetValue(exitData.height)

            if exitData.type == Model_MapExit.ExitType.STAIRS:
                self.checkBoxExitTypeTeleport.SetValue(False)
                self.checkBoxExitTypeStairs.SetValue(True)
                # disable teleport tab
                self.tabExitStairs.Enable()
                self.tabExitTeleport.Disable()
                self.exitTypeTabs.SetSelection(0)
            elif exitData.type == Model_MapExit.ExitType.TELEPORT:
                self.checkBoxExitTypeStairs.SetValue(False)
                self.checkBoxExitTypeTeleport.SetValue(True)
                self.tabExitTeleport.comboBoxMapDestination.SetSelection(exitData.destinationMapId)
                self.tabExitTeleport.spinCtrlMapPositionX.SetValue(exitData.destinationX)
                self.tabExitTeleport.spinCtrlMapPixelOffsetX.SetValue(exitData.destinationPixelOffsetX)
                self.tabExitTeleport.spinCtrlMapPositionY.SetValue(exitData.destinationY)
                self.tabExitTeleport.spinCtrlMapPixelOffsetY.SetValue(exitData.destinationPixelOffsetY)
                self.tabExitTeleport.comboBoxMapPlayerDirection.SetSelection(exitData.playerDirection)
                self.tabExitTeleport.spinCtrlMapScreenOffset.SetValue(exitData.screenOffset)
                self.tabExitTeleport.spinCtrlMapSizeX.SetValue(exitData.mapSizeX)
                self.tabExitTeleport.spinCtrlMapSizeY.SetValue(exitData.mapSizeY)

                # disable stairs tab
                self.tabExitStairs.Disable()
                self.tabExitTeleport.Enable()
                self.exitTypeTabs.SetSelection(1)
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