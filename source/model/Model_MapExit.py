from model.Model_RomDataTable import Model_RomDataTable
import sys

class Model_MapExit:
    
    # The type of the exit (TELEPORT or STAIRS).
    class ExitType:
        TELEPORT = 0
        STAIRS = 1

    class PlayerDirection:
        DOWN = 1
        LEFT = 6
        RIGHT = 7
        UP = 0

    def __init__(self, romData, address, type : ExitType) -> None:
        self.romData = romData

        self.type = type

        self.readExitData(address, type)

    def readExitData(self, address, type):
        self.size = 0

        # read the general exit data
        readOffset = address
        self.positionX = self.romData[readOffset]
        readOffset += 1
        self.positionY = self.romData[readOffset]
        readOffset += 1
        self.width = self.romData[readOffset]
        readOffset += 1
        self.height = self.romData[readOffset]
        readOffset += 1

        if type is self.ExitType.TELEPORT:
            self.destinationMapId = self.romData[readOffset]
            readOffset += 1
            # read the destination X data
            self.destinationX = (self.romData[readOffset] & 0xF0) >> 4
            self.destinationPixelOffsetX = self.romData[readOffset] & 0x0F
            readOffset += 1
            self.destinationX = self.destinationX + self.romData[readOffset] * 16
            readOffset += 1
            # read the destination Y data
            self.destinationY = (self.romData[readOffset] & 0xF0) >> 4
            self.destinationPixelOffsetY = self.romData[readOffset] & 0x0F
            readOffset += 1
            self.destinationY = self.destinationY + self.romData[readOffset] * 16
            readOffset += 1

            self.playerDirection = self.romData[readOffset]
            readOffset += 1
            self.screenOffset = self.romData[readOffset]
            readOffset += 1

            # read the map size
            self.mapSizeX = (self.romData[readOffset] & 0xF0) * 16
            self.mapSizeY = ((self.romData[readOffset] & 0xF0) >> 4) * 16
        else:
            self.stairsByte0 = self.romData[readOffset]
            readOffset += 1
            self.stairsByte1 = self.romData[readOffset]
            readOffset += 1

            # read the scroll movement data
            self.stairsScrollMovementDirection = self.romData[readOffset] & 0xF0
            self.stairsScrollMovementId = self.romData[readOffset] & 0x0F
            readOffset += 1
            # read the player direction before scroll movement
            self.stairsPlayerDirectionBefore = self.romData[readOffset]
            readOffset += 1
            # read the stairs offset in X direction
            self.stairsOffsetX = (self.romData[readOffset] & 0xF0) >> 4
            self.stairsPixelOffsetX = self.romData[readOffset] & 0x0F
            readOffset += 1
            self.stairsOffsetX = self.stairsOffsetX + (self.romData[readOffset] * 16)
            readOffset += 1
            # read the stairs offset in Y direction
            self.stairsOffsetY = (self.romData[readOffset] & 0xF0) >> 4
            self.stairsPixelOffsetY = self.romData[readOffset] & 0x0F
            readOffset += 1
            self.stairsOffsetY = self.stairsOffsetY + (self.romData[readOffset] * 16)
            readOffset += 1
            # read the player direction after scroll movement
            self.stairsPlayerDirectionAfter = self.romData[readOffset]
            readOffset += 1
            
        self.size = readOffset - address
            
    def getStepsDirectionName(self, rawData):
        switch = {
            self.PlayerDirection.DOWN : 'Down',
            self.PlayerDirection.LEFT : 'Left',
            self.PlayerDirection.RIGHT : 'Right',
            self.PlayerDirection.UP : 'Up'
        }
        return switch.get(rawData, chr(rawData))

    