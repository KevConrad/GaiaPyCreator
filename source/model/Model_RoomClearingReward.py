
class RoomClearingReward:
    ROOM_CLEARING_REWARD_NONE = 0x00
    ROOM_CLEARING_REWARD_POWER = 0x01
    ROOM_CLEARING_REWARD_STRENGTH = 0x02
    ROOM_CLEARING_REWARD_DEFENSE = 0x03

    def __init__(self, romData, address) -> None:
        self.romData = romData

        # read the room clearing reward data
        self.roomClearingReward = romData[address]

    