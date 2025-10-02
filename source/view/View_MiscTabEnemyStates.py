
import wx

from model.Model_EnemyState import Model_EnemyState

from view.View_Common import View_Common

from PIL import Image
from pubsub import pub

class View_MiscTabEnemyStates(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        
        # enemy states list box
        self.listBoxEnemyStates = wx.ListBox(self , size = (View_Common.LISTBOX_WIDTH, View_Common.LISTBOX_HEIGHT),
                                             style = wx.LB_SINGLE|wx.LB_HSCROLL)
        self.listBoxEnemyStates.Bind(wx.EVT_LISTBOX, self.onListBox, self.listBoxEnemyStates)

        # create spin ctrl for health points
        self.spinCtrlHealthPoints = wx.SpinCtrl(self, style=wx.SP_ARROW_KEYS)
        self.spinCtrlHealthPoints.SetMin(0)
        self.spinCtrlHealthPoints.SetMax(255)
        labelHealthPoints = wx.StaticText(self, label="Health Points:")
        horizontalBoxHealthPoints = wx.BoxSizer(wx.HORIZONTAL)
        horizontalBoxHealthPoints.Add(labelHealthPoints, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        horizontalBoxHealthPoints.Add(self.spinCtrlHealthPoints, wx.EXPAND|wx.ALL)

        # create spin ctrl for strength
        self.spinCtrlStrength = wx.SpinCtrl(self, style=wx.SP_ARROW_KEYS)
        self.spinCtrlStrength.SetMin(0)
        self.spinCtrlStrength.SetMax(255)
        labelStrength = wx.StaticText(self, label="Strength:")
        horizontalBoxStrength = wx.BoxSizer(wx.HORIZONTAL)
        horizontalBoxStrength.Add(labelStrength, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        horizontalBoxStrength.Add(self.spinCtrlStrength, wx.EXPAND|wx.ALL)

        # create spin ctrl for defense
        self.spinCtrlDefense = wx.SpinCtrl(self, style=wx.SP_ARROW_KEYS)
        self.spinCtrlDefense.SetMin(0)
        self.spinCtrlDefense.SetMax(255)
        labelDefense = wx.StaticText(self, label="Defense:")
        horizontalBoxDefense = wx.BoxSizer(wx.HORIZONTAL)
        horizontalBoxDefense.Add(labelDefense, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        horizontalBoxDefense.Add(self.spinCtrlDefense, wx.EXPAND|wx.ALL)

        # create spin ctrl for dark power
        self.spinCtrlDarkPower = wx.SpinCtrl(self, style=wx.SP_ARROW_KEYS)
        self.spinCtrlDarkPower.SetMin(0)
        self.spinCtrlDarkPower.SetMax(255)
        labelDarkPower = wx.StaticText(self, label="Dark Power:")
        horizontalBoxDarkPower = wx.BoxSizer(wx.HORIZONTAL)
        horizontalBoxDarkPower.Add(labelDarkPower, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
        horizontalBoxDarkPower.Add(self.spinCtrlDarkPower, wx.EXPAND|wx.ALL)

        # create vertical box containing enemy states data
        verticalBoxEnemyStatesDataControls = wx.BoxSizer(wx.VERTICAL)
        verticalBoxEnemyStatesDataControls.Add(horizontalBoxHealthPoints, 0, wx.EXPAND)
        verticalBoxEnemyStatesDataControls.AddSpacer(View_Common.SPACER_SIZE)
        verticalBoxEnemyStatesDataControls.Add(horizontalBoxStrength, 0, wx.EXPAND)
        verticalBoxEnemyStatesDataControls.AddSpacer(View_Common.SPACER_SIZE)
        verticalBoxEnemyStatesDataControls.Add(horizontalBoxDefense, 0, wx.EXPAND)
        verticalBoxEnemyStatesDataControls.AddSpacer(View_Common.SPACER_SIZE)
        verticalBoxEnemyStatesDataControls.Add(horizontalBoxDarkPower, 0, wx.EXPAND)
        verticalBoxEnemyStatesDataControls.AddSpacer(View_Common.SPACER_SIZE)

        # enemy states data
        self.horizontalBoxEnemyStatesData = wx.BoxSizer(wx.HORIZONTAL)
        self.horizontalBoxEnemyStatesData.Add(self.listBoxEnemyStates)
        self.horizontalBoxEnemyStatesData.AddSpacer(View_Common.SPACER_SIZE)
        self.horizontalBoxEnemyStatesData.Add(verticalBoxEnemyStatesDataControls)
        self.horizontalBoxEnemyStatesData.AddStretchSpacer(1)
        self.SetSizer(self.horizontalBoxEnemyStatesData)
        self.Fit()

    def load(self, enemyStateNames : list):
        self.listBoxEnemyStates.Set(enemyStateNames)

    def onListBox(self, event):
        selectedIndex = self.listBoxEnemyStates.GetSelection()
        pub.sendMessage("enemyState_update", enemyStateIndex=selectedIndex)
        
    def update(self, enemyData : Model_EnemyState):
        self.enemyData = enemyData
        self.spinCtrlHealthPoints.SetValue(self.enemyData.healthPoints)
        self.spinCtrlStrength.SetValue(self.enemyData.strength)
        self.spinCtrlDefense.SetValue(self.enemyData.defense)
        self.spinCtrlDarkPower.SetValue(self.enemyData.darkPower)
