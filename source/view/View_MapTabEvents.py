# This file contains the View_MapTabEvents class, which is a panel that is displayed in the notebook of the main window. It allows the user to edit the event data of the map.
# This class is responsible for displaying the event data of the selected map.
import wx

from model.Model_Event import Model_Event
from model.Model_Map import Model_Map

from pubsub import pub

class TabEventEnemy(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        
        # defeat action controls
        horizontalBoxDefeatAction = wx.BoxSizer(wx.HORIZONTAL)
        labelDefeatAction = wx.StaticText(self, label="Defeat Action: ")
        self.spinCtrlDefeatAction = wx.SpinCtrl(self, style=wx.SP_ARROW_KEYS)
        self.spinCtrlDefeatAction.SetMin(0)
        self.spinCtrlDefeatAction.SetMax(255)
        horizontalBoxDefeatAction.Add(labelDefeatAction, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        horizontalBoxDefeatAction.Add(self.spinCtrlDefeatAction, wx.EXPAND|wx.ALL)

        # unknown byte controls
        horizontalBoxUnknownByte = wx.BoxSizer(wx.HORIZONTAL)
        labelUnkownByte = wx.StaticText(self, label="Unkown Byte: ")
        self.spinCtrlUnknownByte = wx.SpinCtrl(self, style=wx.SP_ARROW_KEYS)
        self.spinCtrlUnknownByte.SetMin(0)
        self.spinCtrlUnknownByte.SetMax(255)
        horizontalBoxUnknownByte.Add(labelUnkownByte, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        horizontalBoxUnknownByte.Add(self.spinCtrlUnknownByte, wx.EXPAND|wx.ALL)

        # enemy state controls
        horizontalBoxEnemyState = wx.BoxSizer(wx.HORIZONTAL)
        labelEnemyState = wx.StaticText(self, label="Enemy State: ")
        self.spinCtrlEnemyState = wx.SpinCtrl(self, style=wx.SP_ARROW_KEYS)
        self.spinCtrlEnemyState.SetMin(0)
        self.spinCtrlEnemyState.SetMax(255)
        horizontalBoxEnemyState.Add(labelEnemyState, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        horizontalBoxEnemyState.Add(self.spinCtrlEnemyState, wx.EXPAND|wx.ALL)

        # event type enemy data
        self.verticalBoxEnemyData = wx.BoxSizer(wx.VERTICAL)
        self.verticalBoxEnemyData.Add(horizontalBoxDefeatAction)
        self.verticalBoxEnemyData.Add(horizontalBoxUnknownByte)
        self.verticalBoxEnemyData.Add(horizontalBoxEnemyState)
        self.SetSizer(self.verticalBoxEnemyData)
        self.Fit()

class TabEventNpc(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        # unknown byte controls
        horizontalBoxUnknownByte = wx.BoxSizer(wx.HORIZONTAL)
        labelUnkownByte = wx.StaticText(self, label="Unkown Byte: ")
        self.spinCtrlUnknownByte = wx.SpinCtrl(self, style=wx.SP_ARROW_KEYS)
        self.spinCtrlUnknownByte.SetMin(0)
        self.spinCtrlUnknownByte.SetMax(255)
        horizontalBoxUnknownByte.Add(labelUnkownByte, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        horizontalBoxUnknownByte.Add(self.spinCtrlUnknownByte, wx.EXPAND|wx.ALL)

        # event type NPC data
        self.verticalBoxNpcData = wx.BoxSizer(wx.VERTICAL)
        self.verticalBoxNpcData.Add(horizontalBoxUnknownByte)
        self.SetSizer(self.verticalBoxNpcData)
        self.Fit()

class View_MapTabEvents(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        
        # event selection controls
        horizontalBoxEventSelection = wx.BoxSizer(wx.HORIZONTAL)
        labelEventSelection = wx.StaticText(self, label="Event: ")
        self.spinCtrlEventCurrent = wx.SpinCtrl(self, style=wx.SP_ARROW_KEYS)
        self.spinCtrlEventCurrent.SetMin(0)
        self.spinCtrlEventCurrent.SetMax(1024)
        self.spinCtrlEventCurrent.Bind(wx.EVT_SPINCTRL, self.onEventSelectionChanged)
        labelEventSelectionSlash = wx.StaticText(self, label=" / ")
        self.spinCtrlEventCount = wx.SpinCtrl(self, style=wx.SP_ARROW_KEYS)
        self.spinCtrlEventCount.SetMin(0)
        self.spinCtrlEventCount.SetMax(1024)
        horizontalBoxEventSelection.Add(labelEventSelection, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        horizontalBoxEventSelection.Add(self.spinCtrlEventCurrent, wx.EXPAND|wx.ALL)
        horizontalBoxEventSelection.Add(labelEventSelectionSlash, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        horizontalBoxEventSelection.Add(self.spinCtrlEventCount, wx.EXPAND|wx.ALL)

        # event x position controls
        horizontalBoxEventPositionX = wx.BoxSizer(wx.HORIZONTAL)
        labelEventPositionX = wx.StaticText(self, label="Position X: ")
        self.spinCtrlEventPositionX = wx.SpinCtrl(self, style=wx.SP_ARROW_KEYS)
        self.spinCtrlEventPositionX.SetMin(0)
        self.spinCtrlEventPositionX.SetMax(1024)
        horizontalBoxEventPositionX.Add(labelEventPositionX, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        horizontalBoxEventPositionX.Add(self.spinCtrlEventPositionX, wx.EXPAND|wx.ALL)

        # event y position controls
        horizontalBoxEventPositionY = wx.BoxSizer(wx.HORIZONTAL)
        labelEventPositionY = wx.StaticText(self, label="Position Y: ")
        self.spinCtrlEventPositionY = wx.SpinCtrl(self, style=wx.SP_ARROW_KEYS)
        self.spinCtrlEventPositionY.SetMin(0)
        self.spinCtrlEventPositionY.SetMax(1024)
        horizontalBoxEventPositionY.Add(labelEventPositionY, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        horizontalBoxEventPositionY.Add(self.spinCtrlEventPositionY, wx.EXPAND|wx.ALL)
        
        # event type controls
        horizontalBoxEventType = wx.BoxSizer(wx.HORIZONTAL)
        labelEventType = wx.StaticText(self, label="Type: ")
        labelEventTypeEnemy = wx.StaticText(self, label="Enemy")
        self.checkBoxEventTypeEnemy = wx.CheckBox(self)
        labelEventTypeNPC = wx.StaticText(self, label="NPC")
        self.checkBoxEventTypeNPC = wx.CheckBox(self)
        horizontalBoxEventType.Add(labelEventType, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        horizontalBoxEventType.Add(labelEventTypeEnemy, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        horizontalBoxEventType.Add(self.checkBoxEventTypeEnemy, wx.EXPAND|wx.ALL)
        horizontalBoxEventType.Add(labelEventTypeNPC, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        horizontalBoxEventType.Add(self.checkBoxEventTypeNPC, wx.EXPAND|wx.ALL)

        # event type tabControls
        self.eventTypeTabs = wx.Notebook(self, size=(400, 400))

        # Initiation of the tab windows:
        self.tabEventEnemy = TabEventEnemy(self.eventTypeTabs)
        self.tabEventNpc = TabEventNpc(self.eventTypeTabs)

        # Assigning names to tabs and adding them:
        self.eventTypeTabs.AddPage(self.tabEventEnemy, "Enemy")
        self.eventTypeTabs.AddPage(self.tabEventNpc, "NPC")

        # event data
        self.verticalBoxEventData = wx.BoxSizer(wx.VERTICAL)
        self.verticalBoxEventData.Add(horizontalBoxEventSelection)
        self.verticalBoxEventData.Add(horizontalBoxEventPositionX)
        self.verticalBoxEventData.Add(horizontalBoxEventPositionY)
        self.verticalBoxEventData.Add(horizontalBoxEventType)
        self.verticalBoxEventData.Add(self.eventTypeTabs)

        self.SetSizer(self.verticalBoxEventData)
        self.Fit()

    def onEventSelectionChanged(self, event):
        eventIndex = self.spinCtrlEventCurrent.GetValue() - 1
        self.updateSelectedEvent(eventIndex)
        pub.sendMessage("maps_update_event", selectedEventIndex = eventIndex)

    def update(self, mapData : Model_Map):
        self.mapData = mapData

        if (len(self.mapData.events.events) > 0):
            self.spinCtrlEventCurrent.SetMin(1)
            self.spinCtrlEventCurrent.SetValue(1)
            self.updateSelectedEvent(0)
        else:
            self.spinCtrlEventCurrent.SetMin(0)
            self.spinCtrlEventCurrent.SetValue(0)
            self.updateSelectedEvent(-1)

        self.spinCtrlEventCurrent.SetMax(len(self.mapData.events.events))
        self.spinCtrlEventCount.SetValue(len(self.mapData.events.events))

    def updateSelectedEvent(self, eventIndex):
        if (eventIndex >= 0):
            eventData = self.mapData.events.events[eventIndex]
            self.spinCtrlEventPositionX.SetValue(eventData.positionX)
            self.spinCtrlEventPositionY.SetValue(eventData.positionY)

            if eventData.type == Model_Event.TYPE_ENEMY:
                self.checkBoxEventTypeEnemy.SetValue(True)
                self.checkBoxEventTypeNPC.SetValue(False)

                # enable enemy and disable NPC tab
                self.tabEventEnemy.Enable()
                self.tabEventNpc.Disable()
                self.eventTypeTabs.SetSelection(0)

                # update enemy tab data
                self.tabEventEnemy.spinCtrlDefeatAction.SetValue(eventData.enemyDefeatActionId)
                self.tabEventEnemy.spinCtrlUnknownByte.SetValue(eventData.eventByte)
                self.tabEventEnemy.spinCtrlEnemyState.SetValue(eventData.enemyStateId)
            else:   # event type is NPC
                self.checkBoxEventTypeEnemy.SetValue(False)
                self.checkBoxEventTypeNPC.SetValue(True)

                # enable NPC and disable enemy tab
                self.tabEventEnemy.Disable()
                self.tabEventNpc.Enable()
                self.eventTypeTabs.SetSelection(1)

                # update NPC tab data
                self.tabEventNpc.spinCtrlUnknownByte.SetValue(eventData.eventByte)
        else:
            self.spinCtrlEventPositionX.SetValue(0)
            self.spinCtrlEventPositionY.SetValue(0)
            self.checkBoxEventTypeEnemy.SetValue(False)
            self.checkBoxEventTypeNPC.SetValue(False)