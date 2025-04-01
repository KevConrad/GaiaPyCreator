from model.Model_RomDataTable import Model_RomDataTable
import sys

class Model_MapExit:
    
    # The type of the exit (TELEPORT or STAIRS).
    class ExitType:
        TELEPORT = 0
        STAIRS = 1

    class PlayerDirection:
        DOWN = 0
        LEFT = 1
        RIGHT = 2
        UP = 3

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

            self.playerDirection = self.read_direction(self.romData[readOffset])
            readOffset += 1
            self.screenOffset = self.romData[readOffset]
            readOffset += 1

            # read the map size
            self.mapSizeX = (self.romData[readOffset] & 0x0F) * 16
            self.mapSizeY = ((self.romData[readOffset] & 0xF0) >> 4) * 16
            readOffset += 1
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
    
    def read_direction(self, direction):
        if direction == 0:
            player_direction = self.PlayerDirection.UP
        elif direction == 1:
            player_direction = self.PlayerDirection.DOWN
        elif direction == 2:
            player_direction = self.PlayerDirection.UP
        elif direction == 3:
            player_direction = self.PlayerDirection.DOWN
        elif direction == 4:
            player_direction = self.PlayerDirection.UP
        elif direction == 5:
            player_direction = self.PlayerDirection.UP
        elif direction == 6:
            player_direction = self.PlayerDirection.LEFT
        elif direction == 7:
            player_direction = self.PlayerDirection.RIGHT
        else:
            # TODO: Error handling
            player_direction = self.PlayerDirection.DOWN

        return player_direction