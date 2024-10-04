from model.Model_RomData import Model_RomData

class Model_MapDataTileset:
    LAYER_BG1 = 0
    LAYER_BG2 = 1
    LAYER_BG1_BG2 = 2
    LAYER_SPRITES = 3
    LAYER_HUD = 4
    
    def __init__(self, romData, address) -> None:
        self.romData = romData

        readOffset = address

        # read the tileset data
        self.offsetDecomp = self.romData[readOffset]
        readOffset += 1
        self.sizeDecomp = self.romData[readOffset]
        readOffset += 1
        self.destDecomp = self.romData[readOffset]
        readOffset += 1
        self.addressDecomp = Model_RomData.readLongAddress(self.romData, readOffset)
        readOffset += 3
        self.miniOffset = self.romData[readOffset]
        readOffset += 1

        self.index = 0 # TODO Tileset.getIndexFromAddress(addressDecomp);
        
        self.readLayer()

        self.size = readOffset - address

    def read(self):
        pass

    def readLayer(self):
        self.layer = self.LAYER_BG1

        if ((self.destDecomp == 0x00) and (self.sizeDecomp == 0x10) and
            (self.miniOffset == 0x00)):
            self.layer = self.LAYER_BG1
        elif ((self.destDecomp == 0x00) and (self.sizeDecomp == 0x20) and
              (self.miniOffset == 0x00)):
            self.layer = self.LAYER_BG1_BG2
        elif ((self.destDecomp == 0x10) and (self.miniOffset == 0x00)):
            self.layer = self.LAYER_BG2
        elif (self.miniOffset == 0x01):
            self.layer = self.LAYER_SPRITES
        elif (self.miniOffset == 0x02):
            self.layer = self.LAYER_HUD
            