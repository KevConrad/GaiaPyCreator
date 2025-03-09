# This file contains the View_MapTabEvents class, which is a panel that is displayed in the notebook of the main window. It allows the user to edit the event data of the map.
# This class is responsible for displaying the event data of the selected map.
import wx
import wx.lib.scrolledpanel

from model.Model_Map import Model_Map

class View_MapTabEvents(wx.Panel):
    EVENTS_TAB_INDEX = 1

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        
        # event selection controls
        horizontalBoxEventSelection = wx.BoxSizer(wx.HORIZONTAL)
        labelEventSelection = wx.StaticText(self, label="Event: ")
        self.spinCtrlEventCurrent = wx.SpinCtrl(self, style=wx.SP_ARROW_KEYS)
        self.spinCtrlEventCurrent.SetMin(0)
        self.spinCtrlEventCurrent.SetMax(1024)
        labelEventSelectionSlash = wx.StaticText(self, label=" / ")
        self.spinCtrlEventCount = wx.SpinCtrl(self, style=wx.SP_ARROW_KEYS)
        self.spinCtrlEventCount.SetMin(0)
        self.spinCtrlEventCount.SetMax(1024)
        horizontalBoxEventSelection.Add(labelEventSelection, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        horizontalBoxEventSelection.Add(self.spinCtrlEventCurrent, wx.EXPAND|wx.ALL)
        horizontalBoxEventSelection.Add(labelEventSelectionSlash, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        horizontalBoxEventSelection.Add(self.spinCtrlEventCount, wx.EXPAND|wx.ALL)

        # event data
        self.verticalBoxEventData = wx.BoxSizer(wx.VERTICAL)
        labelEventData = wx.StaticText(self, label="Event Data:")
        self.verticalBoxEventData.Add(labelEventData)
        self.verticalBoxEventData.Add(horizontalBoxEventSelection)

        self.SetSizer(self.verticalBoxEventData)
        self.Fit()

    def update(self, mapData : Model_Map):
        self.mapData = mapData

        if (len(self.mapData.events.events) > 0):
            self.spinCtrlEventCurrent.SetMin(1)
            self.spinCtrlEventCurrent.SetValue(1)
        else:
            self.spinCtrlEventCurrent.SetMin(0)
            self.spinCtrlEventCurrent.SetValue(0)

        self.spinCtrlEventCurrent.SetMax(len(self.mapData.events.events))
        self.spinCtrlEventCount.SetValue(len(self.mapData.events.events))