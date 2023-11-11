
class Model_Text:
    MAX_NAME_SIZE = 64

    def readAsciiText(romData, address):
        print("Entry adddress: " + str(hex(address)))

        loopIndex = 0
        text = ""
        while (romData[address + loopIndex] != 0) and (loopIndex < Model_Text.MAX_NAME_SIZE):

            asciiCharacter = Model_Text.decodeAsciiCharacter(romData[address + loopIndex])
            text += asciiCharacter
            loopIndex += 1
        return text
    
    def decodeAsciiCharacter(character):
        switch = {
            0x40:' ',
            ' ':'.',
            '\\':'\'',
            0x0D:"\r\n",
        }
        return switch.get(character, chr(character))
    
    def getDictionaryEntry(entry):
        pass