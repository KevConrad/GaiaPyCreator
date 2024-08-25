import sys

class Model_MapDataScreenSettings:
    def __init__(self, romData) -> None:
        self.romData = romData

    def read(self, address):
        # read the screen settings data
        self.index = self.romData[address]

        self.size = 1
            