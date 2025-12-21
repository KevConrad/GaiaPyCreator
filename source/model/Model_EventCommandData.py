from enum import Enum

import json

class Model_EventCommandData:
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
        TEXT_WINDOW = 15
        MESSAGE_BOX_CHOICE = 16
        TEXT_WINDOW_LONG = 17
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
    _TYPE_MAPPING = {
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
        'textWindow': DataType.TEXT_WINDOW,
        'messageBoxChoice': DataType.MESSAGE_BOX_CHOICE,
        'textWindowLong': DataType.TEXT_WINDOW_LONG,
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
        for command in self.data['eventCommands']:
            checkCommandId = int(str(command['id']), 16)
            if checkCommandId == commandId:
                return command
        return None
    
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
        if typeString not in Model_EventCommandData._TYPE_MAPPING:
            raise ValueError(f"Unknown data type: '{typeString}'")
        
        return Model_EventCommandData._TYPE_MAPPING[typeString]
