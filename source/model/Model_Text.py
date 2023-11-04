
class Model_Text:
    def __init__(self, romData):
        self.romData = romData

    def readMenuText(self, address):
        print("address")
        text = ""
        while (self.romData[address] != 0):
            text += self.romData[address]
            address += 1
        return text