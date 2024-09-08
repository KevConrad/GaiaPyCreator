from model.Model_Tilemap import Model_Tilemap

class Model_Tilemaps:
    def __init__(self, romData, projectData : dict) -> None:
        self.romData = romData

        # read all tilemap data initially
        tilemaps = projectData['Tilemaps']
        # read all tileset data because it is needed by the tilemaps
        tilesets = projectData['Tilesets']
        self.tilemaps = []
        self.tilemapNames = []

        for tilemap in tilemaps:
            tilemapData = Model_Tilemap(self.romData, tilemap, tilesets)
            self.tilemaps.append(tilemapData)
            self.tilemapNames.append(tilemapData.name)
            