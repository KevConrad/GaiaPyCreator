from pubsub import pub

# notification
from pubsub.utils.notification import useNotifyByWriteFile

from controller.Controller_Project import Controller_Project
from model.Model_MapDataTable import Model_MapDataTable
from model.Model_MapData import Model_MapData
from model.Model_Maps import Model_Maps
from view.View_Main import View_Main

class Controller_Maps:
    def __init__(self, project : Controller_Project, view:View_Main) -> None:
        self.project = project
        self.view = view

        pub.subscribe(self.load, "maps_load")
        pub.subscribe(self.update, "maps_update")

    def load(self):
        if self.project.isProjectLoaded == True:
            self.loadMapDataTable()
            
            self.maps = Model_Maps(self.project.romData.romData, self.project.projectData.projectData, self.mapData)
            self.view.maps.load(self.maps.mapNames)
            
    def loadMapDataTable(self):
        # load the map data table data from the project file
        self.mapDataTable = Model_MapDataTable()
        self.mapDataTable.load(self.project.projectData.projectData)

        self.mapData = []
        address = self.mapDataTable.mapDataTableAddress
        for mapIndex in range (Model_MapData.MAP_COUNT):
            mapData = Model_MapData(self.project.romData.romData)
            length = mapData.read(address, mapIndex)
            self.mapData.append(mapData)

            address += length
        
    def update(self, mapIndex):
        self.mapIndex = mapIndex
        # read the map data
        self.maps.maps[self.mapIndex].read()
        # create the map image
        mapImage = self.maps.maps[self.mapIndex].getImage(True, True, True, 0)
        self.view.maps.update(mapImage, self.maps.maps[self.mapIndex])