from model.Model_RomData import Model_RomData

class Model_MapDataSprites:
    def __init__(self, romData) -> None:
        self.romData = romData

    def read(self, address):
        readOffset = address

        # read the sprites data
        self.uncompressedDataSize = Model_RomData.readLittleEndianValue(self.romData, readOffset)
        readOffset += 2
        self.unusedByte = self.romData[readOffset]
        readOffset += 1
        self.address = Model_RomData.readLongAddress(self.romData, readOffset)
        readOffset += 3

        self.index = 0 # TODO SpriteSet.getIndexFromAddress(m_address);

        self.size = readOffset - address
            