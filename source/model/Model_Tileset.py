import PIL.Image
from model.Model_Compression import Model_Compression

import bitstring

import PIL

class Model_Tileset:
    TILESET_BYTE_SIZE = 0x2000
    TILESET_PIXEL_HEIGHT = 1024
    TILESET_PIXEL_WIDTH = 1024

    TILESET_ROW_TILE_COUNT = 16
    TILESET_ROW_COUNT = 16
    TILESET_TILE_ROW_COUNT = 8
    TILESET_TILE_ROW_PIXEL_COUNT = 8
    TILESET_PIXEL_BIT_COUNT = 4

    def __init__(self, romData, tilesetData : dict) -> None:
        self.romData = romData

        self.name = str(tilesetData['Name'])
        self.address = int(str(tilesetData['Address']), 16)
        self.compSize = int(str(tilesetData['CompSize']), 16)
        self.decompOffset = int(str(tilesetData['DecompOffset']), 16)
        self.decompSize = int(str(tilesetData['DecompSize']), 16)
        self.format = int(str(tilesetData['Format']), 16)

    def read(self):
        if self.compSize > 0:
            self.data, self.decompSize = Model_Compression.decompress(self.romData, self.address, self.compSize)
        else:
            self.data = self.romData[self.address:self.decompSize]

    def getImage(self, readOffset): 
        # limit the length
        length = self.decompSize
        if length == (self.TILESET_BYTE_SIZE * 2):
            length = self.TILESET_BYTE_SIZE
        
        graphicBits = bitstring.ConstBitStream(bytes = self.data, offset=(readOffset * 8), length=(length * 8))
    
        pixelValues = [0] * (self.TILESET_PIXEL_WIDTH * self.TILESET_PIXEL_HEIGHT)
        imageBytes = []
        palette = [255, 0, 0,   128, 0, 0,  128, 128, 0,    128, 128, 128,  255, 0, 128,    255, 0, 255,    255, 255, 0,    255, 0, 0,
                   0, 255, 0,     0, 0, 0,   255, 0, 0,     255, 0, 0,      255, 0, 0,      255, 0, 0,      255, 0, 0,      255, 0, 0]

        # loop for 16 rows of the tileset
        for tileRow in range (self.TILESET_ROW_TILE_COUNT):
            # loop for the 16 tiles in each row
            for tileColumn in range (self.TILESET_TILE_ROW_COUNT):
                # loop for the 8 rows of a tile
                for i in range (self.TILESET_TILE_ROW_COUNT):
                    # loop for the 8 pixels of a tile's row
                    for j in range (self.TILESET_TILE_ROW_PIXEL_COUNT):
                        pixelBit = []
                        # loop for the 4 bits of a single pixel
                        for k in range (self.TILESET_PIXEL_BIT_COUNT):
                            if k == 0:
                                bitValue = graphicBits[(tileRow * 4096) + (tileColumn * 256) + (i * 16) + j]
                            if k == 1:
                                bitValue = graphicBits[(tileRow * 4096) + (tileColumn * 256) + (i * 16) + 8 + j]
                            if k == 2:
                                bitValue = graphicBits[(tileRow * 4096) + (tileColumn * 256) + (i * 16) + (16 * 8) + j]
                            if k == 3:
                                bitValue = graphicBits[(tileRow * 4096) + (tileColumn * 256) + (i * 16) + (17 * 8) + j]

                            if bitValue == 1:
                                pixelBit.append(1)
                            else:
                                pixelBit.append(0)

                        pixelValue = ((pixelBit[0] << 3) | (pixelBit[1] << 2) | (pixelBit[2] << 1) | pixelBit[3])
                        pixelValues[((tileRow) * 1024) + (tileColumn * 8) + (128 * i) + j] = (pixelValue & 0x0F)
                    
                    imageBytes.append(palette[pixelValue])         # red
                    imageBytes.append(palette[pixelValue + 1])     # green
                    imageBytes.append(palette[pixelValue + 2])     # blue

        # copy the pixel values back to the bitmap
        tilesetImage = PIL.Image.frombytes('RGB', (self.TILESET_PIXEL_WIDTH, self.TILESET_PIXEL_HEIGHT), imageBytes)

        return tilesetImage

    