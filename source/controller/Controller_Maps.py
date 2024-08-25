from pubsub import pub

# notification
from pubsub.utils.notification import useNotifyByWriteFile

from controller.Controller_Project import Controller_Project
from model.Model_MapDataTable import Model_MapDataTable
from model.Model_MapData import Model_MapData
from view.View_Main import View_Main

class Controller_Maps:
    def __init__(self, project : Controller_Project, view:View_Main) -> None:
        self.project = project
        self.view = view

        self.mapDataTable = Model_MapDataTable()

        pub.subscribe(self.load, "maps_load")

    def load(self):
        if self.project.isProjectLoaded == True:
            # load the map data from the project file
            self.mapDataTable.load(self.project.projectData.projectData)

            self.mapData = []
            address = self.mapDataTable.mapDataTableAddress
            for mapIndex in range (Model_MapData.MAP_COUNT):
                mapData = Model_MapData(self.project.romData.romData)
                length = mapData.read(address, mapIndex)
                self.mapData.append(mapData)
                
                address += length

        