
import sys 

from model.Model_TextConverter import Model_TextConverter

class Model_Text:
    MAX_TEXT_SIZE = 64                              # maximum number of text characters which is read

    ASCII_TEXT_DICTIONARY_ADDRESS = 0x1EB0F         # ROM address of the text dictionary (use fix address because dictionary is only read)    
    ASCII_TEXT_DICTIONARY_COMMAND = 0x10            # command to read data from the text dictionary
    
    DIALOGUE_TEXT_DICTIONARY_ADDRESS_0 = 0x1EBA8    # ROM address of dialogue text dictionary 0 (use fix address because dictionary is only read) 
    DIALOGUE_TEXT_DICTIONARY_ADDRESS_1 = 0x1F54D    # ROM address of dialogue text dictionary 1 (use fix address because dictionary is only read) 
    DIALOGUE_TEXT_DICTIONARY_INDEX_0 = 0xD6         # index of dialogue text dictionary 0
    DIALOGUE_TEXT_DICTIONARY_INDEX_1 = 0xD7         # index of dialogue text dictionary 1

    def readAsciiText(romData, address):
        text = ""
        while (romData[address] != 0) and (sys.getsizeof(text) < Model_Text.MAX_TEXT_SIZE):
            if (romData[address] == Model_Text.ASCII_TEXT_DICTIONARY_COMMAND):
                address += 1
                dictionaryIndex = romData[address]
                address += 1
                text += Model_Text.getAsciiDictionaryEntry(romData, dictionaryIndex)
            else:
                asciiCharacter = Model_TextConverter.decodeAsciiCharacter(romData[address])
                address += 1
                text += asciiCharacter
        return text
    
    def getAsciiDictionaryEntry(romData, entry):
        # get the text address
        dictionaryEntryAddress = Model_Text.ASCII_TEXT_DICTIONARY_ADDRESS + (entry * 2);                        
        textAddress = 0x10000 + (romData[dictionaryEntryAddress + 1] << 8) + romData[dictionaryEntryAddress]

        # read the text from the dictionary
        text = ""
        while (romData[textAddress] != 0) and (sys.getsizeof(text) < Model_Text.MAX_TEXT_SIZE):
            text += Model_TextConverter.decodeAsciiCharacter(romData[textAddress])
            textAddress += 1
        return text