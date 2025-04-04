
from model.Model_MapData import Model_MapData
from model.Model_RomDataTable import Model_RomDataTable
from model.Model_ScreenSetting import Model_ScreenSetting

class Model_ScreenSettings:
    def __init__(self, romData, projectData : dict) -> None:
        self.romData = romData

        # read the map event data
        screenSettingsTableAddress = int(str(projectData['DataTables']['ScreenSettingTable']['Address']), 16)
        screenSettingsTableSize = int(projectData['DataTables']['ScreenSettingTable']['Size'], base=16)
        screenSettingsDataTable = Model_RomDataTable(self.romData, screenSettingsTableAddress, screenSettingsTableSize)  
        self.screenSettings = []
        for screenSettingIndex in range (screenSettingsTableSize):
            screenSettingAddress = screenSettingsDataTable.getDataAddress(screenSettingIndex)
            self.screenSettings.append(Model_ScreenSetting(self.romData, screenSettingAddress))
    