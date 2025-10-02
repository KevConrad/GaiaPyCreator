import wx

from model.Model_EnemyState import Model_EnemyState

from view.View_MiscTabEnemyStates import View_MiscTabEnemyStates
from view.View_Tabs import TabMisc

from pubsub import pub

class View_Misc:
    SPACER_SIZE = 10

    def __init__(self, frame : wx.Frame, notebook : wx.Notebook):
        self.frame = frame
        self.tabPage = notebook.GetPage(TabMisc.MISC_TAB_INDEX)

        horizontalMiscTabs = wx.BoxSizer(wx.HORIZONTAL)
        self.miscTabs = self.initSubTabs(self.tabPage)
        horizontalMiscTabs.Add(self.miscTabs)

        verticalBox = wx.BoxSizer(wx.VERTICAL)
        verticalBox.Add(horizontalMiscTabs, 0, wx.EXPAND)

        horizontalBox = wx.BoxSizer(wx.HORIZONTAL)
        horizontalBox.Add(verticalBox, 1, wx.EXPAND)
        
        self.tabPage.SetSizer(horizontalBox)
        self.tabPage.Fit()

        self.frame.Show(True)

    def initSubTabs(self, parent):
        miscTabs = wx.Notebook(parent, size=(1000, 500))

        # Initiation of the tab windows:
        self.tabEnemyStates = View_MiscTabEnemyStates(miscTabs)

        # Assigning names to tabs and adding them:
        miscTabs.AddPage(self.tabEnemyStates, "Enemy States")

        miscTabs.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.handleTabChanged)

        return miscTabs


    def handleTabChanged(self, event):
        index = self.miscTabs.GetSelection()

    def load(self, enemyStateNames):
        self.tabEnemyStates.load(enemyStateNames)

    def update(self, enemyStateData: Model_EnemyState):        
        self.tabEnemyStates.update(enemyStateData)
