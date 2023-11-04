
class Model_RomDataTable:
    def __init__(self, romData, address, size) -> None:
        self.address = address
        self.romData = romData
        self.size = size

    def getDataAddress(self, index):
        print("address: " + self.address)
        tableEntryAddress = self.address + index * 2

        return (self.address & 0xFF0000) + (self.romData[tableEntryAddress + 1] << 8) + self.romData[tableEntryAddress]