# This file contains the View_MapTabProperties class, which is a panel that contains the properties of the map.
# This class is responsible for displaying the properties of the selected map.
import wx

from model.Model_Map import Model_Map

class View_MapTabProperties(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        # map name controls
        self.labelName = wx.StaticText(self, label="Name:")
        self.textCtrlName = wx.TextCtrl(self, value="", size=(200, 24))
        horizontalBoxName = wx.BoxSizer(wx.HORIZONTAL)
        horizontalBoxName.Add(self.labelName, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,)
        horizontalBoxName.Add(self.textCtrlName, wx.EXPAND|wx.ALL)

        # player status controls
        self.labelPlayerStatus = wx.StaticText(self, label="Player Status:")
        # player above map check box
        self.checkBoxPlayerAboveMap = wx.CheckBox(self, label="Player Above Map")
        # player enable fighting check box
        self.checkBoxPlayerEnableFighting = wx.CheckBox(self, label="Player Enable Fighting")
        # player invisible check box
        self.checkBoxPlayerInvisible = wx.CheckBox(self, label="Player Invisible")
        # player mirror horizontal check box
        self.checkBoxPlayerMirrorHorizontal = wx.CheckBox(self, label="Player Mirror Horizontal")
        # player mirror vertical check box
        self.checkBoxPlayerMirrorVertical = wx.CheckBox(self, label="Player Mirror Vertical")
        # player status vertical sizer
        verticalBoxPlayerStatus = wx.BoxSizer(wx.VERTICAL)
        verticalBoxPlayerStatus.Add(self.labelPlayerStatus, flag=wx.ALIGN_LEFT|wx.ALL)
        verticalBoxPlayerStatus.Add(self.checkBoxPlayerAboveMap, flag=wx.ALIGN_LEFT|wx.ALL)
        verticalBoxPlayerStatus.Add(self.checkBoxPlayerEnableFighting, flag=wx.ALIGN_LEFT|wx.ALL)
        verticalBoxPlayerStatus.Add(self.checkBoxPlayerInvisible, flag=wx.ALIGN_LEFT|wx.ALL)
        verticalBoxPlayerStatus.Add(self.checkBoxPlayerMirrorHorizontal, flag=wx.ALIGN_LEFT|wx.ALL)
        verticalBoxPlayerStatus.Add(self.checkBoxPlayerMirrorVertical, flag=wx.ALIGN_LEFT|wx.ALL)

        # room clearing rewards controls
        self.labelRoomClearingRewards = wx.StaticText(self, label="Room Clearing Rewards:")
        # room clearing rewards combobox
        self.comboBoxRoomClearingRewards = wx.ComboBox(self, style=wx.CB_DROPDOWN|wx.CB_READONLY)
        # add entries to combobox from class Model_RoomClearingRewards
        self.comboBoxRoomClearingRewards.Append("None")
        self.comboBoxRoomClearingRewards.Append("Power")
        self.comboBoxRoomClearingRewards.Append("Strength")
        self.comboBoxRoomClearingRewards.Append("Defense")
        # add combobox to horizontal sizer
        horizontalBoxRoomClearingRewards = wx.BoxSizer(wx.HORIZONTAL)
        horizontalBoxRoomClearingRewards.Add(self.labelRoomClearingRewards, flag=wx.ALIGN_LEFT|wx.ALL)
        horizontalBoxRoomClearingRewards.Add(self.comboBoxRoomClearingRewards, flag=wx.ALIGN_LEFT|wx.ALL)

        # screen settings controls
        self.labelScreenSettings = wx.StaticText(self, label="Screen Settings:")
        # screen settings spinctrl
        self.spinCtrlScreenSettings = wx.SpinCtrl(self, value="0", min=0, max=255, size=(50, -1))
        # add screen settings label and spinctrl to horizontal sizer
        horizontalBoxScreenSettings = wx.BoxSizer(wx.HORIZONTAL)
        horizontalBoxScreenSettings.Add(self.labelScreenSettings, flag=wx.ALIGN_LEFT|wx.ALL)
        horizontalBoxScreenSettings.Add(self.spinCtrlScreenSettings, flag=wx.ALIGN_LEFT|wx.ALL)
        # map data
        self.verticalBoxMapData = wx.BoxSizer(wx.VERTICAL)
        self.verticalBoxMapData.Add(horizontalBoxName)
        self.verticalBoxMapData.Add(verticalBoxPlayerStatus)
        self.verticalBoxMapData.Add(horizontalBoxRoomClearingRewards)
        self.verticalBoxMapData.Add(horizontalBoxScreenSettings)

        self.SetSizer(self.verticalBoxMapData)
        self.Fit()
    
    def update(self, mapData : Model_Map):
        # update map name
        self.textCtrlName.SetValue(mapData.events.displayedName)

        # update player status check boxes
        self.checkBoxPlayerAboveMap.SetValue(mapData.events.isPlayerAboveMap)
        self.checkBoxPlayerEnableFighting.SetValue(mapData.events.isPlayerFightEnabled)
        self.checkBoxPlayerInvisible.SetValue(mapData.events.isPlayerInvisible)
        self.checkBoxPlayerMirrorHorizontal.SetValue(mapData.events.isPlayerMirroredHorizontal)
        self.checkBoxPlayerMirrorVertical.SetValue(mapData.events.isPlayerMirroredVertical)
        
        # update room clearing rewards combobox
        self.comboBoxRoomClearingRewards.SetSelection(mapData.roomClearingReward)

        # update screen settings spinctrl
        if mapData.screenSettings is not None:
            self.spinCtrlScreenSettings.SetValue(mapData.mapDataScreenSettings[0].index)
        else:
            self.spinCtrlScreenSettings.SetValue(0)


