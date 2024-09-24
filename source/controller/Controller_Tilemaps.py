from pubsub import pub

# notification
from pubsub.utils.notification import useNotifyByWriteFile

from controller.Controller_Project import Controller_Project
from model.Model_Tilemaps import Model_Tilemaps
from view.View_Main import View_Main

class Controller_Tilemaps:
    def __init__(self, project : Controller_Project, view:View_Main) -> None:
        self.project = project
        self.view = view

        self.tilemaps = Model_Tilemaps(self.project.romData.romData, self.project.projectData.projectData)

        pub.subscribe(self.load, "tilemaps_load")
        pub.subscribe(self.update, "tilemaps_update")
        pub.subscribe(self.updateTile, "tilemaps_update_tile")

    def load(self):
        if self.project.isProjectLoaded == True:
            # display the tilesets in the GUI
            self.view.tilemaps.load(self.tilemaps.tilemapNames)

    def update(self, tilemapIndex):
        self.tilemapIndex = tilemapIndex
        self.tilemaps.tilemaps[self.tilemapIndex].read()
        tilemapImage = self.tilemaps.tilemaps[self.tilemapIndex].getImage(readOffset = 0, readAll = True,
                                                                          tileOffset = 0, tilesetReadOffset = 0,
                                                                          tilePieceOffset = 0)
        self.view.tilemaps.update(tilemapImage)

    def updateTile(self, tileIndex):
        tileImage = self.tilemaps.tilemaps[self.tilemapIndex].getImage(readOffset = 0, readAll = False,
                                                                       tileOffset = tileIndex, tilesetReadOffset = 0,
                                                                       tilePieceOffset = 0)
        self.view.tilemaps.updateTile(tileImage)
        