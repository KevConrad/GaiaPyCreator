
class Model_MapDataJumpSetAnchor:
    def __init__(self, romData) -> None:
        self.romData = romData

    def read(self, address):
        self.index = self.romData[address]

        self.size = 1
            