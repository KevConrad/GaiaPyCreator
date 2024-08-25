from model.Model_Tileset import Model_Tileset

class Model_Tilesets:
    def __init__(self, romData, projectData : dict) -> None:
        self.romData = romData

        # read all tileset data initially
        tilesets = projectData['Tilesets']
        self.tilesets = []
        self.tilesetNames = []

        for tileset in tilesets:
            tilesetData = Model_Tileset(self.romData, tileset)
            self.tilesets.append(tilesetData)
            self.tilesetNames.append(tilesetData.name)
            