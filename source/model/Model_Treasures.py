
from model.Model_MapData import Model_MapData
from model.Model_RomDataTable import Model_RomDataTable
from model.Model_Treasure import Model_Treasure

class Model_Treasures:
    TREASURE_DATA_SET_END = 0xFF

    def __init__(self, romData, address) -> None:
        self.romData = romData

        readOffset = address

        # read all treasure data sets
        self.treasures = []
        while (romData[readOffset] != self.TREASURE_DATA_SET_END):
            treasureData = Model_Treasure(romData, readOffset)
            self.treasures.append(treasureData)
            readOffset += Model_Treasure.TREASURE_DATA_SET_SIZE
                                        
        readOffset += 1
    