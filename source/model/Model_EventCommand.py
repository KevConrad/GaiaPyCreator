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

    def __init__(self, romData=None, address=None, hierarchy=None, commandData=None, hierarchyLevel=None, name=None, id=None, type=None, commandIndex=None) -> None:
        """Unified __init__ method that handles different initialization patterns."""
        if romData is not None and address is not None and hierarchy is not None and commandData is not None:
            # First initialization pattern: full command from ROM data
            self.romData = romData
            self.address = address
            self.readOffset = address
            self.hierarchy = hierarchy
            self.commandData = commandData
            self.type = self.CommandType.ACTION  # set default command type
            self.read()
        elif romData is not None and address is not None and commandData is not None and hierarchy is None:
            # Second initialization pattern: command from ROM data without hierarchy
            self.romData = romData
            self.address = address
            self.readOffset = address
            self.commandData = commandData
            self.read()
        elif hierarchyLevel is not None and name is not None and id is not None and type is not None:
            # Third initialization pattern: command from parameters
            self.address = None
            self.commandHierarchy = hierarchyLevel
            self.id = id
            self.name = name
            self.type = type
        elif address is not None and hierarchyLevel is not None and id is not None and commandIndex is not None:
            # Fourth initialization pattern: branch command constructor
            self.address = address
            self.commandHierarchy = hierarchyLevel
            self.data = []
            self.id = id
            self.name = f"BRANCH -> Command [{commandIndex:03d}]"
            self.type = Model_EventCommandData.CommandType.LEAVE
        else:
            raise ValueError("Invalid combination of parameters for Model_EventCommand initialization")

    @classmethod
    def from_rom_data_with_hierarchy(cls, romData, address, hierarchy, commandData):
        """Create a Model_EventCommand from ROM data with hierarchy."""
        return cls(romData=romData, address=address, hierarchy=hierarchy, commandData=commandData)

    @classmethod
    def from_rom_data(cls, romData, address, commandData):
        """Create a Model_EventCommand from ROM data."""
        return cls(romData=romData, address=address, commandData=commandData)

    @classmethod
    def from_parameters(cls, hierarchyLevel: int, name: str, id: int, type):
        """Create a Model_EventCommand from explicit parameters."""
        return cls(hierarchyLevel=hierarchyLevel, name=name, id=id, type=type)

    @classmethod
    def from_branch_command(cls, address: int, hierarchyLevel: int, id: int, commandIndex: int):
        """Create a Model_EventCommand for a branch command."""
        return cls(address=address, hierarchyLevel=hierarchyLevel, id=id, commandIndex=commandIndex)

    def read(self):    
        # read command id
        self.read_id()

        # read command data based on id
        self.id, self.name, self.type, self.dataTypes = self.commandData.getCommandDataById(self.id)
        print("id:", self.id)
        print("name:", self.name)
        print("commandType:", self.type)

        self.dataValues = []
        if self.dataTypes is not None:
            for dataType in self.dataTypes:
                print("dataType:", dataType)
                value = self.read_data(self.romData, dataType, self.name)
                print("value:", value)
                self.dataValues.append(value)
        
        self.size = self.readOffset - self.address
        print("final command size:", self.size)

    def read_id(self):
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

    def read_data(self, source, 
                 dataType: Model_EventCommandData.DataType, name: str) -> int:
        value = None
        if dataType in (
            Model_EventCommandData.DataType.ABSOLUTE_ADDRESS,
            Model_EventCommandData.DataType.EVENT_SCRIPT,
            Model_EventCommandData.DataType.RAM_ADDRESS_LONG,
            Model_EventCommandData.DataType.SPRITESET,
        ):
            address = int.from_bytes(source[self.readOffset:self.readOffset + 3], "little")
            self.readOffset += 3
            value = address

        if dataType == Model_EventCommandData.DataType.EVENT_SCRIPT:
            self.branchAddress = int(value)

        elif dataType == Model_EventCommandData.DataType.BOOL:
            value = source[self.readOffset] == 0x01
            self.readOffset += 1

        elif dataType in (
            Model_EventCommandData.DataType.BYTE,
            Model_EventCommandData.DataType.CHOICE_COUNT,
            Model_EventCommandData.DataType.FACE_DIRECTION,
            Model_EventCommandData.DataType.ITEM,
            Model_EventCommandData.DataType.MAP,
            Model_EventCommandData.DataType.MUSIC,
            Model_EventCommandData.DataType.SOUND,
        ):
            value = source[self.readOffset]
            self.readOffset += 1

            if dataType == Model_EventCommandData.DataType.CHOICE_COUNT:
                self.m_commandChoiceCount = int(value)

        elif dataType == Model_EventCommandData.DataType.BRANCH_ABSOLUTE:
            self.m_branchAddressLocation = self.readOffset
            self.m_branchType = Model_EventCommandData.DataType.BRANCH_ABSOLUTE
            self.branchAddress = int.from_bytes(source[self.readOffset:self.readOffset + 3], "little")
            self.readOffset += 3

        elif dataType == Model_EventCommandData.DataType.BRANCH_OFFSET:
            raw = source[self.readOffset]
            self.readOffset += 1
            value = raw - 256 if raw >= 0x80 else raw
            self.branchAddress = self.readOffset + value

        elif dataType == Model_EventCommandData.DataType.BRANCH_RELATIVE:
            self.m_branchAddressLocation = self.readOffset
            self.m_branchType = Model_EventCommandData.DataType.BRANCH_RELATIVE

            value = source[self.readOffset] | (source[self.readOffset + 1] << 8)
            self.readOffset += 2

            if (self.id == 0x2C0) and value == 0:
                self.branchAddress = self.readOffset
                self.type = Model_EventCommandData.CommandType.CONDITION_TRUE_ONLY
            else:
                self.branchAddress = (self.readOffset & 0xFF0000) + value

            if self.type == Model_EventCommandData.CommandType.MULTIPLE_CONDITION:
                self.m_multipleConditionCount += 1
                self.m_multipleConditionAddresses.append(self.branchAddress)
                self.m_multipleConditionNames.append(f"CASE -> {name}")

        elif dataType == Model_EventCommandData.DataType.MAP_POSITION:
            map_position = (source[self.readOffset] & 0xF0) >> 4
            self.readOffset += 1
            map_position += source[self.readOffset] * 16
            self.readOffset += 1
            value = map_position

        elif dataType == Model_EventCommandData.DataType.MAP_POSITION_OFFSET:
            value = source[self.readOffset] & 0x0F
            self.readOffset += 1

        elif dataType == Model_EventCommandData.DataType.SPRITE_INDEX:
            value = source[self.readOffset] & 0x7F
            self.readOffset += 1

        elif dataType == Model_EventCommandData.DataType.MESSAGE_BOX:
            text_address = (self.readOffset & 0xFF0000) + (source[self.readOffset] | (source[self.readOffset + 1] << 8))
            self.readOffset += 2
            #value = self.readTextBoxSequence(source, text_address)

        elif dataType == Model_EventCommandData.DataType.MESSAGE_BOX_CHOICE:
            self.branchAddress = (self.readOffset & 0xFF0000) + (source[self.readOffset] | (source[self.readOffset + 1] << 8))
            self.readOffset += 2

        elif dataType == Model_EventCommandData.DataType.MESSAGE_BOX_LONG:
            text_address = int.from_bytes(source[self.readOffset:self.readOffset + 3], "little")
            self.readOffset += 3
            #value = self.readTextBoxSequence(source, text_address)

        elif dataType == Model_EventCommandData.DataType.SBYTE:
            raw = source[self.readOffset]
            self.readOffset += 1
            value = raw - 256 if raw >= 0x80 else raw

        elif dataType in (
            Model_EventCommandData.DataType.MAP_REARRANGEMENT_LONG_SWITCH,
            Model_EventCommandData.DataType.RAM_ADDRESS,
            Model_EventCommandData.DataType.SHORT,
        ):
            value = source[self.readOffset] | (source[self.readOffset + 1] << 8)
            self.readOffset += 2

        return value
    
    def get_branch_address(self):
        return self.branchAddress

    def get_type(self):
        return self.type
        