import sys
from model.Model_MapExit import Model_MapExit

class Model_MapExits:
    def __init__(self, romData, address) -> None:
        readOffset = address

        self.exits = []

        # read all exit teleport data sets
        while (romData[readOffset] != 0xFF):
            exitData = Model_MapExit(romData, readOffset, Model_MapExit.ExitType.TELEPORT)
            self.exits.append(exitData)
            readOffset += exitData.size
                                        
        readOffset += 1

        # read all exit stairs data sets
        while (romData[readOffset] != 0xFF):
            exitData = Model_MapExit(romData, readOffset, Model_MapExit.ExitType.STAIRS)
            self.exits.append(exitData)
            readOffset += exitData.size

