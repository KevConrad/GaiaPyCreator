import PIL
import PIL.Image
import wx

from model.Model_Map import Model_Map
from model.Model_Tile import Model_Tile
from model.Model_Tilemap import Model_Tilemap
from view.View_Common import View_Common
from view.View_MapTabEditor import View_MapTabEditor
from view.View_MapTabEvents import View_MapTabEvents
from view.View_MapTabExits import View_MapTabExits
from view.View_MapTabProperties import View_MapTabProperties
from view.View_MapTabSprites import View_MapTabSprites
from view.View_MapTabTreasures import View_MapTabTreasures
from view.View_Tabs import TabMaps

from pubsub import pub
from PIL import Image

class View_Maps:
    MAP_IMAGE_PIXEL_HEIGHT = 400
    MAP_IMAGE_PIXEL_WIDTH = 400
    MAP_MAGNIFICATION_DEFAULT = 15

    def __init__(self, frame : wx.Frame, notebook : wx.Notebook):
        self.frame = frame
        self.tabPage = notebook.GetPage(TabMaps.MAPS_TAB_INDEX)

        # maps list box
        self.listBoxMaps = wx.ListBox(self.tabPage , size = (View_Common.LISTBOX_WIDTH, View_Common.LISTBOX_HEIGHT),
                                      style = wx.LB_SINGLE|wx.LB_HSCROLL)
        self.frame.Bind(wx.EVT_LISTBOX, self.onListBox, self.listBoxMaps)

        self.scrolledWindowMap = wx.ScrolledWindow(self.tabPage,-1,
                                                   size=(self.MAP_IMAGE_PIXEL_WIDTH, self.MAP_IMAGE_PIXEL_HEIGHT),
                                                   pos=(0,0), style=wx.SHOW_SB_ALWAYS)
        self.scrolledWindowMap.SetBackgroundColour('#000000')
       
        # create map image
        self.displayedMapImage = wx.StaticBitmap(self.scrolledWindowMap, wx.ID_ANY, wx.NullBitmap,
                                                 size=(self.MAP_IMAGE_PIXEL_WIDTH, self.MAP_IMAGE_PIXEL_HEIGHT))
        # TODO self.mapImage.Bind(wx.EVT_LEFT_DOWN, self.onTilemapImageClick)

        # Add zoom buttons
        horizontalBoxZoom = wx.BoxSizer(wx.HORIZONTAL)
        labelZoom = wx.StaticText(self.tabPage, label="Zoom:")
        self.zoomInButton = wx.Button(self.tabPage, label="+")
        self.zoomInButton.Bind(wx.EVT_BUTTON, self.onZoomInButtonClick)
        self.zoomOutButton = wx.Button(self.tabPage, label="-")
        self.zoomOutButton.Bind(wx.EVT_BUTTON, self.onZoomOutButtonClick)
        self.magnification = self.MAP_MAGNIFICATION_DEFAULT
        horizontalBoxZoom.Add(labelZoom)
        horizontalBoxZoom.Add(self.zoomInButton)
        horizontalBoxZoom.Add(self.zoomOutButton)

        horizontalBoxMap = wx.BoxSizer(wx.HORIZONTAL)
        horizontalBoxMap.Add(self.scrolledWindowMap)
        self.mapDataTabs = self.initMapDataTabs(self.tabPage)
        horizontalBoxMap.Add(self.mapDataTabs)

        verticalBox = wx.BoxSizer(wx.VERTICAL)
        verticalBox.Add(horizontalBoxMap, 0, wx.EXPAND)
        verticalBox.Add(horizontalBoxZoom)

        horizontalBox = wx.BoxSizer(wx.HORIZONTAL)
        horizontalBox.Add(self.listBoxMaps, 0, wx.EXPAND)
        horizontalBox.Add(verticalBox, 1, wx.EXPAND)
        
        self.tabPage.SetSizer(horizontalBox)
        self.tabPage.Fit()

        self.frame.Show(True)

    def initMapDataTabs(self, parent):
        mapDataTabs = wx.Notebook(parent, size=(400, 400))

        # Initiation of the tab windows:
        self.tabEditor = View_MapTabEditor(mapDataTabs)
        self.tabEvents = View_MapTabEvents(mapDataTabs)
        self.tabExits = View_MapTabExits(mapDataTabs)
        self.tabProperties = View_MapTabProperties(mapDataTabs)
        self.tabSprites = View_MapTabSprites(mapDataTabs)
        self.tabTreasures = View_MapTabTreasures(mapDataTabs)

        # Assigning names to tabs and adding them:
        mapDataTabs.AddPage(self.tabEditor, "Edit")
        mapDataTabs.AddPage(self.tabEvents, "Events")
        mapDataTabs.AddPage(self.tabExits, "Exits")
        mapDataTabs.AddPage(self.tabProperties, "Properties")
        mapDataTabs.AddPage(self.tabSprites, "Sprites")
        mapDataTabs.AddPage(self.tabTreasures, "Treasures")

        mapDataTabs.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.handleTabChanged)

        return mapDataTabs

    def displayMapImage(self, magnification):
        magnificationX = self.mapSizeX * magnification
        magnificationY = self.mapSizeY * magnification
        sizedImage = self.receivedMapImage.resize((magnificationX, magnificationY), PIL.Image.NEAREST)
        wx_image = wx.Image(sizedImage.size[0], sizedImage.size[1])
        wx_image.SetData(sizedImage.convert("RGB").tobytes())
        bitmap = wx.Bitmap(wx_image)
        self.displayedMapImage.SetBitmap(bitmap)
        
        # Ensure the map window has scrollbars
        self.scrolledWindowMap.SetVirtualSize((sizedImage.size[0], sizedImage.size[1]))
        self.scrolledWindowMap.SetScrollRate(20, 20)

    def handleTabChanged(self, event):
        pass

    def load(self, mapNames):
        self.listBoxMaps.Set(mapNames)

    def onListBox(self, event):
        selectedIndex = self.listBoxMaps.GetSelection()
        pub.sendMessage("maps_update", mapIndex=selectedIndex)

    def onZoomInButtonClick(self, event):
        self.magnification = self.magnification + 1
        self.displayMapImage(self.magnification)

    def onZoomOutButtonClick(self, event):
        self.magnification = self.magnification - 1
        self.displayMapImage(self.magnification)

    def update(self, mapImage: PIL.Image, mapData: Model_Map):
        # update map image
        self.receivedMapImage = mapImage
        self.mapSizeX = mapData.sizeX
        self.mapSizeY = mapData.sizeY
        self.displayMapImage(self.magnification)
        
        # update map properties
        self.tabEvents.update(mapData)
        self.tabExits.update(mapData)
        self.tabProperties.update(mapData)
