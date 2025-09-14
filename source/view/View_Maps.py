import PIL
import PIL.Image
import wx

from model.Model_Map import Model_Map
from model.Model_ScreenSetting import Model_ScreenSetting
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
    MAP_IMAGE_PIXEL_HEIGHT = 500
    MAP_IMAGE_PIXEL_WIDTH = 500
    MAP_ZOOM_DEFAULT = 15
    MAP_ZOOM_TIMER_INTERVAL = 50

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
        # bind function if mouse cursor over map image
        self.displayedMapImage.Bind(wx.EVT_MOTION, self.onMouseMoveOverMap)
        # bind function if mouse cursor over map image and left button pressed
        self.displayedMapImage.Bind(wx.EVT_LEFT_DOWN, self.onMouseLeftDownOverMap)

        # Add zoom buttons
        horizontalBoxZoom = wx.BoxSizer(wx.HORIZONTAL)
        labelZoom = wx.StaticText(self.tabPage, label="Zoom:")
        self.zoomInButton = wx.Button(self.tabPage, label="+")
        self.zoomInButton.Bind(wx.EVT_BUTTON, self.onZoomInButtonClick)
        self.zoomInButton.Bind(wx.EVT_LEFT_DOWN, self.onZoomInButtonDown)
        self.zoomInButton.Bind(wx.EVT_LEFT_UP, self.onZoomInButtonUp)
        self.zoomOutButton = wx.Button(self.tabPage, label="-")
        self.zoomOutButton.Bind(wx.EVT_BUTTON, self.onZoomOutButtonClick)
        self.zoomOutButton.Bind(wx.EVT_LEFT_DOWN, self.onZoomOutButtonDown)
        self.zoomOutButton.Bind(wx.EVT_LEFT_UP, self.onZoomOutButtonUp)
        self.zoom = self.MAP_ZOOM_DEFAULT
        labelMouseCursorX = wx.StaticText(self.tabPage, label="X:")
        self.TextMouseCursorX = wx.StaticText(self.tabPage, label="-")
        labelMouseCursorY = wx.StaticText(self.tabPage, label="Y:")
        self.TextMouseCursorY = wx.StaticText(self.tabPage, label="-")
        horizontalBoxZoom.Add(labelZoom)
        horizontalBoxZoom.Add(self.zoomOutButton)
        horizontalBoxZoom.Add(self.zoomInButton)
        horizontalBoxZoom.Add(labelMouseCursorX)
        horizontalBoxZoom.Add(self.TextMouseCursorX)
        horizontalBoxZoom.AddSpacer(10)
        horizontalBoxZoom.Add(labelMouseCursorY)
        horizontalBoxZoom.Add(self.TextMouseCursorY)
        horizontalBoxZoom.AddSpacer(10)

        # Add map layer selection
        horizontalBoxMapLayers = wx.BoxSizer(wx.HORIZONTAL)
        labelMapDisplay = wx.StaticText(self.tabPage, label="Display:")

        labelMapLayerBG1 = wx.StaticText(self.tabPage, label="BG1:")
        self.checkBoxMapLayerBG1 = wx.CheckBox(self.tabPage)
        self.checkBoxMapLayerBG1.Bind(wx.EVT_CHECKBOX, self.onMapLayerChange)
        self.checkBoxMapLayerBG1.SetValue(True)

        labelMapLayerBG2 = wx.StaticText(self.tabPage, label="BG2:")
        self.checkBoxMapLayerBG2 = wx.CheckBox(self.tabPage)
        self.checkBoxMapLayerBG2.Bind(wx.EVT_CHECKBOX, self.onMapLayerChange)
        self.checkBoxMapLayerBG2.SetValue(True)

        labelMapLayerSprites = wx.StaticText(self.tabPage, label="Sprites:")
        self.checkBoxMapLayerSprites = wx.CheckBox(self.tabPage)
        self.checkBoxMapLayerSprites.Bind(wx.EVT_CHECKBOX, self.onMapLayerChange)
        self.checkBoxMapLayerSprites.SetValue(True)

        horizontalBoxMapLayers.Add(labelMapDisplay)
        horizontalBoxMapLayers.Add(labelMapLayerBG1)
        horizontalBoxMapLayers.Add(self.checkBoxMapLayerBG1)
        horizontalBoxMapLayers.Add(labelMapLayerBG2)
        horizontalBoxMapLayers.Add(self.checkBoxMapLayerBG2)
        horizontalBoxMapLayers.Add(labelMapLayerSprites)
        horizontalBoxMapLayers.Add(self.checkBoxMapLayerSprites)

        horizontalBoxMap = wx.BoxSizer(wx.HORIZONTAL)
        horizontalBoxMap.Add(self.scrolledWindowMap)
        self.mapDataTabs = self.initMapDataTabs(self.tabPage)
        horizontalBoxMap.Add(self.mapDataTabs)

        verticalBox = wx.BoxSizer(wx.VERTICAL)
        verticalBox.Add(horizontalBoxMap, 0, wx.EXPAND)
        verticalBox.Add(horizontalBoxZoom)
        verticalBox.Add(horizontalBoxMapLayers)

        horizontalBox = wx.BoxSizer(wx.HORIZONTAL)
        horizontalBox.Add(self.listBoxMaps, 0, wx.EXPAND)
        horizontalBox.Add(verticalBox, 1, wx.EXPAND)
        
        self.tabPage.SetSizer(horizontalBox)
        self.tabPage.Fit()

        self.frame.Show(True)

        # Timer for continuous zoom
        self.zoomInTimer = wx.Timer(self.tabPage)
        self.tabPage.Bind(wx.EVT_TIMER, self.onZoomInTimer, self.zoomInTimer)
        self.zoomOutTimer = wx.Timer(self.tabPage)
        self.tabPage.Bind(wx.EVT_TIMER, self.onZoomOutTimer, self.zoomOutTimer)

    def initMapDataTabs(self, parent):
        mapDataTabs = wx.Notebook(parent, size=(400, 500))

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

    def displayMapImage(self):
        magnificationX = self.mapData.sizeX * self.zoom
        magnificationY = self.mapData.sizeY * self.zoom
        
        image = PIL.Image.new('RGB', (magnificationX, magnificationY), (0, 0, 0))
            
        if self.mapData.screenSettings is not None:
            mapLayerOrder = self.mapData.screenSettings.mapLayerOrderBits
            print("Map layer order bits: " + str(mapLayerOrder))
            if (((mapLayerOrder & Model_ScreenSetting.MAP_LAYER_ORDER_HAS_NORMAL_MAP_LAYERS) == 0x80) and
                (len(self.mapData.mapDataArrangement) > 1)): # TODO: Query of arrangementCount > 1 should not be necessary!
                if self.checkBoxMapLayerBG1.IsChecked() == True:
                    bg1Image = self.mapData.imageLayers[1].resize((magnificationX, magnificationY), PIL.Image.NEAREST)
                    image.paste(bg1Image, (0, 0), bg1Image)
                if self.checkBoxMapLayerBG2.IsChecked() == True:
                    bg2Image = self.mapData.imageLayers[0].resize((magnificationX, magnificationY), PIL.Image.NEAREST)
                    image.paste(bg2Image, (0, 0), bg2Image)
            else:
                if self.checkBoxMapLayerBG1.IsChecked() == True:
                    bg1Image = self.mapData.imageLayers[0].resize((magnificationX, magnificationY), PIL.Image.NEAREST)
                    image.paste(bg1Image, (0, 0), bg1Image)
                if self.checkBoxMapLayerBG2.IsChecked() == True:
                    bg2Image = self.mapData.imageLayers[1].resize((magnificationX, magnificationY), PIL.Image.NEAREST)
                    image.paste(bg2Image, (0, 0), bg2Image)
        else:
            if self.checkBoxMapLayerBG1.IsChecked() == True:
                bg1Image = self.mapData.imageLayers[0].resize((magnificationX, magnificationY), PIL.Image.NEAREST)
                image.paste(bg1Image, (0, 0), bg1Image)
            if self.checkBoxMapLayerBG2.IsChecked() == True:
                bg2Image = self.mapData.imageLayers[1].resize((magnificationX, magnificationY), PIL.Image.NEAREST)
                image.paste(bg2Image, (0, 0), bg2Image)

        # display sprite layer
        if self.checkBoxMapLayerSprites.IsChecked() == True:
                spriteImage = self.mapData.imageLayers[2].resize((magnificationX, magnificationY), PIL.Image.NEAREST)
                image.paste(spriteImage, (0, 0), spriteImage)

        index = self.mapDataTabs.GetSelection()
        if self.mapDataTabs.GetPage(index) is self.tabEvents:
            eventImage = self.mapData.eventImage.resize((magnificationX, magnificationY), PIL.Image.NEAREST)
            image.paste(eventImage, (0, 0), eventImage)
        elif self.mapDataTabs.GetPage(index) is self.tabExits:
            exitImage = self.mapData.exitImage.resize((magnificationX, magnificationY), PIL.Image.NEAREST)
            image.paste(exitImage, (0, 0), exitImage)

        wx_image = wx.Image(image.size[0], image.size[1])
        wx_image.SetData(image.convert("RGB").tobytes())
        bitmap = wx.Bitmap(wx_image)
        self.displayedMapImage.SetBitmap(bitmap)
        
        # Ensure the map window has scrollbars
        self.scrolledWindowMap.SetVirtualSize((image.size[0], image.size[1]))
        self.scrolledWindowMap.SetScrollRate(20, 20)

    def handleTabChanged(self, event):
        index = self.mapDataTabs.GetSelection()
        pub.sendMessage("maps_update_mapImage", currentPositionX=0, currentPositionY=0, tabIndex=index)

    def load(self, mapNames, tilemapNames):
        self.listBoxMaps.Set(mapNames)
        self.tabEditor.load(tilemapNames)
        self.tabExits.load(mapNames)

    def onMapLayerChange(self, event):
        # update map image when map layer checkbox is changed
        self.displayMapImage()

    def onMouseMoveOverMap(self, event):        
        currentPositionX, currentPositionY = event.GetPosition()
        # check if mouse button is pressed
        if event.LeftIsDown() == True:
            index = self.mapDataTabs.GetSelection()
            # keep updating map arrangement with the selected tile if mouse button is kept pressed
            if self.mapDataTabs.GetPage(index) is self.tabEditor:
                # Convert to map coordinates
                currentPositionX = int(currentPositionX / self.zoom)
                currentPositionY = int(currentPositionY / self.zoom)
                pub.sendMessage("maps_update_mapArrangement", currentPositionX=currentPositionX, currentPositionY=currentPositionY, selectedTileIndex=self.tabEditor.selectedTileIndex)
        
        # Convert to map coordinates
        currentPositionX = int(currentPositionX / self.zoom)
        currentPositionY = int(currentPositionY / self.zoom)
        self.TextMouseCursorX.SetLabel(str(currentPositionX))
        self.TextMouseCursorY.SetLabel(str(currentPositionY))

        index = self.mapDataTabs.GetSelection()
        if self.mapDataTabs.GetPage(index) is self.tabEvents:
            self.selectedEventIndex = -1
            for eventIndex in range(len(self.mapData.events.events)):
                event = self.mapData.events.events[eventIndex]
                # Check if the mouse is over the event
                if event.positionX == currentPositionX and event.positionY == currentPositionY:
                    self.selectedEventIndex = eventIndex
                    break
            if self.selectedEventIndex >= 0:
                self.scrolledWindowMap.SetCursor(wx.Cursor(wx.CURSOR_HAND))
            else:
                self.scrolledWindowMap.SetCursor(wx.Cursor(wx.CURSOR_ARROW))
        elif self.mapDataTabs.GetPage(index) is self.tabExits:
            self.selectedExitIndex = -1
            for exitIndex in range(len(self.mapData.exits.exits)):
                exit = self.mapData.exits.exits[exitIndex]
                # Check if the mouse is over the exit area
                if (currentPositionX >= exit.positionX and currentPositionX < (exit.positionX + exit.width)) and \
                   (currentPositionY >= exit.positionY and currentPositionY < (exit.positionY + exit.height)):
                    self.selectedExitIndex = exitIndex
                    break
            if self.selectedExitIndex >= 0:
                self.scrolledWindowMap.SetCursor(wx.Cursor(wx.CURSOR_HAND))
            else:
                self.scrolledWindowMap.SetCursor(wx.Cursor(wx.CURSOR_ARROW))
    
        pub.sendMessage("maps_update_mapImage", currentPositionX=currentPositionX, currentPositionY=currentPositionY, tabIndex=index)

    def onMouseLeftDownOverMap(self, event):
        index = self.mapDataTabs.GetSelection()
        if self.mapDataTabs.GetPage(index) is self.tabEditor:
            currentPositionX, currentPositionY = event.GetPosition()
            # Convert to map coordinates
            currentPositionX = int(currentPositionX / self.zoom)
            currentPositionY = int(currentPositionY / self.zoom)
            pub.sendMessage("maps_update_mapArrangement", currentPositionX=currentPositionX, currentPositionY=currentPositionY, selectedTileIndex=self.tabEditor.selectedTileIndex)
        elif self.mapDataTabs.GetPage(index) is self.tabEvents:
            if self.selectedEventIndex >= 0:
                self.tabEvents.spinCtrlEventCurrent.SetValue(self.selectedEventIndex + 1)
                self.tabEvents.onEventSelectionChanged(None)
        elif self.mapDataTabs.GetPage(index) is self.tabExits:
            if self.selectedExitIndex >= 0:
                self.tabExits.spinCtrlExitCurrent.SetValue(self.selectedExitIndex + 1)
                self.tabExits.onExitSelectionChanged(None)

    def onListBox(self, event):
        selectedIndex = self.listBoxMaps.GetSelection()
        pub.sendMessage("maps_update", mapIndex=selectedIndex)

    def onZoomInButtonClick(self, event):
        self.zoom = self.zoom + 1
        self.displayMapImage()

    def onZoomOutButtonClick(self, event):
        self.zoom = self.zoom - 1
        self.displayMapImage()

    def onZoomInButtonDown(self, event):
        self.zoomInTimer.Start(self.MAP_ZOOM_TIMER_INTERVAL)  # Adjust the interval as needed

    def onZoomInButtonUp(self, event):
        self.zoomInTimer.Stop()

    def onZoomInTimer(self, event):
        self.onZoomInButtonClick(event)

    def onZoomOutButtonDown(self, event):
        self.zoomOutTimer.Start(self.MAP_ZOOM_TIMER_INTERVAL)  # Adjust the interval as needed

    def onZoomOutButtonUp(self, event):
        self.zoomOutTimer.Stop()

    def onZoomOutTimer(self, event):
        self.onZoomOutButtonClick(event)

    def update(self, mapData: Model_Map):
        self.mapData = mapData
        # update map image
        self.displayMapImage()
        
        # update map properties
        self.tabEditor.update(mapData)
        self.tabEvents.update(mapData)
        self.tabExits.update(mapData)
        self.tabProperties.update(mapData)

    def updateImage(self, mapData: Model_Map):
        self.mapData = mapData

        # update map image
        self.displayMapImage()
