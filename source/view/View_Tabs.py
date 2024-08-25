import wx

from pubsub import pub

class TabEvents(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        text = wx.StaticText(self, -1, "Edit event data.", (20,20))

class TabItems(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        text = wx.StaticText(self, -1, "Edit item data.", (20,20))

class TabMaps(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        text = wx.StaticText(self, -1, "Edit map data.", (20,20))

class TabMisc(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        text = wx.StaticText(self, -1, "Edit miscallaneous data.", (20,20))

class TabMusic(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        text = wx.StaticText(self, -1, "Edit music data.", (20,20))

class TabPalettes(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        text = wx.StaticText(self, -1, "Edit palette data.", (20,20))

class TabSprites(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        text = wx.StaticText(self, -1, "Edit sprite data.", (20,20))

class TabTextBox(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        text = wx.StaticText(self, -1, "Edit textbox data.", (20,20))

class TabTilemaps(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        text = wx.StaticText(self, -1, "Edit tilemap data.", (20,20))

class TabTilesets(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        text = wx.StaticText(self, -1, "Edit tileset data.", (20,20))
        
class View_Tabs:
    def __init__(self, frame : wx.Frame):
        
        # Panel creation and tab holder setup:
        panel = wx.Panel(frame)
        self.notebook = wx.Notebook(panel)

        # Initiation of the tab windows:
        self.tabEvents = TabEvents(self.notebook)
        self.tabItems = TabItems(self.notebook)
        self.tabMaps = TabMaps(self.notebook)
        self.tabMisc = TabMisc(self.notebook)
        self.tabMusic = TabMusic(self.notebook)
        self.tabPalettes = TabPalettes(self.notebook)
        self.tabSprites = TabSprites(self.notebook)
        self.tabTextBox = TabTextBox(self.notebook)
        self.tabTilemaps = TabTilemaps(self.notebook)
        self.tabTilesets = TabTilesets(self.notebook)

        # Assigning names to tabs and adding them:
        self.notebook.AddPage(self.tabEvents, "Events")
        self.notebook.AddPage(self.tabItems, "Items")
        self.notebook.AddPage(self.tabMaps, "Maps")
        self.notebook.AddPage(self.tabMisc, "Misc")
        self.notebook.AddPage(self.tabMusic, "Music")
        self.notebook.AddPage(self.tabPalettes, "Palettes")
        self.notebook.AddPage(self.tabSprites, "Sprites")
        self.notebook.AddPage(self.tabTextBox, "Textbox")
        self.notebook.AddPage(self.tabTilemaps, "Tilemaps")
        self.notebook.AddPage(self.tabTilesets, "Tilesets")

        self.notebook.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.handleTabChanged)

        # Organizing notebook layout using a sizer:
        sizer = wx.BoxSizer()
        sizer.Add(self.notebook, 1, wx.EXPAND)
        panel.SetSizer(sizer)

    def handleTabChanged(self, event):
        index = self.notebook.GetSelection()

        if self.notebook.GetPage(index) is self.tabItems:
            pub.sendMessage("items_load")
        if self.notebook.GetPage(index) is self.tabMaps:
            pub.sendMessage("maps_load")
        if self.notebook.GetPage(index) is self.tabTilesets:
            pub.sendMessage("tilesets_load")