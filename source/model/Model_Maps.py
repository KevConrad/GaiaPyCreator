from model.Model_Map import Model_Map
from model.Model_MapExits import Model_MapExits
from model.Model_RomDataTable import Model_RomDataTable

class Model_Maps:
    def __init__(self, romData, projectData : dict, mapDataTable) -> None:
        self.romData = romData

        # read all map data initially
        maps = projectData['Maps']

        exitDataTableAddress = int(str(projectData['DataTables']['MapExitTable']['Address']), 16)
        exitDataTableSize = int(projectData['DataTables']['MapExitTable']['Size'], base=16)
        exitDataTable = Model_RomDataTable(self.romData, exitDataTableAddress, exitDataTableSize)  
        
        # read all tilemap data initially
        tilemaps = projectData['Tilemaps']
        # read all tileset data because it is needed by the tilemaps
        tilesets = projectData['Tilesets']

        self.maps = []
        self.mapExits = []
        self.mapNames = []

        mapIndex = 0
        for map in maps:
            # read the map data
            mapData = Model_Map(self.romData, map, tilemaps, tilesets, mapDataTable[mapIndex])
            self.maps.append(mapData)
            self.mapNames.append(mapData.name)

            # TODO read the map event data

            # read the map exit data
            self.mapExits.append(Model_MapExits(self.romData, exitDataTable.getDataAddress(mapIndex)))
            
            mapIndex += 1
            