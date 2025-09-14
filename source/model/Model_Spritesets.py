from model.Model_Spriteset import Model_Spriteset
from model.Model_Tilesets import Model_Tilesets

class Model_Spritesets:
    def __init__(self, romData, projectData : dict, tilesets:Model_Tilesets) -> None:
        self.romData = romData

        # read all tilemap data initially
        spritesets = projectData['Spritesets']
        self.spritesets = []
        self.spritesetNames = []

        for spriteset in spritesets:
            spritesetData = Model_Spriteset(self.romData, spriteset, tilesets)
            self.spritesets.append(spritesetData)
            self.spritesetNames.append(spritesetData.name)

    def getIndexfromAddress(self, address):
        # get the index of the tileset with the given address
        for index, spriteset in enumerate(self.spritesets):
            if spriteset.address == address:
                return index
        return -1
    