import PIL.Image
from model.Model_Compression import Model_Compression
from model.Model_Palette import Model_Palette
from model.Model_Paletteset import Model_Paletteset
from model.Model_Tileset import Model_Tileset

import bitstring

import PIL

class Model_Tilemap:
    TILEMAP_TILE_HEIGHT = 16                # number of tiles in vertical direction
    TILEMAP_TILE_WIDTH = 16                 # number of tiles in horizontal direction
    TILEMAP_TILE_PIECE_HEIGHT = 2           # number of tile pieces in vertical direction
    TILEMAP_TILE_PIECE_WIDTH = 2            # number of tile pieces in horizontal direction
    TILEMAP_TILE_PIECE_PIXEL_HEIGHT = 8     # number of pixels in a tile piece in vertical direction
    TILEMAP_TILE_PIECE_PIXEL_WIDTH = 8      # number of pixels in a tile piece in horizontal direction
    TILEMAP_PIXEL_BIT_COUNT = 4             # number of bits for a single pixel

    # number of tile pieces in a tile
    TILEMAP_TILE_PIECE_COUNT = TILEMAP_TILE_PIECE_HEIGHT * TILEMAP_TILE_PIECE_WIDTH

    # number of pixels in a tile in vertical direction
    TILEMAP_TILE_PIXEL_HEIGHT = TILEMAP_TILE_PIECE_PIXEL_HEIGHT * TILEMAP_TILE_PIECE_HEIGHT

    # number of pixels in a tile in horizontal direction
    TILEMAP_TILE_PIXEL_WIDTH = TILEMAP_TILE_PIECE_PIXEL_WIDTH * TILEMAP_TILE_PIECE_WIDTH
    
    # number of pixels in a tilemap in vertical direction
    TILEMAP_PIXEL_HEIGHT = TILEMAP_TILE_HEIGHT * TILEMAP_TILE_PIXEL_HEIGHT

    # number of pixels in a tilemap in horizontal direction
    TILEMAP_PIXEL_WIDTH = TILEMAP_TILE_WIDTH * TILEMAP_TILE_PIXEL_WIDTH

    def __init__(self, romData, tilemapData : dict, tilesetsData : dict) -> None:
        self.romData = romData

        # read the data from the JSON file
        self.name = str(tilemapData['Name'])
        self.address = int(str(tilemapData['Address']), 16)
        self.palettesetAddress = int(str(tilemapData['Palette']), 16)
        self.firstTilesetId = int(str(tilemapData['Tileset1']), 10)
        self.secondTilesetId = int(str(tilemapData['Tileset2']), 10)

        tilesetAddressData = []
        for tilesetData in tilesetsData:
            tilesetAddressData.append(int(str(tilesetData['Address']), 16))

        for tilesetData in tilesetsData:
            tilesetAddress = int(str(tilesetData['Address']), 16)
            if tilesetAddress == tilesetAddressData[self.firstTilesetId]:
                self.firstTileset = Model_Tileset(self.romData, tilesetData)
            if tilesetAddress == tilesetAddressData[self.secondTilesetId]:
                self.secondTileset = Model_Tileset(self.romData, tilesetData)

    def read(self):
        # decompress the compressed tilemap data (increment length of compressed data to prevent data truncation)
        self.tilemapData, self.compSize = Model_Compression.decompress(self.romData, self.address, 10000, 0)

        # decompress the compressed tileset data (increment length of compressed data to prevent data truncation)
        self.firstTilesetData, self.firstTilesetCompSize = Model_Compression.decompress(self.romData, self.firstTileset.address,
                                                                                        self.firstTileset.compSize + 1,
                                                                                        self.firstTileset.decompOffset)
        self.secondTilesetData, self.secondTilesetCompSize = Model_Compression.decompress(self.romData, self.firstTileset.address,
                                                                                          self.firstTileset.compSize + 1,
                                                                                          self.firstTileset.decompOffset)
        self.paletteset = Model_Paletteset(self.romData, self.palettesetAddress)
        
    def getImage(self, readOffset, tilesetReadOffset, tileOffset, tilePieceOffset, readAll):
        # array which contains the data of both tilesets used by the tilemap
        tilesetGraphicBits = []

        # limit the length
        length = self.firstTileset.decompSize
        if length == (Model_Tileset.TILESET_BYTE_SIZE * 2):
            length = Model_Tileset.TILESET_BYTE_SIZE
        
        tilesetGraphicBits.append(bitstring.ConstBitStream(bytes = self.firstTilesetData, offset=(readOffset * 8), length=(length * 8)))
        
        length = self.secondTileset.decompSize
        if length == (Model_Tileset.TILESET_BYTE_SIZE * 2):
            length = Model_Tileset.TILESET_BYTE_SIZE
        
        tilesetGraphicBits.append(bitstring.ConstBitStream(bytes = self.secondTilesetData, offset=(readOffset * 8), length=(length * 8)))
        
        if readAll == True:
            pixelHeight = self.TILEMAP_PIXEL_HEIGHT
            pixelWidth = self.TILEMAP_PIXEL_WIDTH
        else:
            pixelHeight =  self.TILEMAP_TILE_PIXEL_HEIGHT
            pixelWidth = self.TILEMAP_TILE_PIXEL_WIDTH

        pixelValues = [0] * (pixelWidth * pixelHeight)
        imageBytes = [0] * ((pixelWidth * pixelHeight) * 3)
        
        tileIndex = 0
        # loop for the 16 map tile rows of a map block (offset = 256)
        for tileY in range (self.TILEMAP_TILE_WIDTH):
            # loop for the 16 map tiles of a map tile row
            for tileX in range (self.TILEMAP_TILE_HEIGHT):
                if (readAll == False):
                    tileIndex = tileOffset

                for tilePiece in range (self.TILEMAP_TILE_PIECE_COUNT):                     
                    tileIndexY = (self.tilemapData[(tileIndex * 8) + (tilePiece * 2)] & 0xF0) >> 4
                    tileIndexX = self.tilemapData[(tileIndex * 8) + (tilePiece * 2)] & 0x0F
                    tileProperty = self.tilemapData[(tileIndex * 8) + (tilePiece * 2) + 1]
                    paletteIndex = (tileProperty & 0x1C) >> 2
                    tilesetReadIndex = 0
                    tilesetOffset = 0
                        
                    # check the tileset offset
                    if ((tilesetReadOffset == 1) and
                        (self.firstTileset.address != self.secondTileset.address)):
                            tilesetReadIndex = 1
                    else:
                        if ((tileProperty & 0x01) != 0):        
                            if (self.secondTilesetId != 0):
                                tilesetReadIndex = 1
                        
                    # loop for the 8 rows of a tile
                    for tileRow in range (self.TILEMAP_TILE_PIECE_PIXEL_WIDTH):                          
                        # loop for the 8 pixels of a tile's row
                        for tilePixel in range (self.TILEMAP_TILE_PIECE_PIXEL_HEIGHT):
                            pixelBit = []

                            # loop for the 4 bits of a single pixel
                            for tilePixelBit in range (self.TILEMAP_PIXEL_BIT_COUNT):
                                isBitSet = False                                    

                                if tilePixelBit == 0:
                                    isBitSet = tilesetGraphicBits[tilesetReadIndex][tilesetOffset + (tileIndexY * 4096) + (tileIndexX * 256) + (tileRow * 16) + tilePixel]
                                if tilePixelBit == 1:
                                    isBitSet = tilesetGraphicBits[tilesetReadIndex][tilesetOffset + (tileIndexY * 4096) + (tileIndexX * 256) + (tileRow * 16) + 8 + tilePixel]
                                if tilePixelBit == 2:
                                    isBitSet = tilesetGraphicBits[tilesetReadIndex][tilesetOffset + (tileIndexY * 4096) + (tileIndexX * 256) + (tileRow * 16) + (16 * 8) + tilePixel]
                                if tilePixelBit == 3:
                                    isBitSet = tilesetGraphicBits[tilesetReadIndex][tilesetOffset + (tileIndexY * 4096) + (tileIndexX * 256) + (tileRow * 16) + (17 * 8) + tilePixel]

                                if isBitSet == 1:
                                    pixelBit.append(1)
                                else:
                                    pixelBit.append(0)

                            pixelValue = ((pixelBit[0] << 3) | (pixelBit[1] << 2) | (pixelBit[2] << 1) | pixelBit[3])

                            if paletteIndex > 0:
                                pixelValue += ((paletteIndex) * 16)

                            if pixelValue == 0:
                                continue

                            if (tileProperty & 0x80) != 0:     # mirror tile in x direction
                                tileRow = 7 - tileRow
                            if (tileProperty & 0x40) != 0:     # mirror tile in y direction
                                tilePixel = 7 - tilePixel

                            if tilePiece == 0:
                                pixelValues[(pixelWidth * ((16 * tileY) + tileRow)) + (16 * tileX) + tilePixel] = pixelValue
                            if tilePiece == 1:
                                pixelValues[(pixelWidth * ((16 * tileY) + tileRow)) + (16 * tileX) + tilePixel + 8] = pixelValue
                            if tilePiece== 2:
                                pixelValues[(pixelWidth * ((16 * tileY) + tileRow + 8)) + (16 * tileX) + tilePixel] = pixelValue
                            if tilePiece == 3:
                                pixelValues[(pixelWidth * ((16 * tileY) + tileRow + 8)) + (16 * tileX) + tilePixel + 8] = pixelValue
                            
                            if (tileProperty & 0x80) != 0:
                                tileRow = 7 - tileRow
                            if (tileProperty & 0x40) != 0:
                                tilePixel = 7 - tilePixel

                if readAll == True:
                    tileIndex += 1
                else:
                    break

            if readAll == False:
                    break

        # create an RGB pixel array with the selected palette and the readout palette color index
        pixelIndex = 0
        for pixelValue in pixelValues:
            paletteIndex = int(float(pixelValue / 16))
            colorIndex = (pixelValue % 16)
            palette = self.paletteset.palettes[paletteIndex - 1]    # TODO check why -1 is needed here
            imageBytes[pixelIndex + 0] = palette.data[((colorIndex * 3) + 0)]   # red
            imageBytes[pixelIndex + 1] = palette.data[((colorIndex * 3) + 1)]   # green
            imageBytes[pixelIndex + 2] = palette.data[((colorIndex * 3) + 2)]   # blue
            pixelIndex = pixelIndex + 3

        # create an image from the RGB pixel array
        tilemapImage = PIL.Image.frombytes('RGB', (pixelWidth, pixelHeight), bytes(imageBytes), 'raw')
        return tilemapImage

    