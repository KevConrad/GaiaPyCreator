
class Model_MapDataJump:
    def __init__(self, romData, address) -> None:
        self.romData = romData
        
        # read the jump data
        self.targetLabelIndex = self.romData[address]

        self.size = 1
        
            