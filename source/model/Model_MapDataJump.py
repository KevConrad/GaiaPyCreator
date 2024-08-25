
class Model_MapDataJump:
    def __init__(self, romData) -> None:
        self.romData = romData

    def read(self, address):
        # read the jump data
        self.targetLabelIndex = self.romData[address]

        self.size = 1
            