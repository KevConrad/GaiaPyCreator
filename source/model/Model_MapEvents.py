import sys
from model.Model_Event import Model_Event
from model.Model_RomData import Model_RomData
from model.Model_Text import Model_Text

class Model_MapEvents:
    EVENT_DATA_SET_END = 0xFF
    
    def __init__(self, romData, address) -> None:
        self.romData = romData
        readOffset = address

        self.playerEventEnable = False
        
        # read the general event data
        if (romData[readOffset] != self.EVENT_DATA_SET_END):
            self.playerEventEnable = True
            self.eventByte0 = romData[readOffset]
            readOffset += 1
            self.eventByte1 = romData[readOffset]
            readOffset += 1
            self.readPlayerFlags(romData[readOffset])
            readOffset += 1
            self.playerEventAddress = Model_RomData.readLongAddress(self.romData, readOffset)
            readOffset += 3
            self.eventByte2 = romData[readOffset]   # TODO: Delimiter byte (0x00) (?) 
            readOffset += 1

            # read all map events
            self.events = [] 
            while (romData[readOffset] != self.EVENT_DATA_SET_END):
                event = Model_Event(romData, readOffset)
                self.events.append(event)

                readOffset += event.size

                # TODO add the event script to the global list of scripts

            readOffset += 1
            
            self.displayedName = Model_Text.readMessageText(romData, readOffset)
            print(self.displayedName)

            if (len(self.displayedName) > 1):
                self.isNameDisplayed = True
            else:
                self.isNameDisplayed = False

    def readPlayerFlags(self, playerFlagByte):
        # Read the "above map" flag
        self.isPlayerAboveMap = bool(playerFlagByte & (1 << 4))
        
        # Read the "enable fight" flag
        self.isPlayerFightEnabled = not bool(playerFlagByte & (1 << 1))
        
        # Read the "invisible" flag
        self.isPlayerInvisible = bool(playerFlagByte & (1 << 0))
        
        # Read the "mirror horizontal" flag
        self.isPlayerMirroredHorizontal = bool(playerFlagByte & (1 << 7))
        
        # Read the "mirror vertical" flag
        self.isPlayerMirroredVertical = bool(playerFlagByte & (1 << 6))
