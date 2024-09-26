import PIL.Image
from model.Model_Compression import Model_Compression
from model.Model_Palette import Model_Palette
from model.Model_Paletteset import Model_Paletteset
from model.Model_Tileset import Model_Tileset

import bitstring

import PIL

class Model_Map:
    def __init__(self, romData, mapData : dict, tilemapData : dict, tilesetsData : dict) -> None:
        self.romData = romData

        # read the data from the JSON file
        self.name = str(mapData['Name'])

    