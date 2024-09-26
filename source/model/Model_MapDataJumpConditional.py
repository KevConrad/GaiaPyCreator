
class Model_MapDataJumpConditional:
    def __init__(self, romData, address) -> None:
        self.romData = romData

        readOffset = address

        # read the conditional jump data
        self.switchIndex = self.romData[readOffset]
        readOffset += 1
        self.targetLabelIndex = self.romData[readOffset]
        readOffset += 1
        
        self.size = readOffset - address
            