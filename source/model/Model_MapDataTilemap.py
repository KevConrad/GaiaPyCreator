from model.Model_RomData import Model_RomData
from model.Model_Tilemaps import Model_Tilemaps

class Model_MapDataTilemap:
    def __init__(self, romData, address, tilemaps:Model_Tilemaps) -> None:
        self.romData = romData

        # read the tilemap data
        readOffset = address
        self.byte0 = self.romData[readOffset]
        readOffset += 1
        self.byte1 = self.romData[readOffset]
        readOffset += 1
        self.byte2 = self.romData[readOffset]
        readOffset += 1
        self.slotId = self.romData[readOffset]
        readOffset += 1
        self.address = Model_RomData.readLongAddress(self.romData, readOffset)
        readOffset += 3
    
        # set the tilemap index
        index = 0
        for tilemap in tilemaps.tilemaps:
            if tilemap.address == self.address:
                self.index = index
                break
            index += 1

        self.size = readOffset - address
            