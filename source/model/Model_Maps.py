from model.Model_Map import Model_Map

class Model_Maps:
    def __init__(self, romData, projectData : dict, mapDataTable) -> None:
        self.romData = romData

        # read all map data initially
        maps = projectData['Maps']

        # read all tilemap data initially
        tilemaps = projectData['Tilemaps']
        # read all tileset data because it is needed by the tilemaps
        tilesets = projectData['Tilesets']

        self.maps = []
        self.mapNames = []

        mapIndex = 0
        for map in maps:
            mapData = Model_Map(self.romData, map, tilemaps, tilesets, mapDataTable[mapIndex])
            self.maps.append(mapData)
            self.mapNames.append(mapData.name)
            mapIndex += 1
            