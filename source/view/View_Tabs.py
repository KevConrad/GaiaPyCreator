import wx

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
        tabEvents = TabEvents(self.notebook)
        tabItems = TabItems(self.notebook)
        tabMaps = TabMaps(self.notebook)
        tabMisc = TabMisc(self.notebook)
        tabMusic = TabMusic(self.notebook)
        tabPalettes = TabPalettes(self.notebook)
        tabSprites = TabSprites(self.notebook)
        tabTextBox = TabTextBox(self.notebook)
        tabTilemaps = TabTilemaps(self.notebook)
        tabTilesets = TabTilesets(self.notebook)

        # Assigning names to tabs and adding them:
        tabEvents = self.notebook.AddPage(tabEvents, "Events")
        self.tabItems = self.notebook.AddPage(tabItems, "Items")
        self.notebook.AddPage(tabMaps, "Maps")
        self.notebook.AddPage(tabMisc, "Misc")
        self.notebook.AddPage(tabMusic, "Music")
        self.notebook.AddPage(tabPalettes, "Palettes")
        self.notebook.AddPage(tabSprites, "Sprites")
        self.notebook.AddPage(tabTextBox, "Textbox")
        self.notebook.AddPage(tabTilemaps, "Tilemaps")
        self.notebook.AddPage(tabTilesets, "Tilesets")

        # Organizing notebook layout using a sizer:
        sizer = wx.BoxSizer()
        sizer.Add(self.notebook, 1, wx.EXPAND)
        panel.SetSizer(sizer)