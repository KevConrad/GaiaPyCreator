from pubsub import pub

print('pubsub API version', pub.VERSION_API)

# notification
from pubsub.utils.notification import useNotifyByWriteFile
import sys

class Model_RomData:
    def __init__(self) -> None:
        pub.subscribe(self.read, "rom_opened")

    def read(self, romPath):
        file = open(romPath, "rb")
        self.romData = file.read()
        
        file.close