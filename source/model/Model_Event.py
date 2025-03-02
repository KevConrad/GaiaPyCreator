import sys
from model.Model_RomData import Model_RomData

class Model_Event:
    class Type:
        npc = 0
        enemy = 1

    def __init__(self, romData, address) -> None:
        self.romData = romData
        readOffset = address

        self.positionX = romData[readOffset]
        readOffset += 1
        self.positionY = romData[readOffset]
        readOffset += 1
        self.triggerFlag = romData[readOffset]
        readOffset += 1
        self.address = Model_RomData.readLongAddress(romData, readOffset)
        readOffset += 3
        if (romData[readOffset] == 0):
            self.type = self.Type.npc
            self.eventByte = romData[readOffset]
            readOffset += 1
        else:
            self.type = self.Type.enemy
            self.enemyStateId = romData[readOffset]
            readOffset += 1
            self.eventByte = romData[readOffset]
            readOffset += 1
            self.enemyDefeatActionId = romData[readOffset]
            readOffset += 1

        self.size = readOffset - address
        