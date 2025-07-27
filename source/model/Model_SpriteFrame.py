
from model.Model_Paletteset import Model_Paletteset
from model.Model_SpriteFrameTileData import Model_SpriteFrameTileData

import PIL

class Model_SpriteFrame:
    def __init__(self, romData, spriteData, address, palettesetAddress) -> None:
        readOffset = address
        self.address = address
        self.palettesetAddress = palettesetAddress
        self.romData = romData

        self.offsetX = spriteData[readOffset]
        readOffset += 1
        self.frameByte0 = spriteData[readOffset]
        readOffset += 1
        self.offsetY = spriteData[readOffset]
        readOffset += 1
        self.frameByte1 = spriteData[readOffset]
        readOffset += 1
        self.frameByte2 = spriteData[readOffset]
        readOffset += 1
        self.frameByte3 = spriteData[readOffset]
        readOffset += 1
        self.frameByte4 = spriteData[readOffset]
        readOffset += 1
        self.frameByte5 = spriteData[readOffset]
        readOffset += 1
        self.frameByte6 = spriteData[readOffset]
        readOffset += 1
        self.frameByte7 = spriteData[readOffset]
        readOffset += 1
        self.frameByte8 = spriteData[readOffset]
        readOffset += 1
        self.frameByte9 = spriteData[readOffset]
        readOffset += 1
        self.tileCount = spriteData[readOffset]
        readOffset += 1

        # Read the tile data
        self.tileData = []
        for tileIndex in range (self.tileCount):
            tileData = Model_SpriteFrameTileData(spriteData, readOffset)
            self.tileData.append(tileData)
            readOffset += tileData.size

        self.size = readOffset - address

    def createImage(self, width, height, tilesetBits):
        self.pixelValues = [0] * (width * height)
        self.imageBytes = [0] * (width * height * 3)

        for tile in range (self.tileCount):
            paletteset = Model_Paletteset(self.romData, self.palettesetAddress)

            tilePieceCount = 0
            if self.tileData[tile].tileCutout == True:
                tilePieceCount = 1
            else:
                tilePieceCount = 4

            for tilePiece in range (tilePieceCount):
                if tilePiece == 0:
                    tileIndexX = self.tileData[tile].tileIdX
                    tileIndexY = self.tileData[tile].tileIdY
                elif tilePiece == 1:
                    if self.tileData[tile].tileIdX == 0x0F:
                        tileIndexX = self.tileData[tile].tileIdX
                    else:
                        tileIndexX = self.tileData[tile].tileIdX + 1
                    tileIndexY = self.tileData[tile].tileIdY
                elif tilePiece == 2:
                    tileIndexX = self.tileData[tile].tileIdX
                    if self.tileData[tile].tileIdY == 0x0F:
                        tileIndexY = self.tileData[tile].tileIdY
                    else:
                        tileIndexY = self.tileData[tile].tileIdY + 1
                else:   # tilePiece is "3"
                    if self.tileData[tile].tileIdX == 0x0F:
                        tileIndexX = self.tileData[tile].tileIdX
                    else:
                        tileIndexX = self.tileData[tile].tileIdX + 1
                    if self.tileData[tile].tileIdY == 0x0F:
                        tileIndexY = self.tileData[tile].tileIdY
                    else:
                        tileIndexY = self.tileData[tile].tileIdY + 1

                tilesetReadIndex = 0
                if self.tileData[tile].tilesetId == 1:
                    tilesetReadIndex = 1
                else:
                    tilesetReadIndex = 0

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

                        # add the palette offset to the pixel value
                        if (self.tileData[tile].tilePaletteId > 0) and (pixelValue != 0):
                            pixelValue += ((self.tileData[tile].tilePaletteId - 1) * 16)

                        # mirror tile in x direction if the mirror x bit is set
                        if self.tileData[tile].tileMirrorX == True:
                            tileRow = 7 - tileRow
                        
                        # mirror tile in y direction if the mirror y bit is set
                        if self.tileData[tile].tileMirrorY == True:
                            tilePixel = 7 - tilePixel
                        
                        tilePieceTemp = tilePiece
                        if ((self.tileData[tile].tileMirrorX == True) and 
                            (self.tileData[tile].tileMirrorY == True) and
                            (self.tileData[tile].tileCutout == False)):
                            if tilePiece == 0:
                                tilePiece = 3
                            elif tilePiece == 1:
                                tilePiece = 2
                            elif tilePiece == 2:
                                tilePiece = 1
                            elif tilePiece == 3:
                                tilePiece = 0
                        elif ((self.tileData[tile].tileMirrorY == True) and
                              (self.tileData[tile].tileCutout == False)):
                            if (tilePiece == 0):
                                tilePiece = 1
                            elif (tilePiece == 1):
                                tilePiece = 0
                            elif (tilePiece == 2):
                                tilePiece = 3
                            elif (tilePiece == 3):
                                tilePiece = 2
                        elif ((self.tileData[tile].tileMirrorX == True) and
                              (self.tileData[tile].tileCutout == False)):
                            if (tilePiece == 0):
                                tilePiece = 2
                            elif (tilePiece == 1):
                                tilePiece = 3
                            elif (tilePiece == 2):  
                                tilePiece = 0
                            elif (tilePiece == 3):
                                tilePiece = 1

                        pixelValueIndex = 0
                        if tilePiece == 0:
                            pixelValueIndex = ((self.tileData[tile].tileOffsetY + tileRow) * width) + (self.tileData[tile].tileOffsetX + tilePixel)
                        elif tilePiece == 1:
                            pixelValueIndex = ((self.tileData[tile].tileOffsetY + tileRow) * width) + (self.tileData[tile].tileOffsetX + tilePixel + 8)
                        elif tilePiece == 2:
                            pixelValueIndex = ((self.tileData[tile].tileOffsetY + tileRow + 8) * width) + (self.tileData[tile].tileOffsetX + tilePixel)
                        elif tilePiece == 3:
                            pixelValueIndex = ((self.tileData[tile].tileOffsetY + tileRow + 8) * width) + (self.tileData[tile].tileOffsetX + tilePixel + 8)

                        self.pixelValues[pixelValueIndex] = pixelValue

                        # update the RGB pixel array with the selected palette and the readout palette color index
                        paletteIndex = int(float(pixelValue / 16))
                        colorIndex = (pixelValue % 16)
                        palette = paletteset.palettes[paletteIndex + 1]
                        imageBytesIndex = pixelValueIndex * 3
                        self.imageBytes[imageBytesIndex + 0] = palette.data[((colorIndex * 3) + 0)]   # red
                        self.imageBytes[imageBytesIndex + 1] = palette.data[((colorIndex * 3) + 1)]   # green
                        self.imageBytes[imageBytesIndex + 2] = palette.data[((colorIndex * 3) + 2)]   # blue
                            
                        # Mirror tile in x direction
                        if self.tileData[tile].tileMirrorX == True:
                            tileRow = 7 - tileRow
                        # Mirror tile in y direction
                        if self.tileData[tile].tileMirrorY == True:
                            tilePixel = 7 - tilePixel
                        
                        tilePiece = tilePieceTemp

        # create an image from the RGB pixel array
        self.spriteImage = PIL.Image.frombytes('RGB', (width, height), bytes(self.imageBytes), 'raw')

        return self.spriteImage


    