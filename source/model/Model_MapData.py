from model.Model_MapData0x0E import Model_MapData0x0E
from model.Model_MapDataArrangement import Model_MapDataArrangement
from model.Model_MapDataJump import Model_MapDataJump
from model.Model_MapDataJumpConditional import Model_MapDataJumpConditional
from model.Model_MapDataJumpSetAnchor import Model_MapDataJumpSetAnchor
from model.Model_MapDataMusic import Model_MapDataMusic
from model.Model_MapDataPalette import Model_MapDataPalette
from model.Model_MapDataScreenSettings import Model_MapDataScreenSettings
from model.Model_MapDataSprites import Model_MapDataSprites
from model.Model_MapDataTilemap import Model_MapDataTilemap
from model.Model_MapDataTileset import Model_MapDataTileset

from model.Model_MapDataBuffer import Model_MapDataBuffer

from model.Model_Tilemaps import Model_Tilemaps
from model.Model_Tilesets import Model_Tilesets

import copy

class Model_MapData:
    MAP_COUNT = 256
    MAP_DATA_0x0E = 0x0E
    MAP_DATA_ARRANGEMENT = 0x06
    MAP_DATA_END_FLAG = 0x00
    MAP_DATA_JUMP = 0x15
    MAP_DATA_JUMP_CONDITIONAL = 0x13
    MAP_DATA_JUMP_SET_ANCHOR = 0x14
    MAP_DATA_MUSIC = 0x11
    MAP_DATA_PALETTE = 0x04
    MAP_DATA_SCREEN_SETTINGS = 0x02
    MAP_DATA_SPRITES = 0x10
    MAP_DATA_TILEMAP = 0x05
    MAP_DATA_TILESET = 0x03

    def __init__(self, romData, tilemaps:Model_Tilemaps, tilesets:Model_Tilesets) -> None:
        self.romData = romData
        self.tilemaps = tilemaps
        self.tilesets = tilesets
    
    def read(self, address, index, mapDataBuffer : Model_MapDataBuffer):
        readOffset = address
        self.index = index
        self.mapData = []

        # check if a data set exists for the map
        tempIndex = self.romData[readOffset] + (self.romData[readOffset + 1] << 8)
        readOffset += 2

        if ((index == tempIndex) or (tempIndex == 0x9070)):
            self.hasDataSet = True

            while (self.romData[readOffset] != self.MAP_DATA_END_FLAG):
                isDataSetFound = True
                functionNumber = self.romData[readOffset]
                readOffset += 1

                if (functionNumber == self.MAP_DATA_0x0E):                  # ??? (0x0E)
                    mapData = Model_MapData0x0E(self.romData, readOffset)

                elif (functionNumber == self.MAP_DATA_ARRANGEMENT):         #  map arrangement data (0x06)
                    mapData = Model_MapDataArrangement(self.romData, readOffset)

                elif (functionNumber == self.MAP_DATA_JUMP):                # jump to a function (?) (0x15)    
                    mapData = Model_MapDataJump(self.romData, readOffset)

                elif (functionNumber == self.MAP_DATA_JUMP_CONDITIONAL):    # ??? (0x13)
                    mapData = Model_MapDataJumpConditional(self.romData, readOffset)

                elif (functionNumber == self.MAP_DATA_JUMP_SET_ANCHOR):     # load a byte (?) (0x14)
                    mapData = Model_MapDataJumpSetAnchor(self.romData, readOffset)

                elif (functionNumber == self.MAP_DATA_MUSIC):               # music data (0x11)        
                    mapData = Model_MapDataMusic(self.romData, readOffset)

                elif (functionNumber == self.MAP_DATA_PALETTE):             # palette data (0x04)
                    mapData = Model_MapDataPalette(self.romData, readOffset)
                    mapDataBuffer.setPaletteBuffer(mapData)
                    # TODO add palette to general palette array

                elif (functionNumber == self.MAP_DATA_SCREEN_SETTINGS):     # screen settings (0x02)
                    mapData = Model_MapDataScreenSettings(self.romData, readOffset)

                elif (functionNumber == self.MAP_DATA_SPRITES):             # sprite data (0x10)
                    mapData = Model_MapDataSprites(self.romData, readOffset)
                    # TODO add spriteset to general sprite array

                elif (functionNumber == self.MAP_DATA_TILEMAP):             # tilemap data (0x05)
                    mapData = Model_MapDataTilemap(self.romData, readOffset, self.tilemaps)
                    mapDataBuffer.setTilemapBuffer(mapData)
                    # TODO add tilemap to general tilemap array

                    # add identical tilemap data if both slots are used
                    if mapData.slotId == 3:
                        self.mapData.append(copy.deepcopy(mapData))
                        mapDataBuffer.setTilemapBuffer(mapData)
                        mapDataBuffer.setTilemapBuffer(mapData)

                elif (functionNumber == self.MAP_DATA_TILESET):             # tileset data (0x03)
                    mapData = Model_MapDataTileset(self.romData, readOffset, self.tilesets)

                    if mapData.layer == Model_MapDataTileset.LAYER_BG1_BG2:
                        mapData.layer = Model_MapDataTileset.LAYER_BG1
                        # mapData will be added to the array at the end of the loop
                        # add second tileset data directly here
                        tilesetSecondData = copy.deepcopy(mapData)
                        tilesetSecondData.index = mapData.index + 1
                        tilesetSecondData.layer = Model_MapDataTileset.LAYER_BG2
                        self.mapData.append(tilesetSecondData)
                        mapDataBuffer.setTilesetBuffer(tilesetSecondData)
                    else:
                        self.mapData.append(mapData)
                    mapDataBuffer.setTilesetBuffer(mapData)                                          
                    # TODO add tileset to general tileset array

                else:
                     isDataSetFound = False                                 # no valid function number found

                if (isDataSetFound == True):
                    self.mapData.append(mapData)
                    readOffset += mapData.size
            readOffset += 1

            self.getPaletteFromBuffer(mapDataBuffer)
            self.getTilemapFromBuffer(mapDataBuffer)
            self.getTilesetFromBuffer(mapDataBuffer)
        else:
            self.hasDataSet = False
            readOffset -= 2

        return readOffset - address

    def getTilemapCount(self):
        tilemapCount = 0
        for dataEntry in self.mapData:
            if type(dataEntry) is Model_MapDataTilemap:
                tilemapCount += 1
        return tilemapCount
    
    def getTilesetCount(self):
        tilesetCount = 0
        for dataEntry in self.mapData:
            if type(dataEntry) is Model_MapDataTileset:
                tilesetCount += 1
        return tilesetCount
    
    def getPaletteFromBuffer(self, mapDataBuffer : Model_MapDataBuffer):
        hasMapLayer = False

        for dataEntry in self.mapData:
            if type(dataEntry) is Model_MapDataPalette:
                if dataEntry.layer == Model_MapDataPalette.MAP_LAYER:
                    hasMapLayer = True

        if hasMapLayer == False:
            self.mapData.append(mapDataBuffer.paletteBuffer[0])

    def getTilemapFromBuffer(self, mapDataBuffer : Model_MapDataBuffer):
        if ((self.getTilemapCount() == 0) and (self.index > 0)):
            for i in range (3):
                self.mapData.append(mapDataBuffer.tilemapBuffer[i])

    def getTilesetFromBuffer(self, mapDataBuffer : Model_MapDataBuffer):
        hasBG1Layer = False
        hasBG2Layer = False
        
        for dataEntry in self.mapData:
            if type(dataEntry) is Model_MapDataTileset:
                if dataEntry.layer == Model_MapDataTileset.LAYER_BG1:
                    hasBG1Layer = True
                elif dataEntry.layer == Model_MapDataTileset.LAYER_BG2:
                    hasBG2Layer = True
                elif dataEntry.layer== Model_MapDataTileset.LAYER_BG1_BG2:
                    hasBG1Layer = True
                    hasBG2Layer = True
                else:
                    pass

        if hasBG1Layer == False:
            self.mapData.append(mapDataBuffer.tilesetBuffer[0])
        if hasBG2Layer == False:
            self.mapData.append(mapDataBuffer.tilesetBuffer[1])
