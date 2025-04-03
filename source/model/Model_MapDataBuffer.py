from model.Model_MapDataPalette import Model_MapDataPalette
from model.Model_MapDataTilemap import Model_MapDataTilemap
from model.Model_MapDataTileset import Model_MapDataTileset

import copy

class Model_MapDataBuffer:
    def __init__(self, romData) -> None:
        self.paletteBuffer = []
        for bufferIndex in range (2):
            self.paletteBuffer.append(Model_MapDataPalette(romData, 0))

        self.tilemapBuffer = []
        self.tilesetBuffer = []
        for bufferIndex in range (3):
            self.tilemapBuffer.append(Model_MapDataTilemap(romData, 0))
            self.tilesetBuffer.append(Model_MapDataTileset(romData, 0))

    def setPaletteBuffer(self, palette : Model_MapDataPalette):
        if palette.layer == Model_MapDataPalette.MAP_LAYER:
            self.paletteBuffer[0] = copy.deepcopy(palette)
        else:
            self.paletteBuffer[1] = copy.deepcopy(palette)  

    def setTilemapBuffer(self, tilemap : Model_MapDataTilemap):
        if tilemap.slotId > 0:
            self.tilemapBuffer[tilemap.slotId - 1] = copy.deepcopy(tilemap)

    def setTilesetBuffer(self, tileset : Model_MapDataTileset):
        if tileset.layer == Model_MapDataTileset.LAYER_BG1:
            self.tilesetBuffer[0] = copy.deepcopy(tileset)

        elif tileset.layer == Model_MapDataTileset.LAYER_BG2:
            self.tilesetBuffer[1] = copy.deepcopy(tileset)

        elif tileset.layer == Model_MapDataTileset.LAYER_BG1_BG2:
            self.tilesetBuffer[0] = copy.deepcopy(tileset)
            tileset.index += + 1
            tileset.layer = Model_MapDataTileset.LAYER_BG2
            self.tilesetBuffer[1] = copy.deepcopy(tileset)

        elif tileset.layer == Model_MapDataTileset.LAYER_SPRITES:
            self.tilesetBuffer[2] = copy.deepcopy(tileset)