from enum import Enum

import json

class Model_EventCommandData:
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
        RETURN = 13
    
    # Mapping from JSON string to CommandType enum
    _COMMANDTYPE_MAPPING = {
        'action': CommandType.ACTION,
        'branch': CommandType.BRANCH,
        'call': CommandType.CALL,
        'choice': CommandType.CHOICE,
        'choiceEntry': CommandType.CHOICE_ENTRY,
        'condition': CommandType.CONDITION,
        'conditionTrue': CommandType.CONDITION_TRUE,
        'conditionTrueOnly': CommandType.CONDITION_TRUE_ONLY,
        'conditionFalse': CommandType.CONDITION_FALSE,
        'jump': CommandType.JUMP,
        'leave': CommandType.LEAVE,
        'multipleCondition': CommandType.MULTIPLE_CONDITION,
        'multipleConditionEntry': CommandType.MULTIPLE_CONDITION_ENTRY,
        'return': CommandType.RETURN,
    }

    # enumeration for data types
    class DataType(Enum):
        ABSOLUTE_ADDRESS = 1
        BRANCH_ABSOLUTE = 2
        BRANCH_OFFSET = 3
        BRANCH_RELATIVE = 4
        BOOL = 5
        BYTE = 6
        CHOICE_COUNT = 7
        EVENT_SCRIPT = 8
        FACE_DIRECTION = 9
        ITEM = 10
        MAP = 11
        MAP_POSITION = 12
        MAP_POSITION_OFFSET = 13
        MAP_REARRANGEMENT_LONG_SWITCH = 14
        MESSAGE_BOX = 15
        MESSAGE_BOX_CHOICE = 16
        MESSAGE_BOX_LONG = 17
        MUSIC = 18
        NUMBER = 19
        RAM_ADDRESS = 20
        RAM_ADDRESS_LONG = 21
        SBYTE = 22
        SHORT = 23
        SOUND = 24
        SPRITE_INDEX = 25
        SPRITESET = 26
    
    # Mapping from JSON string to DataType enum
    _DATATYPE_MAPPING = {
        'absoluteAddress': DataType.ABSOLUTE_ADDRESS,
        'branchAbsolute': DataType.BRANCH_ABSOLUTE,
        'branchOffset': DataType.BRANCH_OFFSET,
        'branchRelative': DataType.BRANCH_RELATIVE,
        'bool': DataType.BOOL,
        'byte': DataType.BYTE,
        'choiceCount': DataType.CHOICE_COUNT,
        'eventScript': DataType.EVENT_SCRIPT,
        'faceDirection': DataType.FACE_DIRECTION,
        'item': DataType.ITEM,
        'map': DataType.MAP,
        'mapPosition': DataType.MAP_POSITION,
        'mapPositionOffset': DataType.MAP_POSITION_OFFSET,
        'mapRearrangementLongSwitch': DataType.MAP_REARRANGEMENT_LONG_SWITCH,
        'messageBox': DataType.MESSAGE_BOX,
        'messageBoxChoice': DataType.MESSAGE_BOX_CHOICE,
        'messageBoxLong': DataType.MESSAGE_BOX_LONG,
        'music': DataType.MUSIC,
        'number': DataType.NUMBER,
        'ramAddress': DataType.RAM_ADDRESS,
        'ramAddressLong': DataType.RAM_ADDRESS_LONG,
        'sbyte': DataType.SBYTE,
        'short': DataType.SHORT,
        'sound': DataType.SOUND,
        'spriteIndex': DataType.SPRITE_INDEX,
        'spriteset': DataType.SPRITESET,
    }



    FILE_PATH = '../data/Data_EventCommands.json'

    def __init__(self) -> None:
        self.data = json.load(open(self.FILE_PATH, 'r'))

    def getCommandDataById(self, commandId: int):
        id = None
        name = None
        commandType = None
        dataTypes = None

        for command in self.data['eventCommands']:
            checkCommandId = int(str(command['id']), 16)
            if checkCommandId == commandId:
                id = command['id']
                name = command['name']
                # read command type if it exists, otherwise set to default ACTION
                if 'type' in command:
                    commandType = Model_EventCommandData.convertStringToCommandType(command['type'])
                else:
                    commandType = Model_EventCommandData.CommandType.ACTION

                if 'data' in command:
                    dataTypes = []
                    for data in command['data']:
                        dataType = Model_EventCommandData.convertStringToDataType(data['type'])
                        dataTypes.append(dataType)

                break

        return id, name, commandType, dataTypes

    @staticmethod
    def convertStringToCommandType(typeString: str) -> 'Model_EventCommandData.CommandType':
        """
        Convert a command type string from Data_EventCommands.json to corresponding CommandType enum.
        
        Args:
            typeString: The command type string (e.g., 'action', 'branch', 'call')
            
        Returns:
            The corresponding CommandType enum value
            
        Raises:
            ValueError: If the type string is not recognized
        """
        print("typeString:", typeString)
        if typeString not in Model_EventCommandData._COMMANDTYPE_MAPPING:
            raise ValueError(f"Unknown command type: '{typeString}'")
        
        return Model_EventCommandData._COMMANDTYPE_MAPPING[typeString]
    
    @staticmethod
    def convertStringToDataType(typeString: str) -> 'Model_EventCommandData.DataType':
        """
        Convert a data type string from Data_EventCommands.json to corresponding DataType enum.
        
        Args:
            typeString: The data type string (e.g., 'music', 'byte', 'mapPosition')
            
        Returns:
            The corresponding DataType enum value
            
        Raises:
            ValueError: If the type string is not recognized
        """
        if typeString not in Model_EventCommandData._DATATYPE_MAPPING:
            raise ValueError(f"Unknown data type: '{typeString}'")
        
        return Model_EventCommandData._DATATYPE_MAPPING[typeString]
