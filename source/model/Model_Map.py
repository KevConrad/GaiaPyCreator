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
from model.Model_Spritesets import Model_Spritesets
from model.Model_Tilemaps import Model_Tilemaps
from model.Model_Tilemap import Model_Tilemap
from model.Model_Tilesets import Model_Tilesets
from model.Model_Tileset import Model_Tileset
from model.Model_Treasures import Model_Treasures

import bitstring

import PIL

class Model_Map:
    BYTES_PER_PIXEL = 4 # RGBA

    def __init__(self, romData, mapData : dict, projectData : dict, mapDataTableEntry : Model_MapData,
                 mapIndex, screenSettings : Model_ScreenSettings, roomClearingRewards : Model_RoomClearingRewards,
                 spritesets:Model_Spritesets) -> None:
        self.romData = romData
        self.spritesets = spritesets

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
            self.screenSettings = screenSettings.screenSettings[self.mapDataScreenSettings[0].index - 1]
        
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

        # read the map treasure data
        treasureDataTableAddress = int(str(projectData['DataTables']['TreasureChestTable']['Address']), 16)
        treasureDataTableSize = int(projectData['DataTables']['TreasureChestTable']['Size'], base=16)
        treasureDataTable = Model_RomDataTable(self.romData, treasureDataTableAddress, treasureDataTableSize)
        self.treasures = Model_Treasures(self.romData, treasureDataTable.getDataAddress(mapIndex))

    def read(self, tilemaps: Model_Tilemaps, tilesets: Model_Tilesets):
        if len(self.mapDataArrangement) > 0:
            self.mapDataArrangement[0].read()
        if len(self.mapDataArrangement) > 1:
            self.mapDataArrangement[1].read()
            
        self.tilemapData = []
        if len(self.mapDataTilemap) > 0:
            tilemapIndex = self.mapDataTilemap[0].index
            self.tilemapData.append(tilemaps[tilemapIndex].read())
        if len(self.mapDataTilemap) > 1:
            tilemapIndex = self.mapDataTilemap[1].index
            self.tilemapData.append(tilemaps[tilemapIndex].read())

        # get tileset indices for BG1 and BG2 layers
        for tileset in self.mapDataTileset:
            if tileset.layer == Model_MapDataTileset.LAYER_BG1:
                self.tilesetIndexBG1 = tileset.index
            if tileset.layer == Model_MapDataTileset.LAYER_BG2:
                self.tilesetIndexBG2 = tileset.index

        # read BG1 layer tileset data
        if self.tilesetIndexBG1 >= 0:
            # decompress the compressed tileset data (increment length of compressed data to prevent data truncation)
            self.tilesetDataBG1, self.tilesetBG1CompSize = Model_Compression.decompress(self.romData, tilesets[self.tilesetIndexBG1].address,
                                                                                        tilesets[self.tilesetIndexBG1].decompOffset)
        # read BG2 layer tileset data
        if self.tilesetIndexBG2 >= 0:
            # decompress the compressed tileset data (increment length of compressed data to prevent data truncation)
            self.tilesetDataBG2, self.tilesetBG2CompSize = Model_Compression.decompress(self.romData, tilesets[self.tilesetIndexBG2].address,
                                                                                        tilesets[self.tilesetIndexBG2].decompOffset)
            
        # read sprite data
        self.spritesetIndex = self.spritesets.getIndexfromAddress(self.mapDataSprites[0].address)
        if self.spritesetIndex >= 0:
            self.spritesets.spritesets[self.spritesetIndex].read()
            self.spriteTilesetBits = self.spritesets.spritesets[self.spritesetIndex].tilesetBits

        # read map palette data
        paletteIndexMap = self.getPaletteIndex(Model_MapDataPalette.MAP_LAYER)
        if paletteIndexMap >= 0:
            self.palettesetMap = Model_Paletteset(self.romData, self.mapDataPalette[paletteIndexMap].address)

        # read sprites palette data
        paletteIndexMap = self.getPaletteIndex(Model_MapDataPalette.SPRITE_LAYER)
        if paletteIndexMap >= 0:
            self.palettesetSprites = Model_Paletteset(self.romData, self.mapDataPalette[paletteIndexMap].address)

        # read sprites data
        if len(self.mapDataSprites) > 0:
            # decompress the compressed sprites data (increment length of compressed data to prevent data truncation)
            pass
    
    def createImage(self, screenSettings):
        # read all tilesets that are used by the map
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

        # create map layer images
        self.imageLayers = []
        self.imageBytes = []
        # BG1 layer
        image, imageBytes = self.createLayerImage(0, False)
        self.imageLayers.append(image)
        self.imageBytes.append(imageBytes)

        # create BG2 layer if it exists
        if len(self.mapDataArrangement) > 1:
            image, imageBytes = self.createLayerImage(1, False)        
            self.imageLayers.append(image)
            self.imageBytes.append(imageBytes)
            self.hasBG2Layer = True
        else:
            self.hasBG2Layer = False

        # sprite layer
        image, imageBytes = self.createSpriteImage()
        self.imageLayers.append(image)
        self.imageBytes.append(imageBytes)

    def createEventImage(self, selectedEventIndex):
        # create the array containing the image bytes
        imageBytes = [0] * (self.pixelWidth * self.pixelHeight * self.BYTES_PER_PIXEL)

        # read the map events and write the event overlay to the bitmap pixel value array
        eventIndex = 0
        for event in self.events.events:
            if (event.positionX > self.sizeX) or (event.positionY > self.sizeY):
                continue
            # calculate the pixel index of the current event
            pixelIndex = (self.pixelWidth * self.BYTES_PER_PIXEL * event.positionY * Model_Tilemap.TILEMAP_TILE_PIXEL_HEIGHT) + Model_Tilemap.TILEMAP_TILE_PIXEL_WIDTH * self.BYTES_PER_PIXEL * event.positionX
            for height in range (Model_Tilemap.TILEMAP_TILE_PIXEL_HEIGHT):
                for width in range (Model_Tilemap.TILEMAP_TILE_PIXEL_WIDTH):
                    pixelOffsetX = self.BYTES_PER_PIXEL * width
                    pixelOffsetY = self.pixelWidth * self.BYTES_PER_PIXEL * height
                    # check if the event is selected
                    if eventIndex == selectedEventIndex:
                        if ((height == 0) or
                            (height == (Model_Tilemap.TILEMAP_TILE_PIXEL_HEIGHT - 1)) or
                            (width == 0) or
                            (width == (Model_Tilemap.TILEMAP_TILE_PIXEL_WIDTH - 1))):
                            imageBytes[pixelIndex + pixelOffsetX + pixelOffsetY + 0] = 0xFF
                            imageBytes[pixelIndex + pixelOffsetX + pixelOffsetY + 1] = 0xFF
                            imageBytes[pixelIndex + pixelOffsetX + pixelOffsetY + 2] = 0xFF
                        else:
                            imageBytes[pixelIndex + pixelOffsetX + pixelOffsetY + 0] = 0xFF
                    else:
                        imageBytes[pixelIndex + pixelOffsetX + pixelOffsetY + 0] = 0xFF
                    imageBytes[pixelIndex + pixelOffsetX + pixelOffsetY + 3] = 0xAA
            eventIndex += 1
        
        # create an image from the RGB pixel array
        self.eventImage = PIL.Image.frombytes('RGBA', (self.pixelWidth, self.pixelHeight), bytes(imageBytes), 'raw')

    def createExitImage(self, selectedExitIndex):
        # create the array containing the image bytes
        imageBytes = [0] * (self.pixelWidth * self.pixelHeight * self.BYTES_PER_PIXEL)

        # read the map exits and write the exit overlay to the bitmap pixel value array
        exitIndex = 0
        for exit in self.exits.exits:
            pixelIndex = (self.pixelWidth * self.BYTES_PER_PIXEL * exit.positionY * Model_Tilemap.TILEMAP_TILE_PIXEL_HEIGHT) + Model_Tilemap.TILEMAP_TILE_PIXEL_WIDTH * self.BYTES_PER_PIXEL * exit.positionX
            for exitSizeY in range (exit.height):
                for exitSizeX in range (exit.width):
                    for height in range (Model_Tilemap.TILEMAP_TILE_PIXEL_HEIGHT):
                        for width in range (Model_Tilemap.TILEMAP_TILE_PIXEL_WIDTH):
                            pixelOffsetX = self.BYTES_PER_PIXEL * ((exitSizeX * Model_Tilemap.TILEMAP_TILE_PIXEL_WIDTH) + width)
                            pixelOffsetY = self.pixelWidth * self.BYTES_PER_PIXEL * (height + (Model_Tilemap.TILEMAP_TILE_PIXEL_HEIGHT * exitSizeY))
                            if exitIndex == selectedExitIndex:
                                if (((height == 0) and (exitSizeY == 0)) or
                                    ((height == (Model_Tilemap.TILEMAP_TILE_PIXEL_HEIGHT - 1)) and (exitSizeY == (exit.height - 1))) or
                                    ((width == 0) and (exitSizeX == 0)) or
                                    ((width == (Model_Tilemap.TILEMAP_TILE_PIXEL_WIDTH - 1) and (exitSizeX == (exit.width - 1))))):
                                    imageBytes[pixelIndex + pixelOffsetX + pixelOffsetY + 0] = 0xFF
                                    imageBytes[pixelIndex + pixelOffsetX + pixelOffsetY + 1] = 0xFF
                                    imageBytes[pixelIndex + pixelOffsetX + pixelOffsetY + 2] = 0xFF
                                else:
                                    imageBytes[pixelIndex + pixelOffsetX + pixelOffsetY + 2] = 0xFF
                            else:
                                imageBytes[pixelIndex + pixelOffsetX + pixelOffsetY + 2] = 0xFF
                            imageBytes[pixelIndex + pixelOffsetX + pixelOffsetY + 3] = 0xAA
            exitIndex += 1
        
        # create an image from the RGB pixel array
        self.exitImage = PIL.Image.frombytes('RGBA', (self.pixelWidth, self.pixelHeight), bytes(imageBytes), 'raw')

    def createSpriteImage(self):
        # create the array containing the image bytes
        imageBytes = [0] * (self.pixelWidth * self.pixelHeight * self.BYTES_PER_PIXEL)

        # read the map events and write the sprite data to the bitmap pixel value array
        for event in self.events.events:
            if (event.positionX > self.sizeX) or (event.positionY > self.sizeY):
                continue
            # calculate the pixel index of the current event
            positionY = event.positionY
            if (event.positionY > 0):
                positionY = event.positionY - 1
            pixelIndex = (self.pixelWidth * self.BYTES_PER_PIXEL * positionY * Model_Tilemap.TILEMAP_TILE_PIXEL_HEIGHT) + Model_Tilemap.TILEMAP_TILE_PIXEL_WIDTH * self.BYTES_PER_PIXEL * event.positionX
            spriteIndex = self.romData[event.address]
            frameIndex = self.spritesets.spritesets[self.spritesetIndex].sprites[spriteIndex].frameData[0].frameId
            self.spritesets.spritesets[self.spritesetIndex].spriteFrames[frameIndex].createImageExternal(self.pixelWidth, self.spriteTilesetBits, 0, imageBytes, pixelIndex)

        # create an image from the RGB pixel array
        image = PIL.Image.frombytes('RGBA', (self.pixelWidth, self.pixelHeight), bytes(imageBytes), 'raw')
        return image, imageBytes
    
    def createLayerImage(self, layer, isTransparent):
        tilePos = 0
        
        # read the arrangement index for the current map layer
        arrangementDataIndex = self.getArrangementDataIndexOfLayer(layer)
        arrangementData = self.mapDataArrangement[arrangementDataIndex].data

        paletteData = self.palettesetMap.palettes
        # read the tilemap index for the current map layer
        tilemapOffset = self.getTilemapIndexOfLayer(layer)
        tilemapData = self.tilemapData[tilemapOffset]

        imageBytes = [0] * (self.pixelWidth * self.pixelHeight * self.BYTES_PER_PIXEL)

        mapSizePixelValueIndex = int(float(self.sizeX / 16)) * 256
        mapBlockCount = int(float(self.mapDataArrangement[layer].sizeY / 16))
        mapBlockRowCount = int(float(self.mapDataArrangement[layer].sizeX / 16))
        # loop through all map block rows (offset = 65536)
        for blockY in range(mapBlockCount):
            blockYPixelValueIndex = 256 * blockY
            # loop through all map blocks of a map block row (offset = 256)
            for blockX in range (mapBlockRowCount):
                blockXPixelValueIndex = 256 * blockX
                # loop through the 16 map tile rows of a map block (offset = 256)
                for tileY in range (16):
                    tileYPixelValueIndex = (16 * tileY) + blockYPixelValueIndex
                    # loop through the 16 map tiles of a map tile row
                    for tileX in range (16):
                        tileXPixelValueIndex = (16 * tileX) + blockXPixelValueIndex
                        # read the index of the current tile from the arrangement data
                        tileIndex = arrangementData[tilePos]
                        tileArrayIndex = tileIndex * 8

                        # loop through the 4 map tile pieces
                        for tilePiece in range (4):
                            tilesetReadIndex = 0 # TODO layer

                            # read the x and y index of the current tile from the tilemap data
                            tileIndexY = (tilemapData[tileArrayIndex + (tilePiece * 2)] & 0xF0) >> 4
                            tileIndexX = tilemapData[tileArrayIndex + (tilePiece * 2)] & 0x0F
                            tilesetBitsArrayIndex = (tileIndexY * 4096) + (tileIndexX * 256)
                            
                            # read the property of the current tile from the tilemap data
                            tileProperty = tilemapData[tileArrayIndex + (tilePiece * 2) + 1]
                            
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
                                tileRowPixelValueIndex_0_1 = mapSizePixelValueIndex * (tileYPixelValueIndex + tileRow) + tileXPixelValueIndex
                                tileRowPixelValueIndex_2_3 = mapSizePixelValueIndex * (tileYPixelValueIndex + tileRow + 8) + tileXPixelValueIndex
                                tileRowIndex = tilesetBitsArrayIndex + (tileRow * 16)
                                # loop for the 8 pixels of a tile's row
                                for tilePixel in range (8):
                                    pixelValue = 0
                                    # loop for the 4 bits of a single pixel
                                    for tilePixelBit in range (4):
                                        # read the current tile pixel bit
                                        if tilePixelBit == 0:
                                            pixelValue += self.tilesetBits[tilesetReadIndex][tileRowIndex + tilePixel] << 3
                                        elif tilePixelBit == 1:
                                            pixelValue += self.tilesetBits[tilesetReadIndex][tileRowIndex + 8 + tilePixel] << 2
                                        elif tilePixelBit == 2:
                                            pixelValue += self.tilesetBits[tilesetReadIndex][tileRowIndex + 128 + tilePixel] << 1
                                        else: # tilePixelBit is 3
                                            pixelValue += self.tilesetBits[tilesetReadIndex][tileRowIndex + 136 + tilePixel]
                                    
                                    # continue if the pixel belongs to the background
                                    if pixelValue == 0:
                                        continue

                                    # add the palette offset to the pixel value
                                    if paletteOffset > 0:
                                        pixelValue += ((paletteOffset - 1) * 16)

                                    # mirror tile in x direction if the mirror x bit is set
                                    if ((tileProperty & 0x80) != 0):
                                        tileRow = 7 - tileRow
                                    
                                    # mirror tile in y direction if the mirror y bit is set
                                    if (tileProperty & 0x40) != 0:
                                        tilePixel = 7 - tilePixel
                                    
                                    if tilePiece == 0:
                                        imageBytesIndex = (tileRowPixelValueIndex_0_1 + tilePixel) * self.BYTES_PER_PIXEL
                                    elif tilePiece == 1:
                                        imageBytesIndex = (tileRowPixelValueIndex_0_1 + tilePixel + 8) * self.BYTES_PER_PIXEL
                                    elif tilePiece == 2:
                                        imageBytesIndex = (tileRowPixelValueIndex_2_3 + tilePixel) * self.BYTES_PER_PIXEL
                                    else:       # tilePiece is 3
                                        imageBytesIndex = (tileRowPixelValueIndex_2_3 + tilePixel + 8) * self.BYTES_PER_PIXEL

                                    # update the RGB pixel array with the selected palette and the readout palette color index
                                    paletteIndex = int(pixelValue / 16)
                                    colorIndex = (pixelValue % 16) * 3
                                    palette = paletteData[paletteIndex]
                                    imageBytes[imageBytesIndex:imageBytesIndex + 3] = palette.data[colorIndex:colorIndex + 3]  # red, green, blue
                                    if pixelValue == 0:
                                        imageBytes[imageBytesIndex + 3] = 0                          # alpha (transparent)
                                    else:
                                        if isTransparent is True:
                                            imageBytes[imageBytesIndex + 3] = 128
                                        else:
                                            imageBytes[imageBytesIndex + 3] = 255                    # alpha (non-transparent)

                                    if (tileProperty & 0x80) != 0:
                                        tileRow = 7 - tileRow

                                    if (tileProperty & 0x40) != 0:
                                        tilePixel = 7 - tilePixel
                        tilePos += 1
        # create an image from the RGB pixel array
        image = PIL.Image.frombytes('RGBA', (self.pixelWidth, self.pixelHeight), bytes(imageBytes), 'raw')
        return image, imageBytes
    
    def updateArrangement(self, positionX, positionY, tileIndex, layer, imageBytes):
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

                    if (tileProperty & 0x80) != 0:
                        tileRow = 7 - tileRow

                    if (tileProperty & 0x40) != 0:
                        tilePixel = 7 - tilePixel
    
                    # create an RGB pixel array with the selected palette and the readout palette color index
                    imageBytesIndex = pixelIndex * self.BYTES_PER_PIXEL

                    paletteIndex = int(float(pixelValue / 16))
                    colorIndex = (pixelValue % 16)
                    palette = self.palettesetMap.palettes[paletteIndex]
                    imageBytes[imageBytesIndex + 0] = palette.data[((colorIndex * 3) + 0)]   # red
                    imageBytes[imageBytesIndex + 1] = palette.data[((colorIndex * 3) + 1)]   # green
                    imageBytes[imageBytesIndex + 2] = palette.data[((colorIndex * 3) + 2)]   # blue
                    if pixelValue == 0:
                        imageBytes[imageBytesIndex + 3] = 0                      # alpha (transparent)
                    else:
                        imageBytes[imageBytesIndex + 3] = 255                    # alpha (non-transparent)

        # create an image from the RGB pixel array
        self.imageLayers[layer] = PIL.Image.frombytes('RGBA', (self.pixelWidth, self.pixelHeight), bytes(imageBytes), 'raw')

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
    