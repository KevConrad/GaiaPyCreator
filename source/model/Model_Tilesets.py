from model.Model_RomDataTable import Model_RomDataTable
from model.Model_Tileset import Model_Tileset
import sys

class Model_Tilesets:
    def __init__(self, romData) -> None:
        self.romData = romData

    def load(self, projectData : dict):
        tilesetData = projectData['Tilesets']
        self.tilesetNames = []
        self.tilesets = []
        i = 0
        for tileset in tilesetData:
            tilesetData = Model_Tileset(self.romData, tileset)
            self.tilesets.append(tilesetData)
            self.tilesetNames.append(tilesetData.name)
            
            if i >= 15:
                break
            i += 1
            
        #print(self.tilesets)