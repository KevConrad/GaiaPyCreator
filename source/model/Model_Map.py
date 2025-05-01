import PIL.Image
from model.Model_Compression import Model_Compression
from model.Model_MapData import Model_MapData
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
from model.Model_MapEvents import Model_MapEvents
from model.Model_MapExits import Model_MapExits
from model.Model_Palette import Model_Palette
from model.Model_Paletteset import Model_Paletteset
from model.Model_RomDataTable import Model_RomDataTable
from model.Model_RoomClearingRewards import Model_RoomClearingRewards
from model.Model_ScreenSettings import Model_ScreenSettings
from model.Model_ScreenSetting import Model_ScreenSetting
from model.Model_Tilemap import Model_Tilemap
from model.Model_Tileset import Model_Tileset

import bitstring

import PIL

class Model_Map:
    def __init__(self, romData, mapData : dict, projectData : dict, mapDataTableEntry : Model_MapData,
                 mapIndex, screenSettings : Model_ScreenSettings, roomClearingRewards : Model_RoomClearingRewards) -> None:
        self.romData = romData

        # read the data from the JSON file
        self.name = str(mapData['Name'])

        self.mapData0x0E = []
        self.mapDataArrangement = [] 
        self.mapDataJump = []
        self.mapDataJumpConditional = []
        self.mapDataJumpSetAnchor = []
        self.mapDataMusic = []
        self.mapDataPalette = []
        self.mapDataScreenSettings = []
        self.mapDataSprites = []
        self.mapDataTilemap = []
        self.mapDataTileset = []

        for dataEntry in mapDataTableEntry.mapData:
            if type(dataEntry) is Model_MapData0x0E:
                self.mapData0x0E.append(dataEntry)
            if type(dataEntry) is Model_MapDataArrangement:
                self.mapDataArrangement.append(dataEntry)
            if type(dataEntry) is Model_MapDataJump:
                self.mapDataJump.append(dataEntry)
            if type(dataEntry) is Model_MapDataJumpConditional:
                self.mapDataJumpConditional.append(dataEntry)
            if type(dataEntry) is Model_MapDataJumpSetAnchor:
                self.mapDataJumpSetAnchor.append(dataEntry)
            if type(dataEntry) is Model_MapDataMusic:
                self.mapDataMusic.append(dataEntry)
            if type(dataEntry) is Model_MapDataPalette:
                self.mapDataPalette.append(dataEntry)
            if type(dataEntry) is Model_MapDataScreenSettings:
                self.mapDataScreenSettings.append(dataEntry)
            if type(dataEntry) is Model_MapDataSprites:
                self.mapDataSprites.append(dataEntry)
            if type(dataEntry) is Model_MapDataTilemap:
                self.mapDataTilemap.append(dataEntry)
            if type(dataEntry) is Model_MapDataTileset:
                self.mapDataTileset.append(dataEntry)

        # get the room clearing reward
        self.roomClearingReward = roomClearingRewards.roomClearingRewards[mapIndex].roomClearingReward
        
        if len(self.mapDataScreenSettings) > 0:
            # get the screen settings
            self.screenSettings = screenSettings.screenSettings[self.mapDataScreenSettings[0].index]
        
        # set the map size in x direction
        if ((len(self.mapDataArrangement) > 1) and 
            (self.mapDataArrangement[1].sizeX > self.mapDataArrangement[0].sizeX)):
            self.sizeX = self.mapDataArrangement[1].sizeX
        elif (len(self.mapDataArrangement) > 0):
            self.sizeX = self.mapDataArrangement[0].sizeX
        else:
            self.sizeX = 0

        # set the map size in y direction
        if ((len(self.mapDataArrangement) > 1) and 
            (self.mapDataArrangement[1].sizeY > self.mapDataArrangement[0].sizeY)):
            self.sizeY = self.mapDataArrangement[1].sizeY
        elif (len(self.mapDataArrangement) > 0):
            self.sizeY = self.mapDataArrangement[0].sizeY
        else:
            self.sizeY = 0

        # read the map event data
        eventDataTableAddress = int(str(projectData['DataTables']['MapEventTable']['Address']), 16)
        eventDataTableSize = int(projectData['DataTables']['MapEventTable']['Size'], base=16)
        eventDataTable = Model_RomDataTable(self.romData, eventDataTableAddress, eventDataTableSize)  
        self.events = Model_MapEvents(self.romData, eventDataTable.getDataAddress(mapIndex))

        # read the map exit data
        exitDataTableAddress = int(str(projectData['DataTables']['MapExitTable']['Address']), 16)
        exitDataTableSize = int(projectData['DataTables']['MapExitTable']['Size'], base=16)
        exitDataTable = Model_RomDataTable(self.romData, exitDataTableAddress, exitDataTableSize)  
        self.exits = Model_MapExits(self.romData, exitDataTable.getDataAddress(mapIndex))

    def read(self):
        if len(self.mapDataArrangement) > 0:
            self.mapDataArrangement[0].read()
        if len(self.mapDataArrangement) > 1:
            self.mapDataArrangement[1].read()
            
        self.tilemapData = []
        if len(self.mapDataTilemap) > 0:
            # decompress the compressed tilemap data (increment length of compressed data to prevent data truncation)
            tilemapData, self.compSize = Model_Compression.decompress(self.romData, self.mapDataTilemap[0].address, 10000, 0)
            self.tilemapData.append(tilemapData)
        if len(self.mapDataTilemap) > 1:
            # decompress the compressed tilemap data (increment length of compressed data to prevent data truncation)
            tilemapData, self.compSize = Model_Compression.decompress(self.romData, self.mapDataTilemap[1].address, 10000, 0)
            self.tilemapData.append(tilemapData)

        # read BG1 layer tileset data
        self.tilesetIndexBG1, decompOffset = self.getTilesetIndex(Model_MapDataTileset.LAYER_BG1)
        if self.tilesetIndexBG1 >= 0:
            # decompress the compressed tileset data (increment length of compressed data to prevent data truncation)
            self.tilesetDataBG1, self.tilesetBG1CompSize = Model_Compression.decompress(self.romData, self.mapDataTileset[self.tilesetIndexBG1].addressDecomp,
                                                                                        0x4000,
                                                                                        decompOffset)
        # read BG2 layer tileset data
        self.tilesetIndexBG2, decompOffset = self.getTilesetIndex(Model_MapDataTileset.LAYER_BG2)
        if self.tilesetIndexBG2 >= 0:
            # decompress the compressed tileset data (increment length of compressed data to prevent data truncation)
            self.tilesetDataBG2, self.tilesetBG2CompSize = Model_Compression.decompress(self.romData, self.mapDataTileset[self.tilesetIndexBG2].addressDecomp,
                                                                                        0x4000,
                                                                                        decompOffset)
        # read map palette data
        paletteIndexMap = self.getPaletteIndex(Model_MapDataPalette.MAP_LAYER)
        if paletteIndexMap >= 0:
            self.palettesetMap = Model_Paletteset(self.romData, self.mapDataPalette[paletteIndexMap].address)

        # read sprites palette data
        paletteIndexMap = self.getPaletteIndex(Model_MapDataPalette.SPRITE_LAYER)
        if paletteIndexMap >= 0:
            self.palettesetSprites = Model_Paletteset(self.romData, self.mapDataPalette[paletteIndexMap].address)
    
    def createImage(self, isBG1LayerDisplayed, isBG2LayerDisplayed, isSpriteLayerDisplayed, screenSettings):          
        # read all tilesets that are used by the map

        # array which contains the data of both tilesets used by the map
        self.tilesetBits = []

        if self.tilesetIndexBG1 >= 0:
            self.tilesetBits.append(bitstring.ConstBitStream(bytes = self.tilesetDataBG1, offset=0,
                                                               length=Model_Tileset.TILESET_BYTE_SIZE * 8))
        
        if self.tilesetIndexBG2 >= 0:
            self.tilesetBits.append(bitstring.ConstBitStream(bytes = self.tilesetDataBG2, offset=0,
                                                               length=Model_Tileset.TILESET_BYTE_SIZE * 8))

        # read the map layers
        self.pixelWidth = self.sizeX * Model_Tilemap.TILEMAP_TILE_PIXEL_WIDTH
        self.pixelHeight = self.sizeY * Model_Tilemap.TILEMAP_TILE_PIXEL_HEIGHT
        self.pixelValues = [0] * (self.pixelWidth * self.pixelHeight)
        self.imageBytes = [0] * (self.pixelWidth * self.pixelHeight * 3)

        if self.screenSettings is not None:
            mapLayerOrder = self.screenSettings.mapLayerOrderBits
            if (((mapLayerOrder & Model_ScreenSetting.MAP_LAYER_ORDER_HAS_NORMAL_MAP_LAYERS) == 0x00) and
                (len(self.mapDataArrangement) > 1)): # TODO: Query of arrangementCount > 1 should not be necessary!
                if isBG2LayerDisplayed is True:
                    self.createLayer(self.sizeX, 1)
                if isBG1LayerDisplayed is True:
                    self.createLayer(self.sizeX, 0)              
            else:
                if isBG1LayerDisplayed is True:
                    self.createLayer(self.sizeX, 0)    
                if (isBG2LayerDisplayed is True) and (len(self.mapDataArrangement) > 1):
                    self.createLayer(self.sizeX, 1)
        else:
            if isBG1LayerDisplayed is True:
                self.createLayer(self.sizeX, 0)
            if (isBG2LayerDisplayed is True) and (len(self.mapDataArrangement) > 1):
                self.createLayer(self.sizeX, 1)
        # TODO add display of sprite layer
        #if (isSpriteLayerDisplayed is True) and (data.getSpriteCount() > 0))
            # read the map overlay (events, exits, sprites) and write it to the bitmap pixel value array
            #displayOverlay(mapSizeX, mapSizeY, tilesetBits, pixelValues);

        # create an RGB pixel array with the selected palette and the readout palette color index
        pixelIndex = 0
        for pixelValue in self.pixelValues:
            paletteIndex = int(float(pixelValue / 16))
            colorIndex = (pixelValue % 16)
            palette = self.palettesetMap.palettes[paletteIndex]
            self.imageBytes[pixelIndex + 0] = palette.data[((colorIndex * 3) + 0)]   # red
            self.imageBytes[pixelIndex + 1] = palette.data[((colorIndex * 3) + 1)]   # green
            self.imageBytes[pixelIndex + 2] = palette.data[((colorIndex * 3) + 2)]   # blue
            pixelIndex = pixelIndex + 3

        # create an image from the RGB pixel array
        self.mapImage = PIL.Image.frombytes('RGB', (self.pixelWidth, self.pixelHeight), bytes(self.imageBytes), 'raw')

    def createEventImage(self, selectedEventIndex):
        # create the array containing the image bytes
        pixelWidth = self.sizeX * Model_Tilemap.TILEMAP_TILE_PIXEL_WIDTH
        pixelHeight = self.sizeY * Model_Tilemap.TILEMAP_TILE_PIXEL_HEIGHT
        self.eventImageBytes = self.imageBytes.copy()

        # read the map events and write the event overlay to the bitmap pixel value array
        eventIndex = 0
        for event in self.events.events:
            if (event.positionX > self.sizeX) or (event.positionY > self.sizeY):
                continue
            # calculate the pixel index of the current event
            pixelIndex = (pixelWidth * 3 * event.positionY * Model_Tilemap.TILEMAP_TILE_PIXEL_HEIGHT) + Model_Tilemap.TILEMAP_TILE_PIXEL_WIDTH * 3 * event.positionX
            for height in range (Model_Tilemap.TILEMAP_TILE_PIXEL_HEIGHT):
                for width in range (Model_Tilemap.TILEMAP_TILE_PIXEL_WIDTH):
                    pixelOffsetX = 3 * width
                    pixelOffsetY = pixelWidth * 3 * height
                    # check if the event is selected
                    if eventIndex == selectedEventIndex:
                        if ((height == 0) or
                            (height == (Model_Tilemap.TILEMAP_TILE_PIXEL_HEIGHT - 1)) or
                            (width == 0) or
                            (width == (Model_Tilemap.TILEMAP_TILE_PIXEL_WIDTH - 1))):
                            self.eventImageBytes[pixelIndex + pixelOffsetX + pixelOffsetY + 0] = 0xFF
                            self.eventImageBytes[pixelIndex + pixelOffsetX + pixelOffsetY + 1] = 0xFF
                            self.eventImageBytes[pixelIndex + pixelOffsetX + pixelOffsetY + 2] = 0xFF
                        else:
                            self.eventImageBytes[pixelIndex + pixelOffsetX + pixelOffsetY + 0] = 0xFF
                    else:
                        self.eventImageBytes[pixelIndex + pixelOffsetX + pixelOffsetY + 0] = 0xFF
            eventIndex += 1
        
        # create an image from the RGB pixel array
        self.eventImage = PIL.Image.frombytes('RGB', (pixelWidth, pixelHeight), bytes(self.eventImageBytes), 'raw')

    def createExitImage(self, selectedExitIndex):
        # create the array containing the image bytes
        pixelWidth = self.sizeX * Model_Tilemap.TILEMAP_TILE_PIXEL_WIDTH
        pixelHeight = self.sizeY * Model_Tilemap.TILEMAP_TILE_PIXEL_HEIGHT
        self.exitImageBytes = self.imageBytes.copy()

        # read the map exits and write the exit overlay to the bitmap pixel value array
        exitIndex = 0
        for exit in self.exits.exits:
            pixelIndex = (pixelWidth * 3 * exit.positionY * Model_Tilemap.TILEMAP_TILE_PIXEL_HEIGHT) + Model_Tilemap.TILEMAP_TILE_PIXEL_WIDTH * 3 * exit.positionX
            for exitSizeY in range (exit.height):
                for exitSizeX in range (exit.width):
                    for height in range (Model_Tilemap.TILEMAP_TILE_PIXEL_HEIGHT):
                        for width in range (Model_Tilemap.TILEMAP_TILE_PIXEL_WIDTH):
                            pixelOffsetX = 3 * ((exitSizeX * Model_Tilemap.TILEMAP_TILE_PIXEL_WIDTH) + width)
                            pixelOffsetY = pixelWidth * 3 * (height + (Model_Tilemap.TILEMAP_TILE_PIXEL_HEIGHT * exitSizeY))
                            if exitIndex == selectedExitIndex:
                                if (((height == 0) and (exitSizeY == 0)) or
                                    ((height == (Model_Tilemap.TILEMAP_TILE_PIXEL_HEIGHT - 1)) and (exitSizeY == (exit.height - 1))) or
                                    ((width == 0) and (exitSizeX == 0)) or
                                    ((width == (Model_Tilemap.TILEMAP_TILE_PIXEL_WIDTH - 1) and (exitSizeX == (exit.width - 1))))):
                                    self.exitImageBytes[pixelIndex + pixelOffsetX + pixelOffsetY + 0] = 0xFF
                                    self.exitImageBytes[pixelIndex + pixelOffsetX + pixelOffsetY + 1] = 0xFF
                                    self.exitImageBytes[pixelIndex + pixelOffsetX + pixelOffsetY + 2] = 0xFF
                                else:
                                    self.exitImageBytes[pixelIndex + pixelOffsetX + pixelOffsetY + 2] = 0xFF
                            else:
                                self.exitImageBytes[pixelIndex + pixelOffsetX + pixelOffsetY + 2] = 0xFF
            exitIndex += 1
        
        # create an image from the RGB pixel array
        self.exitImage = PIL.Image.frombytes('RGB', (pixelWidth, pixelHeight), bytes(self.exitImageBytes), 'raw')

    def createLayer(self, mapSizeX, layer):
        tilePos = 0
        
        # read the arrangement index for the current map layer
        arrangementDataIndex = self.getArrangementDataIndexOfLayer(layer)
            
        # read the tilemap index for the current map layer
        tilemapOffset = self.getTilemapIndexOfLayer(layer)
        
        # loop through all map block rows (offset = 65536)
        for blockY in range(int(float(self.mapDataArrangement[layer].sizeY / 16))):
            # loop through all map blocks of a map block row (offset = 256)
            for blockX in range (int(float(self.mapDataArrangement[layer].sizeX / 16))):
                # loop through the 16 map tile rows of a map block (offset = 256)
                for tileY in range (16):
                    # loop through the 16 map tiles of a map tile row
                    for tileX in range (16):
                        # read the index of the current tile from the arrangement data
                        tileIndex = self.mapDataArrangement[arrangementDataIndex].data[tilePos]

                        # loop through the 4 map tile pieces
                        for tilePiece in range (4):
                            tilesetReadIndex = 0 # TODO layer

                            # read the x and y index of the current tile from the tilemap data
                            tileIndexY = (self.tilemapData[tilemapOffset][(tileIndex * 8) + (tilePiece * 2)] & 0xF0) >> 4
                            tileIndexX = self.tilemapData[tilemapOffset][(tileIndex * 8) + (tilePiece * 2)] & 0x0F
                            
                            # read the property of the current tile from the tilemap data
                            tileProperty = self.tilemapData[tilemapOffset][(tileIndex * 8) + (tilePiece * 2) + 1]
                            
                            # read the palette offset from the tilemap data
                            paletteOffset = (tileProperty & 0x1C) >> 2
                            
                            # check the tileset offset
                            if (tileProperty & 0x01) != 0:
                                if len(self.tilesetBits) > 1:
                                    tilesetReadIndex = 1
                            else:
                                if ((self.tilesetIndexBG2 >= 0) and (layer > 0) and
                                    (self.getTilesetAddressDecomp(Model_MapDataTileset.LAYER_BG1) != self.getTilesetAddressDecomp(Model_MapDataTileset.LAYER_BG2)) and
                                    (self.mapDataTilemap[0].address != self.mapDataTilemap[1].address)):
                                    tilesetReadIndex = 1

                            # loop for the 8 rows of a tile
                            for tileRow in range (8):
                                # loop for the 8 pixels of a tile's row
                                for tilePixel in range (8):
                                    pixelBit = []

                                    # loop for the 4 bits of a single pixel
                                    for tilePixelBit in range (4):
                                        bPixelBit = False

                                        # read the current tile pixel bit
                                        if tilePixelBit == 0:
                                            bPixelBit = self.tilesetBits[tilesetReadIndex][(tileIndexY * 4096) + (tileIndexX * 256) + (tileRow * 16) + tilePixel]
                                        if tilePixelBit == 1:
                                            bPixelBit = self.tilesetBits[tilesetReadIndex][(tileIndexY * 4096) + (tileIndexX * 256) + (tileRow * 16) + 8 + tilePixel]
                                        if tilePixelBit == 2:
                                            bPixelBit = self.tilesetBits[tilesetReadIndex][(tileIndexY * 4096) + (tileIndexX * 256) + (tileRow * 16) + (16 * 8) + tilePixel]
                                        if tilePixelBit == 3:
                                            bPixelBit = self.tilesetBits[tilesetReadIndex][(tileIndexY * 4096) + (tileIndexX * 256) + (tileRow * 16) + (17 * 8) + tilePixel]

                                        # set the pixel bit in the pixel bit array that containt all 4 pixel bits
                                        if bPixelBit == 1:
                                            pixelBit.append(1)
                                        else:
                                            pixelBit.append(0)
                                    
                                    # write the pixel value from the pixel bits
                                    pixelValue = ((pixelBit[0] << 3) | (pixelBit[1] << 2) | (pixelBit[2] << 1) | pixelBit[3])
                                    
                                    # continue if the pixel belongs to the background
                                    if pixelValue == 0:
                                        continue

                                    # add the palette offset to the pixel value
                                    if (paletteOffset > 0) and (pixelValue != 0):
                                        pixelValue += ((paletteOffset - 1) * 16)

                                    # mirror tile in x direction if the mirror x bit is set
                                    if ((tileProperty & 0x80) != 0):
                                        tileRow = 7 - tileRow
                                    
                                    # mirror tile in y direction if the mirror y bit is set
                                    if (tileProperty & 0x40) != 0:
                                        tilePixel = 7 - tilePixel
                                    
                                    if tilePiece== 0:
                                        self.pixelValues[((int(float(mapSizeX / 16))) * 256 * ((256 * blockY) + (16 * tileY) + tileRow)) + (256 * blockX) + (16 * tileX) + tilePixel] = pixelValue
                                    if tilePiece== 1:
                                        self.pixelValues[((int(float(mapSizeX / 16))) * 256 * ((256 * blockY) + (16 * tileY) + tileRow)) + (256 * blockX) + (16 * tileX) + tilePixel + 8] = pixelValue
                                    if tilePiece== 2:
                                        self.pixelValues[((int(float(mapSizeX / 16))) * 256 * ((256 * blockY) + (16 * tileY) + tileRow + 8)) + (256 * blockX) + (16 * tileX) + tilePixel] = pixelValue
                                    if tilePiece== 3:
                                        self.pixelValues[((int(float(mapSizeX / 16))) * 256 * ((256 * blockY) + (16 * tileY) + tileRow + 8)) + (256 * blockX) + (16 * tileX) + tilePixel + 8] = pixelValue

                                    if (tileProperty & 0x80) != 0:
                                        tileRow = 7 - tileRow

                                    if (tileProperty & 0x40) != 0:
                                        tilePixel = 7 - tilePixel
                        tilePos += 1
    
    def updateArrangement(self, positionX, positionY, tileIndex, layer):
        # read the arrangement index for the current map layer
        arrangementDataIndex = self.getArrangementDataIndexOfLayer(layer)
        
        # calculate the tile position in the arrangement data
        tilePosition = (int(float(positionY / 16)) * int(float(self.mapDataArrangement[arrangementDataIndex].sizeX / 16))) + int(float(positionX / 16))
        self.mapDataArrangement[arrangementDataIndex].data[tilePosition] = tileIndex

        # read the tilemap index for the current map layer
        tilemapOffset = self.getTilemapIndexOfLayer(layer)
        
        # loop through the 4 map tile pieces
        for tilePiece in range (4):
            tilesetReadIndex = 0 # TODO layer

            # read the x and y index of the current tile from the tilemap data
            tileIndexY = (self.tilemapData[tilemapOffset][(tileIndex * 8) + (tilePiece * 2)] & 0xF0) >> 4
            tileIndexX = self.tilemapData[tilemapOffset][(tileIndex * 8) + (tilePiece * 2)] & 0x0F
                            
            # read the property of the current tile from the tilemap data
            tileProperty = self.tilemapData[tilemapOffset][(tileIndex * 8) + (tilePiece * 2) + 1]
            
            # read the palette offset from the tilemap data
            paletteOffset = (tileProperty & 0x1C) >> 2
                            
            # check the tileset offset
            if (tileProperty & 0x01) != 0:
                if len(self.tilesetBits) > 1:
                    tilesetReadIndex = 1
            else:
                if ((self.tilesetIndexBG2 >= 0) and (layer > 0) and
                    (self.getTilesetAddressDecomp(Model_MapDataTileset.LAYER_BG1) != self.getTilesetAddressDecomp(Model_MapDataTileset.LAYER_BG2)) and
                    (self.mapDataTilemap[0].address != self.mapDataTilemap[1].address)):
                    tilesetReadIndex = 1

            # loop for the 8 rows of a tile
            for tileRow in range (8):
                # loop for the 8 pixels of a tile's row
                for tilePixel in range (8):
                    pixelBit = []

                    # loop for the 4 bits of a single pixel
                    for tilePixelBit in range (4):
                        bPixelBit = False

                        # read the current tile pixel bit
                        if tilePixelBit == 0:
                            bPixelBit = self.tilesetBits[tilesetReadIndex][(tileIndexY * 4096) + (tileIndexX * 256) + (tileRow * 16) + tilePixel]
                        if tilePixelBit == 1:
                            bPixelBit = self.tilesetBits[tilesetReadIndex][(tileIndexY * 4096) + (tileIndexX * 256) + (tileRow * 16) + 8 + tilePixel]
                        if tilePixelBit == 2:
                            bPixelBit = self.tilesetBits[tilesetReadIndex][(tileIndexY * 4096) + (tileIndexX * 256) + (tileRow * 16) + (16 * 8) + tilePixel]
                        if tilePixelBit == 3:
                            bPixelBit = self.tilesetBits[tilesetReadIndex][(tileIndexY * 4096) + (tileIndexX * 256) + (tileRow * 16) + (17 * 8) + tilePixel]

                        # set the pixel bit in the pixel bit array that containt all 4 pixel bits
                        if bPixelBit == 1:
                            pixelBit.append(1)
                        else:
                            pixelBit.append(0)
                                    
                    # write the pixel value from the pixel bits
                    pixelValue = ((pixelBit[0] << 3) | (pixelBit[1] << 2) | (pixelBit[2] << 1) | pixelBit[3])
                        
                    # continue if the pixel belongs to the background
                    if pixelValue == 0:
                        continue

                    # add the palette offset to the pixel value
                    if (paletteOffset > 0) and (pixelValue != 0):
                        pixelValue += ((paletteOffset - 1) * 16)

                    # mirror tile in x direction if the mirror x bit is set
                    if ((tileProperty & 0x80) != 0):
                        tileRow = 7 - tileRow
                    
                    # mirror tile in y direction if the mirror y bit is set
                    if (tileProperty & 0x40) != 0:
                        tilePixel = 7 - tilePixel
                                
                    if tilePiece== 0:
                        pixelIndex = ((int(float(self.sizeX / 16))) * 256 * ((16 * positionY) + tileRow)) + (16 * positionX) + tilePixel
                    if tilePiece== 1:
                        pixelIndex = ((int(float(self.sizeX / 16))) * 256 * ((16 * positionY) + tileRow)) + (16 * positionX) + tilePixel + 8
                    if tilePiece== 2:
                        pixelIndex = ((int(float(self.sizeX / 16))) * 256 * ((16 * positionY) + tileRow + 8)) + (16 * positionX) + tilePixel
                    if tilePiece== 3:
                        pixelIndex = ((int(float(self.sizeX / 16))) * 256 * ((16 * positionY) + tileRow + 8)) + (16 * positionX) + tilePixel + 8

                    self.pixelValues[pixelIndex] = pixelValue

                    if (tileProperty & 0x80) != 0:
                        tileRow = 7 - tileRow

                    if (tileProperty & 0x40) != 0:
                        tilePixel = 7 - tilePixel
    
                    # create an RGB pixel array with the selected palette and the readout palette color index
                    imageBytesIndex = pixelIndex * 3

                    paletteIndex = int(float(pixelValue / 16))
                    colorIndex = (pixelValue % 16)
                    palette = self.palettesetMap.palettes[paletteIndex]
                    self.imageBytes[imageBytesIndex + 0] = palette.data[((colorIndex * 3) + 0)]   # red
                    self.imageBytes[imageBytesIndex + 1] = palette.data[((colorIndex * 3) + 1)]   # green
                    self.imageBytes[imageBytesIndex + 2] = palette.data[((colorIndex * 3) + 2)]   # blue

        # create an image from the RGB pixel array
        self.mapImage = PIL.Image.frombytes('RGB', (self.pixelWidth, self.pixelHeight), bytes(self.imageBytes), 'raw')

    def getTilemapIndexOfLayer(self, layer):
        tilemapOffset = 0
        for index in range (len(self.mapDataTilemap)):
            mapDataTilemap : Model_MapDataTilemap = self.mapDataTilemap[index]
            if mapDataTilemap.slotId == 3:
                tilemapOffset = 0
                break
            else:
                if (((layer == 0) and (mapDataTilemap.slotId == 1)) or
                    ((layer == 1) and (mapDataTilemap.slotId == 2))):
                    tilemapOffset = index
                    break
        return tilemapOffset

    def getArrangementDataIndexOfLayer(self, layer):
        arrangementDataIndex = 0
        for index in range(len(self.mapDataArrangement)):
            mapDataArrangement : Model_MapDataArrangement = self.mapDataArrangement[index]
            if (((layer == 0) and (mapDataArrangement.slotId == 1)) or
                ((layer == 1) and (mapDataArrangement.slotId == 2))):
                arrangementDataIndex = index
                break
        return arrangementDataIndex
    
    def createImageOverlay(self, currentPositionX, currentPositionY, tabIndex):
        if (tabIndex == 1):
            # get the array containing the event image bytes
            imageBytes = self.eventImageBytes.copy()
        elif (tabIndex == 2):
            # get the array containing the exit image bytes
            imageBytes = self.exitImageBytes.copy()
        else:
            # get the array containing the image bytes
            imageBytes = self.imageBytes.copy()

        frameHeight = Model_Tilemap.TILEMAP_TILE_PIXEL_HEIGHT
        frameWidth = Model_Tilemap.TILEMAP_TILE_PIXEL_WIDTH

        # set the frame on the current mouse position
        pixelIndex = (self.pixelWidth * 3 * currentPositionY * frameHeight) + frameWidth * 3 * currentPositionX
        for height in range (frameHeight):
            for width in range (frameWidth):
                if ((height == 0) or
                    (height == (frameHeight - 1)) or
                    (width == 0) or
                    (width == (frameWidth - 1))):
                    pixelOffsetX = 3 * width
                    pixelOffsetY = self.pixelWidth * 3 * height
                    imageBytes[pixelIndex + pixelOffsetX + pixelOffsetY + 0] = 0xFF
                    imageBytes[pixelIndex + pixelOffsetX + pixelOffsetY + 1] = 0xFF
                    imageBytes[pixelIndex + pixelOffsetX + pixelOffsetY + 2] = 0xFF
        
        # create an image from the RGB pixel array
        self.mapImage = PIL.Image.frombytes('RGB', (self.pixelWidth, self.pixelHeight), bytes(imageBytes), 'raw')
    
    def getTilesetAddressDecomp(self, layer):
        addressDecomp = -1

        for tilesetIndex in range (len(self.mapDataTileset)):
            tileset : Model_MapDataTileset = self.mapDataTileset[tilesetIndex]
            if (tileset.layer == layer):
                addressDecomp = tileset.addressDecomp
                break

        return addressDecomp
    
    def getPaletteIndex(self, layer):
        index = -1

        for paletteIndex in range (len(self.mapDataPalette)):
            palette : Model_MapDataPalette = self.mapDataPalette[paletteIndex]
            if (((layer == Model_MapDataPalette.MAP_LAYER) and (palette.layer == Model_MapDataPalette.MAP_LAYER)) or
                ((layer == Model_MapDataPalette.SPRITE_LAYER) and (palette.layer == Model_MapDataPalette.SPRITE_LAYER))):
                index = paletteIndex
                break

        return index
    
    def getTilesetIndex(self, layer):
        index = -1
        decompOffset = 0

        for tilesetIndex in range (len(self.mapDataTileset)):
            tileset : Model_MapDataTileset = self.mapDataTileset[tilesetIndex]
            if ((layer != Model_MapDataTileset.LAYER_SPRITES) and
                (tileset.layer == Model_MapDataTileset.LAYER_BG1_BG2)):
                if (layer == Model_MapDataTileset.LAYER_BG1):
                    index = tilesetIndex
                elif (layer == Model_MapDataTileset.LAYER_BG2):
                    index = tilesetIndex
                    decompOffset = 0x2000
                break
            elif (tileset.layer == layer):
                index = tilesetIndex
                break

        return index, decompOffset
    