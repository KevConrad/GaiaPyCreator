from model.Model_RomData import Model_RomData

class Model_MapDataMusic:
    def __init__(self, romData) -> None:
        self.romData = romData

    def read(self, address):
        readOffset = address

        # read the music data
        self.byte0 = self.romData[readOffset]
        readOffset += 1
        self.byte1 = self.romData[readOffset]
        readOffset += 1
        self.address = Model_RomData.readLongAddress(self.romData, readOffset)
        readOffset += 3
        self.index = 0 # TODO Music.getIndexFromAddress(m_address);

        self.size = readOffset - address
            