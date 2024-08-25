from model.Model_RomData import Model_RomData

class Model_MapDataArrangement:
    def __init__(self, romData) -> None:
        self.romData = romData

    def read(self, address):
        readOffset = address

        # read the map arrangement data
        self.slotId = self.romData[readOffset];
        readOffset += 1
        self.address = Model_RomData.readLongAddress(self.romData, readOffset)
        readOffset += 3
        self.index = 0 # TODO MapArrangementData.getIndexFromAddress(m_address);

        self.size = readOffset - address
            