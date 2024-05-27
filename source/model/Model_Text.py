
import sys 

from model.Model_TextConverter import Model_TextConverter

class Model_Text:
    MAX_TEXT_SIZE = 512                             # maximum number of text characters which is read

    ASCII_TEXT_DICTIONARY_ADDRESS = 0x1EB0F         # ROM address of the text dictionary (use fix address because dictionary is only read)    
    ASCII_TEXT_DICTIONARY_COMMAND = 0x10            # command to read data from the text dictionary
    
    MESSAGE_TEXT_DICTIONARY_ADDRESS_0 = 0x1EBA8     # ROM address of message text dictionary 0 (use fix address because dictionary is only read) 
    MESSAGE_TEXT_DICTIONARY_ADDRESS_1 = 0x1F54D     # ROM address of message text dictionary 1 (use fix address because dictionary is only read) 
    MESSAGE_TEXT_DICTIONARY_INDEX_0 = 0xD6          # index of message text dictionary 0
    MESSAGE_TEXT_DICTIONARY_INDEX_1 = 0xD7          # index of message text dictionary 1

    MESSAGE_TEXT_END_COMMAND = 0xCA                 # command for the reached end of a text message
    
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
    
    def getMessageDictionaryEntry(romData, dictionaryIndex, dictionaryEntryIndex):
        # get the text address
        if dictionaryIndex == Model_Text.MESSAGE_TEXT_DICTIONARY_INDEX_0:
            dictionaryEntryAddress = Model_Text.MESSAGE_TEXT_DICTIONARY_ADDRESS_0 + (dictionaryEntryIndex * 2)
        else:
            dictionaryEntryAddress = Model_Text.MESSAGE_TEXT_DICTIONARY_ADDRESS_1 + (dictionaryEntryIndex * 2)

        textAddress = 0x10000 + (romData[dictionaryEntryAddress + 1] << 8) + romData[dictionaryEntryAddress]

        # read the text from the dictionary
        text = ""
        while ((romData[textAddress] != Model_Text.MESSAGE_TEXT_END_COMMAND) and
               (sys.getsizeof(text) < Model_Text.MAX_TEXT_SIZE)):
            text += Model_TextConverter.decodeMessageCharacter(romData[textAddress])
            textAddress += 1
        return text
    
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
    
    def readMessageText(romData, address):
        text = ""
        while ((romData[address] != Model_Text.MESSAGE_TEXT_END_COMMAND) and
               (sys.getsizeof(text) < Model_Text.MAX_TEXT_SIZE)):
            if (romData[address] == Model_Text.MESSAGE_TEXT_DICTIONARY_INDEX_0 or
                romData[address] == Model_Text.MESSAGE_TEXT_DICTIONARY_INDEX_1):
                dictionaryIndex = romData[address]
                address += 1
                dictionaryEntryIndex = romData[address]
                address += 1
                text += Model_Text.getMessageDictionaryEntry(romData, dictionaryIndex, dictionaryEntryIndex)
            else:
                messageCharacter = Model_TextConverter.decodeMessageCharacter(romData[address])
                address += 1
                text += messageCharacter
        return text