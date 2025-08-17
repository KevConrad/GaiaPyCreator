from pubsub import pub

# notification
from pubsub.utils.notification import useNotifyByWriteFile

from controller.Controller_Project import Controller_Project
from model.Model_MapDataTable import Model_MapDataTable
from model.Model_MapData import Model_MapData
from model.Model_MapDataBuffer import Model_MapDataBuffer
from model.Model_Maps import Model_Maps
from model.Model_RoomClearingRewards import Model_RoomClearingRewards
from model.Model_ScreenSettings import Model_ScreenSettings
from model.Model_Tilemaps import Model_Tilemaps
from view.View_Main import View_Main

class Controller_Maps:
    def __init__(self, project : Controller_Project, view:View_Main) -> None:
        self.project = project
        self.view = view

        self.tilemaps = Model_Tilemaps(self.project.romData.romData, self.project.projectData.projectData)

        pub.subscribe(self.load, "maps_load")
        pub.subscribe(self.update, "maps_update")
        pub.subscribe(self.updateEventImage, "maps_update_event")
        pub.subscribe(self.updateExitImage, "maps_update_exit")
        pub.subscribe(self.updateMapArrangement, "maps_update_mapArrangement")
        pub.subscribe(self.updateMapImage, "maps_update_mapImage")
        pub.subscribe(self.updateTilemapImage, "maps_update_tilemapImage")

    def load(self):
        if self.project.isProjectLoaded == True:
            self.loadMapDataTable(self.tilemaps)

            self.roomClearingRewards = Model_RoomClearingRewards(self.project.romData.romData, self.project.projectData.projectData)
            
            self.screenSettings = Model_ScreenSettings(self.project.romData.romData, self.project.projectData.projectData)
            
            self.maps = Model_Maps(self.project.romData.romData, self.project.projectData.projectData, self.mapData, self.screenSettings, self.roomClearingRewards)

            self.view.maps.load(self.maps.mapNames, self.tilemaps.tilemapNames)
            
    def loadMapDataTable(self, tilemaps: Model_Tilemaps):
        # load the map data table data from the project file
        self.mapDataTable = Model_MapDataTable()
        self.mapDataTable.load(self.project.projectData.projectData)
        self.tilemaps = tilemaps

        self.mapData = []
        address = self.mapDataTable.mapDataTableAddress
        mapDataBuffer = Model_MapDataBuffer(self.project.romData.romData, tilemaps)
        for mapIndex in range (Model_MapData.MAP_COUNT):
            mapData = Model_MapData(self.project.romData.romData, tilemaps)
            length = mapData.read(address, mapIndex, mapDataBuffer)
            self.mapData.append(mapData)

            address += length
        
    def update(self, mapIndex):
        self.mapIndex = mapIndex
        # read the map data
        self.maps.maps[self.mapIndex].read()
        # create the map image
        self.maps.maps[self.mapIndex].createImage(True, True, True, 0)
        self.maps.maps[self.mapIndex].createEventImage(0)
        self.maps.maps[self.mapIndex].createExitImage(0)

        self.tilemapIndex = self.maps.maps[self.mapIndex].mapDataTilemap[0].index
        self.tilemaps.tilemaps[self.tilemapIndex].read()
        self.tilemapImage = self.tilemaps.tilemaps[self.tilemapIndex].getImage(readOffset = 0, readAll = True,
                                                                               tileOffset = 0, tilesetReadOffset = 0)
        self.tilemapImage = self.tilemaps.tilemaps[self.tilemapIndex].getImageOverlay(0, 0, 0, 0, True)
        
        self.view.maps.update(self.maps.maps[self.mapIndex])

        # update the tilemap image in the map editor tab page
        self.view.maps.tabEditor.updateTilemapImage(self.tilemapImage)

    def updateEventImage(self, selectedEventIndex):
        self.maps.maps[self.mapIndex].createEventImage(selectedEventIndex)
        self.view.maps.updateImage(self.maps.maps[self.mapIndex])

    def updateExitImage(self, selectedExitIndex):
        self.maps.maps[self.mapIndex].createExitImage(selectedExitIndex)
        self.view.maps.updateImage(self.maps.maps[self.mapIndex])

    def updateMapArrangement(self, currentPositionX, currentPositionY, selectedTileIndex):
        self.maps.maps[self.mapIndex].updateArrangement(currentPositionX, currentPositionY, selectedTileIndex, 0, self.maps.maps[self.mapIndex].imageBytes[0])
        # update the map image in the GUI
        self.view.maps.updateImage(self.maps.maps[self.mapIndex])

    def updateMapImage(self, currentPositionX, currentPositionY, tabIndex):
        #self.maps.maps[self.mapIndex].createImageOverlay(currentPositionX, currentPositionY, tabIndex)
        # update the map image in the GUI
        self.view.maps.updateImage(self.maps.maps[self.mapIndex])

    def updateTilemapImage(self, currentPositionX, currentPositionY, selectedPositionX, selectedPositionY):
        tilemapImage = self.tilemaps.tilemaps[self.tilemapIndex].getImageOverlay(currentPositionX, currentPositionY,
                                                                                 selectedPositionX, selectedPositionY, True)
        # update the tilemap image in the map editor tab page
        self.view.maps.tabEditor.updateTilemapImage(tilemapImage)
