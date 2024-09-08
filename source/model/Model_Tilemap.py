import PIL.Image
from model.Model_Compression import Model_Compression
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
        self.palette = int(str(tilemapData['Palette']), 16)
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
        
    def getImage(self, readOffset, readAll, tileOffset, tilesetReadOffset, tilePieceOffset):
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
        
        pixelValues = [0] * (self.TILEMAP_PIXEL_WIDTH * self.TILEMAP_PIXEL_HEIGHT)
        imageBytes = [0] * ((self.TILEMAP_PIXEL_WIDTH * self.TILEMAP_PIXEL_HEIGHT) * 3)

        tileIndex = 0
        tilePos = 0
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

                                if (readAll == False) and (tilePiece == tilePieceOffset):
                                    if (tilePixel == 0) or (tilePixel == 7) or (tileRow == 0) or (tileRow == 7):
                                        # pixelValue = 8 * 16; # TODO check if needed
                                        pass

                                if pixelValue == 0:
                                    continue

                                if (tileProperty & 0x80) != 0:     # mirror tile in x direction
                                    tileRow = 7 - tileRow
                                if (tileProperty & 0x40) != 0:     # mirror tile in y direction
                                    tilePixel = 7 - tilePixel

                                if tilePiece == 0:
                                    pixelValues[(self.TILEMAP_PIXEL_WIDTH * ((16 * tileY) + tileRow)) + (16 * tileX) + tilePixel] = pixelValue
                                if tilePiece == 1:
                                    pixelValues[(self.TILEMAP_PIXEL_WIDTH * ((16 * tileY) + tileRow)) + (16 * tileX) + tilePixel + 8] = pixelValue
                                if tilePiece== 2:
                                    pixelValues[(self.TILEMAP_PIXEL_WIDTH * ((16 * tileY) + tileRow + 8)) + (16 * tileX) + tilePixel] = pixelValue
                                if tilePiece == 3:
                                    pixelValues[(self.TILEMAP_PIXEL_WIDTH * ((16 * tileY) + tileRow + 8)) + (16 * tileX) + tilePixel + 8] = pixelValue
                                
                                if (tileProperty & 0x80) != 0:
                                    tileRow = 7 - tileRow
                                if (tileProperty & 0x40) != 0:
                                    tilePixel = 7 - tilePixel
                tilePos += 1

                if readAll == True:
                    tileIndex += 1
                else:
                    break

        palette = [0] * (16 * 3)
        palette[0] = 255
        palette[1] = 0
        palette[2] = 0

        palette[3] = 128
        palette[4] = 0
        palette[5] = 0
        
        palette[6] = 128
        palette[7] = 128
        palette[8] = 0
        
        palette[9] = 128
        palette[10] = 128
        palette[11] = 128
        
        palette[12] = 255
        palette[13] = 0
        palette[14] = 128
        
        palette[15] = 255
        palette[16] = 0
        palette[17] = 255
        
        palette[18] = 255
        palette[19] = 255
        palette[20] = 0
        
        palette[21] = 255
        palette[22] = 0
        palette[23] = 0

        palette[24] = 0
        palette[25] = 255
        palette[26] = 0
        
        palette[27] = 0
        palette[28] = 0
        palette[29] = 0

        palette[30] = 255
        palette[31] = 0
        palette[32] = 0
        
        palette[33] = 255
        palette[34] = 0
        palette[35] = 0
        
        palette[36] = 255
        palette[37] = 0
        palette[38] = 0
        
        palette[39] = 255
        palette[40] = 0
        palette[41] = 0
        
        palette[42] = 255
        palette[43] = 0
        palette[44] = 0
        
        palette[45] = 255
        palette[46] = 0
        palette[47] = 0

        # create an RGB pixel array with the selected palette and the readout palette color index
        pixelIndex = 0
        for pixelValue in pixelValues:
            imageBytes[pixelIndex] = palette[pixelValue & 0x0F]             # red
            imageBytes[pixelIndex + 1] = palette[(pixelValue & 0x0F) + 1]   # green
            imageBytes[pixelIndex + 2] = palette[(pixelValue & 0x0F) + 2]   # blue
            pixelIndex = pixelIndex + 3

        # create an image from the RGB pixel array
        tilemapImage = PIL.Image.frombytes('RGB', (self.TILEMAP_PIXEL_WIDTH, self.TILEMAP_PIXEL_HEIGHT), bytes(imageBytes))
        return tilemapImage

    