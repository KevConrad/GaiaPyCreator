
class Model_MapData0x0E:
    def __init__(self, romData) -> None:
        self.romData = romData

    def read(self, address):
        readOffset = address

        # read the 0x0E data
        self.byte0 = self.romData[readOffset]
        readOffset += 1
        self.byte1 = self.romData[readOffset]
        readOffset +=1
        self.byte2 = self.romData[readOffset]
        readOffset +3

        self.size = readOffset - address
            