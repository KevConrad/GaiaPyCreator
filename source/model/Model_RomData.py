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