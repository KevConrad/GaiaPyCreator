from enum import Enum

from model.Model_Event import Model_Event
from model.Model_EventCommandData import Model_EventCommandData
from model.Model_RomData import Model_RomData

class Model_EventCommand:
    COMMAND_PREFIX_ASSEMBLER = 0x0A00
    COMMAND_PREFIX_COP = 0x0200

    class BaseType(Enum):
        ASSEMBLER_COMMAND = 0,
        COP_COMMAND = 1
    
    # enumeration for command types
    class CommandType(Enum):
        ACTION = 0,
        BRANCH = 1,
        CALL = 2,
        CHOICE = 3,
        CHOICE_ENTRY = 4,
        CONDITION = 5,
        CONDITION_TRUE = 6,
        CONDITION_TRUE_ONLY = 7,
        CONDITION_FALSE = 8,
        JUMP = 9,
        LEAVE = 10,
        MULTIPLE_CONDITION = 11,
        MULTIPLE_CONDITION_ENTRY = 12

    def __init__(self, romData, address, hierarchy, commandData : Model_EventCommandData) -> None:
        self.romData = romData
        self.address = address
        self.readOffset = address
        self.hierarchy = hierarchy
        self.type = self.CommandType.ACTION        # set default command type
       
        self.read()

    def __init__(self, romData, address, commandData : Model_EventCommandData) -> None:
        self.romData = romData
        self.address = address
        self.readOffset = address
        self.commandData = commandData

        self.read()

    def getCommandType(self):
        # Implementation to determine command type
        pass

    def read(self):
        # read command id
        self.readId()

        # read command data based on id
        self.data = self.commandData.getCommandDataById(self.id)
        print("data:", self.data['id'])

    def readId(self):
        # read command id
        if self.romData[self.readOffset] == 0x02:
            self.readOffset += 1
            self.id = self.COMMAND_PREFIX_COP + self.romData[self.readOffset]
            self.readOffset += 1
            self.size = 2
            self.baseType = self.BaseType.COP_COMMAND
        else:
            self.id = self.COMMAND_PREFIX_ASSEMBLER + self.romData[self.readOffset]
            self.readOffset += 1
            self.size = 1
            self.baseType = self.BaseType.ASSEMBLER_COMMAND 
    