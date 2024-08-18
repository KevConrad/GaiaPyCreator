import PIL.Image
from model.Model_Compression import Model_Compression

import bitstring

import PIL

class Model_Tileset:
    TILESET_BYTE_SIZE = 0x2000

    TILESET_TILE_HEIGHT = 16        # number of tiles in vertical direction
    TILESET_TILE_WIDTH = 16         # number of tiles in horizontal direction
    TILESET_TILE_PIXEL_HEIGHT = 8   # number of pixels in a tile in vertical direction
    TILESET_TILE_PIXEL_WIDTH = 8    # number of pixels in a tile in horizontal direction
    TILESET_PIXEL_BIT_COUNT = 4     # number of bits for a single pixel
    
    TILESET_PIXEL_HEIGHT = TILESET_TILE_HEIGHT * TILESET_TILE_PIXEL_HEIGHT
    TILESET_PIXEL_WIDTH = TILESET_TILE_WIDTH * TILESET_TILE_PIXEL_WIDTH

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
            # decompress the compressed tileset data (increment length of compressed data to prevent data truncation)
            self.data, self.compSize = Model_Compression.decompress(self.romData, self.address, self.compSize + 1)
        else:
            self.data = self.romData[self.address:self.decompSize]

    def getImage(self, readOffset): 
        # limit the length
        length = self.decompSize
        if length == (self.TILESET_BYTE_SIZE * 2):
            length = self.TILESET_BYTE_SIZE
        
        graphicBits = bitstring.ConstBitStream(bytes = self.data, offset=(readOffset * 8), length=(length * 8))
        print(length)
        print(graphicBits.length)
    
        pixelValues = [0] * (self.TILESET_PIXEL_WIDTH * self.TILESET_PIXEL_HEIGHT)
        imageBytes = [0] * ((self.TILESET_PIXEL_WIDTH * self.TILESET_PIXEL_HEIGHT) * 3)

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

        # loop for 16 tiles of the tileset in vertical direction
        for tileRow in range (self.TILESET_TILE_HEIGHT):
            # loop for the 16 of the tileset in horizontal direction for the current tile row
            for tileColumn in range (self.TILESET_TILE_WIDTH):
                # loop for the 8 pixels of a tile in vertical direction
                for i in range (self.TILESET_TILE_PIXEL_HEIGHT):
                    # loop for the 8 pixels of a tile in horizontal direction for the current pixel row
                    for j in range (self.TILESET_TILE_PIXEL_WIDTH):
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

        # create an RGB pixel array with the selected palette and the readout palette color index
        pixelIndex = 0
        for pixelValue in pixelValues:
            imageBytes[pixelIndex] = palette[pixelValue & 0x0F]             # red
            imageBytes[pixelIndex + 1] = palette[(pixelValue & 0x0F) + 1]   # green
            imageBytes[pixelIndex + 2] = palette[(pixelValue & 0x0F) + 2]   # blue
            pixelIndex = pixelIndex + 3

        # create an image from the RGB pixel array
        tilesetImage = PIL.Image.frombytes('RGB', (self.TILESET_PIXEL_WIDTH, self.TILESET_PIXEL_HEIGHT), bytes(imageBytes))
        tilesetImage.show()
        return tilesetImage

    