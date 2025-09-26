
class Model_Treasure:
    TREASURE_DATA_SET_SIZE = 4

    def __init__(self, romData, address) -> None:
        self.romData = romData

        # read the treasure data

        # read the position of the treasure
        self.positionX = romData[address]
        address += 1
        self.positionY = romData[address]
        address += 1
        self.itemIndex = romData[address]
        address += 1

        # Read the flag which states if music is played when the treasure is opened
        if (romData[address] & 0x80) != 0:
            self.isMusicPlayed = True
        else:
            self.isMusicPlayed = False
        
        # read the treasure id
        self.id = romData[address] & 0x7F
    