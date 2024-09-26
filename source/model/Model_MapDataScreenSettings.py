import sys

class Model_MapDataScreenSettings:
    def __init__(self, romData, address) -> None:
        self.romData = romData

        # read the screen settings data
        self.index = self.romData[address]

        self.size = 1
            