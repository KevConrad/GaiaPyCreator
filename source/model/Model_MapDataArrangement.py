from model.Model_Compression import Model_Compression
from model.Model_RomData import Model_RomData

class Model_MapDataArrangement:
    READ_OFFSET = 2                 # read offset for the compressed data

    def __init__(self, romData, address) -> None:
        self.romData = romData
        
        readOffset = address

        # read the map arrangement data
        self.slotId = self.romData[readOffset]
        readOffset += 1
        self.address = Model_RomData.readLongAddress(self.romData, readOffset)
        readOffset += 3
        self.index = 0 # TODO MapArrangementData.getIndexFromAddress(m_address);
        
        self.sizeX = self.romData[self.address] * 16
        self.sizeY = self.romData[self.address + 1] * 16

        self.size = readOffset - address

    def read(self):
        # decompress the compressed map arrangement data
        self.data, self.compSize = Model_Compression.decompress(self.romData, self.address + self.READ_OFFSET, 0)
            