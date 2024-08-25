import sys

class Model_MapDataTable:
    def __init__(self) -> None:
        pass
    
    def load(self, projectData : dict):
        self.mapDataTableAddress = int(str(projectData['DataTables']['MapDataTable']['Address']), 16)
        mapDataTableSize = int(projectData['DataTables']['MapDataTable']['Size'])

        print('MapData.TableAddress: ' + hex(self.mapDataTableAddress))
        print('MapData.TableSize: ' + hex(mapDataTableSize))
