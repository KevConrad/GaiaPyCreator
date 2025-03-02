import sys
from model.Model_MapExit import Model_MapExit

class Model_MapExits:
    EXIT_DATA_SET_END = 0xFF

    def __init__(self, romData, address) -> None:
        readOffset = address

        # read all exit teleport data sets
        self.teleports = []
        while (romData[readOffset] != self.EXIT_DATA_SET_END):
            exitData = Model_MapExit(romData, readOffset, Model_MapExit.ExitType.TELEPORT)
            self.teleports.append(exitData)
            readOffset += exitData.size
                                        
        readOffset += 1

        # read all exit stairs data sets
        self.steps = []
        while (romData[readOffset] != self.EXIT_DATA_SET_END):
            exitData = Model_MapExit(romData, readOffset, Model_MapExit.ExitType.STAIRS)
            self.steps.append(exitData)
            readOffset += exitData.size

