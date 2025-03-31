# This file contains the View_MapTabEvents class, which is a panel that is displayed in the notebook of the main window. It allows the user to edit the event data of the map.
# This class is responsible for displaying the event data of the selected map.
import wx

from model.Model_Event import Model_Event
from model.Model_Map import Model_Map

from pubsub import pub

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

        # event data
        self.verticalBoxEventData = wx.BoxSizer(wx.VERTICAL)
        labelEventData = wx.StaticText(self, label="Event Data:")
        self.verticalBoxEventData.Add(labelEventData)
        self.verticalBoxEventData.Add(horizontalBoxEventSelection)
        self.verticalBoxEventData.Add(horizontalBoxEventPositionX)
        self.verticalBoxEventData.Add(horizontalBoxEventPositionY)
        self.verticalBoxEventData.Add(horizontalBoxEventType)

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

            if eventData.type == Model_Event.Type.enemy:
                self.checkBoxEventTypeEnemy.SetValue(True)
                self.checkBoxEventTypeNPC.SetValue(False)
            elif eventData.type == Model_Event.Type.npc:
                self.checkBoxEventTypeEnemy.SetValue(False)
                self.checkBoxEventTypeNPC.SetValue(True)
            else:
                self.checkBoxEventTypeEnemy.SetValue(False)
                self.checkBoxEventTypeNPC.SetValue(False)
        else:
            self.spinCtrlEventPositionX.SetValue(0)
            self.spinCtrlEventPositionY.SetValue(0)
            self.checkBoxEventTypeEnemy.SetValue(False)
            self.checkBoxEventTypeNPC.SetValue(False)