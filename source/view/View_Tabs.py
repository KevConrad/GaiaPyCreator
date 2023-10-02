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
        notebook = wx.Notebook(panel)

        # Initiation of the tab windows:
        tabEvents = TabEvents(notebook)
        tabItems = TabItems(notebook)
        tabMaps = TabMaps(notebook)
        tabMisc = TabMisc(notebook)
        tabMusic = TabMusic(notebook)
        tabPalettes = TabPalettes(notebook)
        tabSprites = TabSprites(notebook)
        tabTextBox = TabTextBox(notebook)
        tabTilemaps = TabTilemaps(notebook)
        tabTilesets = TabTilesets(notebook)

        # Assigning names to tabs and adding them:
        notebook.AddPage(tabEvents, "Events")
        notebook.AddPage(tabItems, "Items")
        notebook.AddPage(tabMaps, "Maps")
        notebook.AddPage(tabMisc, "Misc")
        notebook.AddPage(tabMusic, "Music")
        notebook.AddPage(tabPalettes, "Palettes")
        notebook.AddPage(tabSprites, "Sprites")
        notebook.AddPage(tabTextBox, "Textbox")
        notebook.AddPage(tabTilemaps, "Tilemaps")
        notebook.AddPage(tabTilesets, "Tilesets")

        # Organizing notebook layout using a sizer:
        sizer = wx.BoxSizer()
        sizer.Add(notebook, 1, wx.EXPAND)
        panel.SetSizer(sizer)