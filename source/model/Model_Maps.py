from model.Model_Map import Model_Map

class Model_Maps:
    def __init__(self, romData, projectData : dict) -> None:
        self.romData = romData

        # read all map data initially
        maps = projectData['Maps']

        # read all tilemap data initially
        tilemaps = projectData['Tilemaps']
        # read all tileset data because it is needed by the tilemaps
        tilesets = projectData['Tilesets']

        self.maps = []
        self.mapNames = []

        for map in maps:
            mapData = Model_Map(self.romData, map, tilemaps, tilesets)
            self.maps.append(mapData)
            self.mapNames.append(mapData.name)
            