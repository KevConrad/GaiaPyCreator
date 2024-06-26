from model.Model_RomDataTable import Model_RomDataTable
from model.Model_Tileset import Model_Tileset
import sys

from pubsub import pub

class Model_Tilesets:
    def __init__(self, romData, projectData : dict, updateFunction) -> None:
        self.romData = romData

        # read all tileset data initially
        tilesets = projectData['Tilesets']
        self.tilesets = []
        self.tilesetNames = []
        i = 0
        for tileset in tilesets:
            tilesetData = Model_Tileset(self.romData, tileset)
            self.tilesets.append(tilesetData)
            self.tilesetNames.append(tilesetData.name)
            i += 1
            pub.sendMessage("progressBar_update", updateValue=(int((i / len(tilesets)) * 100)))
        pub.sendMessage("progressBar_update", updateValue=100)

    def load(self, projectData : dict):
        pass
            