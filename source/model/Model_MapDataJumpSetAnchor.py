
class Model_MapDataJumpSetAnchor:
    def __init__(self, romData, address) -> None:
        self.romData = romData

        self.index = self.romData[address]

        self.size = 1
            