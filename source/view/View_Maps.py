import PIL
import PIL.Image
import wx
import wx.lib.scrolledpanel

from model.Model_Map import Model_Map
from model.Model_Tile import Model_Tile
from model.Model_Tilemap import Model_Tilemap
from view.View_Common import View_Common
from view.View_Tabs import TabMaps

from pubsub import pub
from PIL import Image

class View_Maps:

    class TabEditor(wx.Panel):
        EDITOR_TAB_INDEX = 0

        def __init__(self, parent):
            wx.Panel.__init__(self, parent)
            text = wx.StaticText(self, -1, "Edit map.", (20,20))

    class TabEvents(wx.Panel):
        EVENTS_TAB_INDEX = 1

        def __init__(self, parent):
            wx.Panel.__init__(self, parent)
            text = wx.StaticText(self, -1, "Edit map event data.", (20,20))

    class TabExits(wx.Panel):
        EXITS_TAB_INDEX = 2

        def __init__(self, parent):
            wx.Panel.__init__(self, parent)
            text = wx.StaticText(self, -1, "Edit map exit data.", (20,20))

    class TabProperties(wx.Panel):
        PROPERTIES_TAB_INDEX = 3

        def __init__(self, parent, tabPage):
            wx.Panel.__init__(self, parent)
            text = wx.StaticText(self, -1, "Edit map properties.", (20,20))

            # map size spinCtrls
            #horizontalBoxMapSize = wx.BoxSizer(wx.HORIZONTAL)
            #labelMapSizeX = wx.StaticText(tabPage, label="Size X: ")
            #self.spinCtrlMapSizeX = wx.SpinCtrl(tabPage, style=wx.SP_ARROW_KEYS)
            #self.spinCtrlMapSizeX.SetMin(0)
            #self.spinCtrlMapSizeX.SetMax(1024)
            #self.spinCtrlMapSizeY = wx.SpinCtrl(tabPage, style=wx.SP_ARROW_KEYS)
            #self.spinCtrlMapSizeY.SetMin(0)
            #self.spinCtrlMapSizeY.SetMax(1024)
            #horizontalBoxMapSize.Add(labelMapSizeX, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
            #horizontalBoxMapSize.Add(self.spinCtrlMapSizeX, wx.EXPAND|wx.ALL)
            #horizontalBoxMapSize.Add(self.spinCtrlMapSizeY, wx.EXPAND|wx.ALL)

            # map data
            #self.verticalBoxMapData = wx.BoxSizer(wx.VERTICAL)
            #labelMapData = wx.StaticText(tabPage, label="Map Data:")
            #self.verticalBoxMapData.Add(labelMapData)
            #self.verticalBoxMapData.Add(horizontalBoxMapSize)

    class TabSprites(wx.Panel):
        SPRITES_TAB_INDEX = 2

        def __init__(self, parent):
            wx.Panel.__init__(self, parent)
            text = wx.StaticText(self, -1, "Edit map sprite data.", (20,20))

    class TabTreasures(wx.Panel):
        SPRITES_TAB_INDEX = 2

        def __init__(self, parent):
            wx.Panel.__init__(self, parent)
            text = wx.StaticText(self, -1, "Edit map treasure data.", (20,20))

    MAP_IMAGE_PIXEL_HEIGHT = 400
    MAP_IMAGE_PIXEL_WIDTH = 400

    def __init__(self, frame : wx.Frame, notebook : wx.Notebook):
        self.frame = frame
        self.tabPage = notebook.GetPage(TabMaps.MAPS_TAB_INDEX)

        # maps list box
        self.listBoxMaps = wx.ListBox(self.tabPage , size = (View_Common.LISTBOX_WIDTH, View_Common.LISTBOX_HEIGHT),
                                      style = wx.LB_SINGLE|wx.LB_HSCROLL)
        self.frame.Bind(wx.EVT_LISTBOX, self.onListBox, self.listBoxMaps)

        self.panelMapImage = wx.ScrolledWindow(self.tabPage,-1,
                                               size=(self.MAP_IMAGE_PIXEL_WIDTH, self.MAP_IMAGE_PIXEL_HEIGHT),
                                               pos=(0,0), style=wx.SIMPLE_BORDER)
       
        # map image
        verticalBoxMapImage = wx.BoxSizer(wx.VERTICAL)
        self.mapImage = wx.StaticBitmap(self.panelMapImage, wx.ID_ANY, wx.NullBitmap,
                                        size=(self.MAP_IMAGE_PIXEL_WIDTH, self.MAP_IMAGE_PIXEL_HEIGHT))
        # TODO self.mapImage.Bind(wx.EVT_LEFT_DOWN, self.onTilemapImageClick)
        verticalBoxMapImage.Add(self.mapImage)
        
        #self.panelMapImage.SetupScrolling(scroll_x=True, scroll_y=True, scrollIntoView=True)
        #self.panelMapImage.SetScrollbar(wx.VERTICAL, 0, 16, 50)
        self.panelMapImage.SetBackgroundColour('#000000')
        #self.panelMapImage.SetSizer(verticalBoxMapImage)

        self.mapDataTabs = self.initMapDataTabs(self.tabPage)

        horizontalBox = wx.BoxSizer(wx.HORIZONTAL)
        horizontalBox.Add(self.listBoxMaps, 0, wx.EXPAND)
        horizontalBox.Add(self.panelMapImage)
        horizontalBox.Add(self.mapDataTabs)
        
        self.tabPage.SetSizer(horizontalBox)
        self.tabPage.Fit()

        self.frame.Show(True)

    def initMapDataTabs(self, parent):
        mapDataTabs = wx.Notebook(parent, size=(400, 400))

        # Initiation of the tab windows:
        self.tabEditor = self.TabEditor(mapDataTabs)
        self.tabEvents = self.TabEvents(mapDataTabs)
        self.tabExits = self.TabExits(mapDataTabs)
        self.tabProperties = self.TabProperties(mapDataTabs, parent)
        self.tabSprites = self.TabSprites(mapDataTabs)
        self.tabTreasures = self.TabTreasures(mapDataTabs)

        # Assigning names to tabs and adding them:
        mapDataTabs.AddPage(self.tabEditor, "Edit")
        mapDataTabs.AddPage(self.tabEvents, "Events")
        mapDataTabs.AddPage(self.tabExits, "Exits")
        mapDataTabs.AddPage(self.tabProperties, "Properties")
        mapDataTabs.AddPage(self.tabSprites, "Sprites")
        mapDataTabs.AddPage(self.tabTreasures, "Treasures")

        mapDataTabs.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.handleTabChanged)

        return mapDataTabs

    def handleTabChanged(self, event):
        pass

    def load(self, mapNames):
        self.listBoxMaps.Set(mapNames)

    def onListBox(self, event):
        selectedIndex = self.listBoxMaps.GetSelection()
        pub.sendMessage("maps_update", mapIndex=selectedIndex)

    def update(self, mapImage : PIL.Image, mapData : Model_Map):
        # update map image
        sizedImage = mapImage.resize((mapData.sizeX * 20, mapData.sizeY * 20), PIL.Image.NEAREST)
        wx_image = wx.EmptyImage(sizedImage.size[0], sizedImage.size[1])
        wx_image.SetData(sizedImage.convert("RGB").tobytes())
        bitmap = wx.BitmapFromImage(wx_image)
        self.mapImage.SetBitmap(bitmap)
        
        xUnits = int(sizedImage.size[0] / self.MAP_IMAGE_PIXEL_WIDTH)
        yUnits = int(sizedImage.size[1] / self.MAP_IMAGE_PIXEL_HEIGHT)
        print(xUnits)
        print(yUnits)
        
        #self.panelMapImage.SetScrollbars(self.MAP_IMAGE_PIXEL_WIDTH, self.MAP_IMAGE_PIXEL_HEIGHT, xUnits, yUnits)
        
        verticalBoxMapImage = wx.BoxSizer(wx.VERTICAL)
        verticalBoxMapImage.Detach(self.mapImage)
        verticalBoxMapImage.Add(self.mapImage)
        self.panelMapImage.SetSizer(verticalBoxMapImage)

        self.panelMapImage.SetScrollbars(1, 1, 1, 1)
        self.panelMapImage.SetScrollbar(wx.HORIZONTAL, 0, self.MAP_IMAGE_PIXEL_WIDTH, xUnits)
        self.panelMapImage.SetScrollbar(wx.VERTICAL, 0, self.MAP_IMAGE_PIXEL_HEIGHT, yUnits)

        # update map data
        self.spinCtrlMapSizeX.SetValue(mapData.sizeX)
        self.spinCtrlMapSizeY.SetValue(mapData.sizeY)

