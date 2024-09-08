from enum import Enum

# enumeration for the different palette formats
class PaletteFormat(Enum):
    FORMAT_2BPP = 0                     # 2BPP (2 bits per pixel) palette format
    FORMAT_4BPP = 1                     # 4BPP (4 bits per pixel) palette format
        
class Model_Palette:
    PALETTE_COLOR_COUNT_2BPP = 4        # number of colors in a 2BPP palette
    PALETTE_COLOR_COUNT_4BPP = 16       # number of colors in a 4BPP palette
    PALETTE_COLOR_BYTE_COUNT = 3        # number of bytes for a single color

    # array which contains the index of the palette color of 2BPP palettes
    PALETTE_COLOR_POSITIONS_2BPP = [ 0, 2, 1, 3 ]

    # array which contains the index of the palette color of 4BPP palettes
    PALETTE_COLOR_POSITIONS_4BPP = [ 0, 8, 4, 12, 2, 10, 6, 14, 1, 9, 5, 13, 3, 11, 7, 15 ]

    PALETTE_SIZE_2BPP = 8               # size of a 2BPP (2 bits per pixel) palette in bytes
    PALETTE_SIZE_4BPP = 32              # size of a 4BPP (4 bits per pixel) palette in bytes

    def __init__(self, romData, address, format : PaletteFormat) -> None:
        self.romData = romData
        self.address = address
        self.format = format
    
    def read(self):
        if (self.format == PaletteFormat.FORMAT_2BPP):
            colorCount = self.PALETTE_COLOR_COUNT_2BPP
            colorPositions = self.PALETTE_COLOR_POSITIONS_2BPP
            self.data = [0] * (self.PALETTE_COLOR_COUNT_2BPP * 3)
        else:                       # 4BPP format
            colorCount = self.PALETTE_COLOR_COUNT_4BPP
            colorPositions = self.PALETTE_COLOR_POSITIONS_4BPP
            self.data = [0] * (self.PALETTE_COLOR_COUNT_4BPP * 3)

        for colorIndex in range (colorCount):
            rawColor = ((self.romData[self.address + (colorIndex * 2) + 1] & 0x7F) << 8)
            rawColor += self.romData[self.address + (colorIndex * 2)]
            red = (rawColor % 32) * 8                           # red color value
            green = ((rawColor / 32) % 32) * 8                  # green color value
            blue = ((rawColor / 1024) % 32) * 8                 # blue color value

            # assign the correct position value of the color within the palette data
            self.data[colorPositions[colorIndex] * 3] = red
            self.data[(colorPositions[colorIndex] * 3) + 1] = green
            self.data[(colorPositions[colorIndex] * 3) + 2] = blue