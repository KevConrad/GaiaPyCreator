
class Model_Tile:
    TILE_TYPE_NAMES = ["Pass", "Steps", "Climb Up/Down", "Ramp Down", "Sink Through", "Ramp Left",
                       "Block Diagonal Left", "Climb Left Right", "Jump", "Block Diagonal Right",
                       "Ramp Right", "Unknown0", "Ramp Up", "Unknown1", "Unknown2", "Block"]
    
    TILE_PIECE_COUNT = 4                # number of tile pieces in a tile

    IS_MIRROR_X_BIT_MASK = 0x80         # bit 7 contains the information if tile is mirrored in X direction
    IS_MIRROR_Y_BIT_MASK = 0x40         # bit 6 contains the information if tile is mirrored in X direction
    IS_OVER_PLAYER_BIT_MASK = 0x20      # bit 5 contains the information if tile is over the player
    PALETTE_ID_BIT_MASK = 0x1C          # bits 2-4 contains the palette id
    TILE_TYPE_BIT_MASK = 0x02           # bit 1 contains the tile type information
    TILESET_ID_BIT_MASK = 0x01          # bit 0 contains the tileset id

    def __init__(self, tilemapData, tileIndex, tilePiece):
        tileData = tilemapData[(tileIndex * 8) + (tilePiece * 2) + 1]
        print(str(hex(tileData)))

        # read the palette id
        self.paletteId = (tileData & self.PALETTE_ID_BIT_MASK) >> 2

        # read if tile is above player
        if (tileData & self.IS_OVER_PLAYER_BIT_MASK) != 0:
            self.isOverPlayer = True
        else:
            self.isOverPlayer = False

        # read if tile is mirrored in X direction
        if (tileData & self.IS_MIRROR_X_BIT_MASK) != 0:
            self.isMirroredX = True
        else:
            self.isMirroredX = False

        # read if tile is mirrored in Y direction
        if (tileData & self.IS_MIRROR_Y_BIT_MASK) != 0:
            self.isMirroredY = True
        else:
            self.isMirroredY = False

        # read tileset id
        self.tilesetId = tileData & self.TILESET_ID_BIT_MASK

        # read tile type
        tileTypeRaw = 0
        for tilepieceIndex in range (self.TILE_PIECE_COUNT):
            tileData = tilemapData[(tileIndex * 8) + (tilepieceIndex * 2) + 1]
            if (tileData & self.TILE_TYPE_BIT_MASK) != 0:
                tileTypeRaw |= 1 << tilepieceIndex
        self.type = tileTypeRaw
