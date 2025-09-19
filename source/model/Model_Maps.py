from model.Model_Map import Model_Map
from model.Model_MapExits import Model_MapExits
from model.Model_RomDataTable import Model_RomDataTable
from model.Model_ScreenSettings import Model_ScreenSettings
from model.Model_Spritesets import Model_Spritesets

class Model_Maps:
    def __init__(self, romData, projectData : dict, mapDataTable, screenSettings, roomClearingRewards,
                 spritesets:Model_Spritesets) -> None:
        self.romData = romData

        # read all map data initially
        maps = projectData['Maps']
        
        self.maps = []
        self.mapNames = []

        mapIndex = 0
        for map in maps:
            # read the map data
            mapData = Model_Map(self.romData, map, projectData, mapDataTable[mapIndex], mapIndex, screenSettings, roomClearingRewards,
                                spritesets)
            # fill map data that is not set from previous map
            self.copyMapData(mapData, mapIndex)

            self.maps.append(mapData)
            self.mapNames.append(mapData.name)
            
            mapIndex += 1

    def copyMapData(self, mapData, mapIndex):
        if mapIndex > 0:
            # check if sprite data exists
            if len(mapData.mapDataSprites) == 0:
                # copy the sprite data from the previous map
                mapData.mapDataSprites = self.maps[mapIndex - 1].mapDataSprites.copy()
            