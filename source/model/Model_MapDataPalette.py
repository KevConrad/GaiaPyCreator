from model.Model_RomData import Model_RomData

class Model_MapDataPalette:
    MAP_LAYER = 0
    SPRITE_LAYER = 1

    def __init__(self, romData, address) -> None:
        self.romData = romData

        readOffset = address

        # read the palette data
        self.offsetDataSource = self.romData[readOffset]
        readOffset += 1
        self.numBytes = self.romData[readOffset]
        readOffset += 1
        self.offsetDataDestination = self.romData[readOffset]
        readOffset += 1
        self.address = Model_RomData.readLongAddress(self.romData, readOffset)
        readOffset += 3

        self.index = 0 # TODO PaletteSet.getIndexFromAddress(m_address);

        if(self.index < 0):
            self.index = 0

        if ((self.offsetDataDestination == 0x80) or
            (self.offsetDataDestination == 0x90) or
            (self.offsetDataDestination == 0xA0)):
            self.layer = self.SPRITE_LAYER
        else:
            self.layer = self.MAP_LAYER
        
        self.size = readOffset - address
            