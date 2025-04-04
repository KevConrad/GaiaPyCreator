from pubsub import pub

# notification
from pubsub.utils.notification import useNotifyByWriteFile

from controller.Controller_Project import Controller_Project
from model.Model_MapDataTable import Model_MapDataTable
from model.Model_MapData import Model_MapData
from model.Model_MapDataBuffer import Model_MapDataBuffer
from model.Model_Maps import Model_Maps
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

    def load(self):
        if self.project.isProjectLoaded == True:
            self.loadMapDataTable(self.tilemaps)
            
            self.screenSettings = Model_ScreenSettings(self.project.romData.romData, self.project.projectData.projectData)
            
            self.maps = Model_Maps(self.project.romData.romData, self.project.projectData.projectData, self.mapData, self.screenSettings)

            self.view.maps.load(self.maps.mapNames, self.tilemaps.tilemapNames)
            
    def loadMapDataTable(self, tilemaps:Model_Tilemaps):
        # load the map data table data from the project file
        self.mapDataTable = Model_MapDataTable()
        self.mapDataTable.load(self.project.projectData.projectData)

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
        self.maps.maps[self.mapIndex].getImage(True, True, True, 0)
        self.maps.maps[self.mapIndex].getEventImage(0)
        self.maps.maps[self.mapIndex].getExitImage(0)
        self.view.maps.update(self.maps.maps[self.mapIndex])

    def updateEventImage(self, selectedEventIndex):
        self.maps.maps[self.mapIndex].getEventImage(selectedEventIndex)
        self.view.maps.updateImage(self.maps.maps[self.mapIndex])

    def updateExitImage(self, selectedExitIndex):
        self.maps.maps[self.mapIndex].getExitImage(selectedExitIndex)
        self.view.maps.updateImage(self.maps.maps[self.mapIndex])
