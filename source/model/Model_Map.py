import PIL.Image
from model.Model_Compression import Model_Compression
from model.Model_MapData import Model_MapData
from model.Model_MapData0x0E import Model_MapData0x0E
from model.Model_MapDataArrangement import Model_MapDataArrangement
from model.Model_MapDataJump import Model_MapDataJump
from model.Model_MapDataJumpConditional import Model_MapDataJumpConditional
from model.Model_MapDataJumpSetAnchor import Model_MapDataJumpSetAnchor
from model.Model_MapDataMusic import Model_MapDataMusic
from model.Model_MapDataPalette import Model_MapDataPalette
from model.Model_MapDataScreenSettings import Model_MapDataScreenSettings
from model.Model_MapDataSprites import Model_MapDataSprites
from model.Model_MapDataTilemap import Model_MapDataTilemap
from model.Model_MapDataTileset import Model_MapDataTileset
from model.Model_Palette import Model_Palette
from model.Model_Paletteset import Model_Paletteset
from model.Model_Tileset import Model_Tileset

import bitstring

import PIL

class Model_Map:
    def __init__(self, romData, mapData : dict, tilemapData : dict, tilesetsData : dict, mapDataTableEntry : Model_MapData) -> None:
        self.romData = romData
        self.mapData = mapDataTableEntry.mapData

        # read the data from the JSON file
        self.name = str(mapData['Name'])

    def getImage(self):
        self.mapArrangement = []

        for dataEntry in self.mapData:
            if type(dataEntry) is Model_MapDataArrangement:
                dataEntry.read()


    