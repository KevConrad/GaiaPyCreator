from pubsub import pub

# notification
from pubsub.utils.notification import useNotifyByWriteFile

from controller.Controller_Project import Controller_Project
from model.Model_Tile import Model_Tile
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
        pub.subscribe(self.updateTileImage, "tilemaps_update_tileImage")
        pub.subscribe(self.updateTilemapImage, "tilemaps_update_tilemapImage")

    def load(self):
        if self.project.isProjectLoaded == True:
            # display the tilesets in the GUI
            self.view.tilemaps.load(self.tilemaps.tilemapNames)

    def update(self, tilemapIndex):
        self.tilemapIndex = tilemapIndex
        self.tilemaps.tilemaps[self.tilemapIndex].read()
        self.tilemapImage = self.tilemaps.tilemaps[self.tilemapIndex].getImage(readOffset = 0, readAll = True,
                                                                          tileOffset = 0, tilesetReadOffset = 0)
        self.view.tilemaps.update()

    def updateTilemapImage(self, currentPositionX, currentPositionY, selectedPositionX, selectedPositionY):
        tilemapImage = self.tilemaps.tilemaps[self.tilemapIndex].getImageOverlay(currentPositionX, currentPositionY,
                                                                                 selectedPositionX, selectedPositionY, True)
        # update the tilemap image in the GUI
        self.view.tilemaps.updateTilemapImage(tilemapImage)

    def updateTileImage(self, currentPositionX, currentPositionY, selectedPositionX, selectedPositionY):    
        tileImage = self.tilemaps.tilemaps[self.tilemapIndex].getImageOverlay(currentPositionX, currentPositionY,
                                                                              selectedPositionX, selectedPositionY, False)
        # update the tile image in the GUI
        self.view.tilemaps.updateTileImage(tileImage)

    def updateTile(self, tileIndex, tilePieceIndex):
        tileImage = self.tilemaps.tilemaps[self.tilemapIndex].getImage(readOffset = 0, readAll = False,
                                                                       tileOffset = tileIndex, tilesetReadOffset = 0)
        tileProperties = Model_Tile(self.tilemaps.tilemaps[self.tilemapIndex].tilemapData, tileIndex, tilePiece=tilePieceIndex)
        self.view.tilemaps.updateTileProperties(tileProperties)
        