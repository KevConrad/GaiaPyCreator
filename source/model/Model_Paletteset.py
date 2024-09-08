from model.Model_Palette import Model_Palette
from model.Model_Palette import PaletteFormat

class Model_Paletteset:
    PALETTESET_PALETTE_COUNT = 8        # number of palettes in a paletteset

    def __init__(self, romData, address, index) -> None:
        self.romData = romData
        self.address = address
        self.index = index
        self.name = "Paletteset " + str(index)
        
        # read all palettes from the paletteset
        self.palettes = []
        for paletteIndex in range(self.PALETTESET_PALETTE_COUNT):
            paletteAddress = self.address + (paletteIndex * Model_Palette.PALETTE_SIZE_4BPP)
            self.palettes.append(Model_Palette(paletteAddress, PaletteFormat.FORMAT_4BPP))
    
    