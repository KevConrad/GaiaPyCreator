
from model.Model_RoomClearingReward import RoomClearingReward

class Model_RoomClearingRewards:
    def __init__(self, romData, projectData : dict) -> None:
        self.romData = romData

        # read the room clearing rewards data table data from the project file
        roomClearingRewardsTableAddress = int(str(projectData['DataTables']['RoomClearingRewardTable']['Address']), 16)
        roomClearingRewardsTableSize = int(projectData['DataTables']['RoomClearingRewardTable']['Size'], base=16)

        # read the room clearing rewards data
        self.roomClearingRewards = []
        for roomClearingRewardIndex in range (roomClearingRewardsTableSize):
            roomClearingRewardAddress = roomClearingRewardsTableAddress + roomClearingRewardIndex
            self.roomClearingRewards.append(RoomClearingReward(self.romData, roomClearingRewardAddress))
    