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
from model.Model_MapExits import Model_MapExits
from model.Model_Palette import Model_Palette
from model.Model_Paletteset import Model_Paletteset
from model.Model_RomDataTable import Model_RomDataTable
from model.Model_Tilemap import Model_Tilemap
from model.Model_Tileset import Model_Tileset

import bitstring

import PIL

class Model_Map:
    def __init__(self, romData, mapData : dict, projectData : dict, mapDataTableEntry : Model_MapData, mapIndex) -> None:
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

        # TODO read the map event data

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
    
    def getImage(self, isBG1LayerDisplayed, isBG2LayerDisplayed, isSpriteLayerDisplayed, screenSettings):          
        # read all tilesets that are used by the map

        # array which contains the data of both tilesets used by the map
        tilesetGraphicBits = []

        if self.tilesetIndexBG1 >= 0:
            tilesetGraphicBits.append(bitstring.ConstBitStream(bytes = self.tilesetDataBG1, offset=0,
                                                               length=Model_Tileset.TILESET_BYTE_SIZE * 8))
        
        if self.tilesetIndexBG2 >= 0:
            tilesetGraphicBits.append(bitstring.ConstBitStream(bytes = self.tilesetDataBG2, offset=0,
                                                               length=Model_Tileset.TILESET_BYTE_SIZE * 8))

        # read the map layers
        pixelWidth = self.sizeX * Model_Tilemap.TILEMAP_TILE_PIXEL_WIDTH
        pixelHeight = self.sizeY * Model_Tilemap.TILEMAP_TILE_PIXEL_HEIGHT
        pixelValues = [0] * (pixelWidth * pixelHeight)
        imageBytes = [0] * (pixelWidth * pixelHeight * 3)

        #mapLayerOrder = screenSettings.getMapLayerOrderBits();
        #if ((mapLayerOrder.mapLayerOrder.hasNormalMapLayers == false) and (data.GetDataCount(MapDataTableEntry.EDataset.arrangementData) > 1)) //TODO: Query of arrangementCount > 1 should not be necessary!
            #if isBG2LayerDisplayed is True:
        print("Size X: " + str(self.sizeX))
        pixelValues = self.displayLayer(self.sizeX, tilesetGraphicBits, pixelValues, 0)
                #if isBG1LayerDisplayed is True:
                #    displayLayer(self.sizeX, tilesetGraphicBits, pixelValues, 0)              
            #else:
                #if isBG1LayerDisplayed is True:
                #    displayLayer(self.sizeX, tilesetGraphicBits, pixelValues, 0)
                #if (isBG2LayerDisplayed is True) and (data.GetDataCount(MapDataTableEntry.EDataset.arrangementData) > 1))
                #    displayLayer(self.sizeX, tilesetGraphicBits, pixelValues, 1)

        #if (isSpriteLayerDisplayed is True) and (data.getSpriteCount() > 0))
            # read the map overlay (events, exits, sprites) and write it to the bitmap pixel value array
            #displayOverlay(mapSizeX, mapSizeY, tilesetBits, pixelValues);

        # create an RGB pixel array with the selected palette and the readout palette color index
        pixelIndex = 0
        for pixelValue in pixelValues:
            paletteIndex = int(float(pixelValue / 16))
            colorIndex = (pixelValue % 16)
            palette = self.palettesetMap.palettes[paletteIndex]    # TODO check why -1 is needed here
            imageBytes[pixelIndex + 0] = palette.data[((colorIndex * 3) + 0)]   # red
            imageBytes[pixelIndex + 1] = palette.data[((colorIndex * 3) + 1)]   # green
            imageBytes[pixelIndex + 2] = palette.data[((colorIndex * 3) + 2)]   # blue
            pixelIndex = pixelIndex + 3

        # create an image from the RGB pixel array
        mapImage = PIL.Image.frombytes('RGB', (pixelWidth, pixelHeight), bytes(imageBytes), 'raw')
        return mapImage


    def displayLayer(self, mapSizeX, tilesetBits, pixelValues, layer):
        tilePos = 0
        
        # read the arrangement index for the current map layer
        arrangementDataIndex = 0
        for index in range(len(self.mapDataArrangement)):
            mapDataArrangement : Model_MapDataArrangement = self.mapDataArrangement[index]
            if (((layer == 0) and (mapDataArrangement.slotId == 1)) or
                ((layer == 1) and (mapDataArrangement.slotId == 2))):
                arrangementDataIndex = index
                break
            
        # read the tilemap index for the current map layer
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
        
        # loop through all map block rows (offset = 65536)
        for blockY in range(int(float(self.mapDataArrangement[layer].sizeY / 16))):
            # loop through all map blocks of a map block row (offset = 256)
            for blockX in range (int(float(self.mapDataArrangement[layer].sizeY / 16))):
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
                                if len(tilesetBits) > 1:
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
                                            bPixelBit = tilesetBits[tilesetReadIndex][(tileIndexY * 4096) + (tileIndexX * 256) + (tileRow * 16) + tilePixel]
                                        if tilePixelBit == 1:
                                            bPixelBit = tilesetBits[tilesetReadIndex][(tileIndexY * 4096) + (tileIndexX * 256) + (tileRow * 16) + 8 + tilePixel]
                                        if tilePixelBit == 2:
                                            bPixelBit = tilesetBits[tilesetReadIndex][(tileIndexY * 4096) + (tileIndexX * 256) + (tileRow * 16) + (16 * 8) + tilePixel]
                                        if tilePixelBit == 3:
                                            bPixelBit = tilesetBits[tilesetReadIndex][(tileIndexY * 4096) + (tileIndexX * 256) + (tileRow * 16) + (17 * 8) + tilePixel]

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

                                    # ddd the palette offset to the pixel value
                                    if (paletteOffset > 0) and (pixelValue != 0):
                                        pixelValue += ((paletteOffset - 1) * 16)

                                    # mirror tile in x direction if the mirror x bit is set
                                    if ((tileProperty & 0x80) != 0):
                                        tileRow = 7 - tileRow
                                    
                                    # mirror tile in y direction if the mirror y bit is set
                                    if (tileProperty & 0x40) != 0:
                                        tilePixel = 7 - tilePixel
                                    
                                    if tilePiece== 0:
                                        pixelValues[((int(float(mapSizeX / 16))) * 256 * ((256 * blockY) + (16 * tileY) + tileRow)) + (256 * blockX) + (16 * tileX) + tilePixel] = pixelValue;
                                    if tilePiece== 1:
                                        pixelValues[((int(float(mapSizeX / 16))) * 256 * ((256 * blockY) + (16 * tileY) + tileRow)) + (256 * blockX) + (16 * tileX) + tilePixel + 8] = pixelValue;
                                    if tilePiece== 2:
                                        pixelValues[((int(float(mapSizeX / 16))) * 256 * ((256 * blockY) + (16 * tileY) + tileRow + 8)) + (256 * blockX) + (16 * tileX) + tilePixel] = pixelValue;
                                    if tilePiece== 3:
                                        pixelValues[((int(float(mapSizeX / 16))) * 256 * ((256 * blockY) + (16 * tileY) + tileRow + 8)) + (256 * blockX) + (16 * tileX) + tilePixel + 8] = pixelValue;

                                    if (tileProperty & 0x80) != 0:
                                        tileRow = 7 - tileRow

                                    if (tileProperty & 0x40) != 0:
                                        tilePixel = 7 - tilePixel
                        tilePos += 1
        return pixelValues
    
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
    