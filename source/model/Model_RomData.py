from pubsub import pub

print('pubsub API version', pub.VERSION_API)

# notification
from pubsub.utils.notification import useNotifyByWriteFile
import sys

class Model_RomData:
    def __init__(self) -> None:
        pub.subscribe(self.readFromRomFile, "rom_opened")

    def readFromRomFile(self, romPath):
        print("Read ROM data.")
        file = open(romPath, "rb")
        self.romData = file.read()
        
        file.close

    def readLittleEndianValue(romData, address):
        lowByte = romData[address]
        highByte = romData[address + 1]
        return (lowByte | (highByte << 8))

    def readLongAddress(romData, address):
        # read the address from the source data
        longAddress = romData[address] | (romData[address + 1] << 8) | (romData[address + 2] << 16)

        tempAddress = longAddress & 0xFFFF

        if (tempAddress >= 0x8000):
            longAddress -= 0x800000
        else:
            longAddress -= 0xC00000

        return longAddress