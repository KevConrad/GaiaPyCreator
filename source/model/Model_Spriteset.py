
from model.Model_Compression import Model_Compression
from model.Model_Sprite import Model_Sprite

class Model_Spriteset:
    def __init__(self, romData, sprite : dict) -> None:
        self.romData = romData

        # read the data from the JSON file
        self.address = int(str(sprite['Address']), 16)
        self.compressed = int(str(sprite['Compressed']), 16)
        self.name = str(sprite['Name'])
        self.palettesetAddress = int(str(sprite['Palette']), 16)
        self.spriteCount = int(str(sprite['SpriteCount']), 10)
        self.tileset1Address = int(str(sprite['Tileset1']), 16)
        self.tileset2Address = int(str(sprite['Tileset2']), 16)

        # read the sprites
        sprites = sprite['Sprites']
        self.sprites = []
        self.spriteNames = []

        for sprite in sprites:
            spriteData = Model_Sprite(self.romData, sprite)
            self.sprites.append(spriteData)
            self.spriteNames.append(spriteData.name)

    def read(self):
        # read the sprite data from the ROM
        if self.compressed != 0:
            # read the compressed sprite data
            self.spriteData, self.compSize = Model_Compression.decompress(self.romData, self.address, 10000, 0)
    