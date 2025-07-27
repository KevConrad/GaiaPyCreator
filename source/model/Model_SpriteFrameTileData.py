
class Model_SpriteFrameTileData:
    def __init__(self, spriteTileData, address) -> None:
        readOffset = address

        # Read the tile sector information
        if spriteTileData[readOffset] == 0:
            self.tileCutout = True
        else:
            self.tileCutout = False
        readOffset += 1

        # Read the tile position offset in x direction
        self.tileOffsetX = spriteTileData[readOffset]
        readOffset += 1

        self.byte1 = spriteTileData[readOffset]
        readOffset += 1

        # Read the tile position offset in y direction
        self.tileOffsetY = spriteTileData[readOffset]
        readOffset += 1

        self.byte2 = spriteTileData[readOffset]
        readOffset += 1

        # Read the tile index
        self.tileIdX = spriteTileData[readOffset] & 0x0F
        self.tileIdY = (spriteTileData[readOffset] & 0xF0) >> 4
        readOffset += 1

        # Read the tile mirror setting
        if (spriteTileData[readOffset] & 0x80) != 0:
            self.tileMirrorX = True
        else:
            self.tileMirrorX = False
        if (spriteTileData[readOffset] & 0x40) != 0:
            self.tileMirrorY = True
        else:
            self.tileMirrorY = False

        # Read the palette index
        self.tilePaletteId = (spriteTileData[readOffset] & 0x0E) >> 1

        # Read the tile passable setting
        if (spriteTileData[readOffset] & 0x20) == 0:
            self.tilePassable = True
        else:
            self.tilePassable = False

        # Read the tileset index
        self.tilesetId = spriteTileData[readOffset] & 0x01
        readOffset += 1

        self.size = readOffset - address



    