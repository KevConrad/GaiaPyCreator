
from model.Model_Compression import Model_Compression
from model.Model_Sprite import Model_Sprite
from model.Model_SpriteFrame import Model_SpriteFrame
from model.Model_Tilesets import Model_Tilesets
from model.Model_Tileset import Model_Tileset

import bitstring

class Model_Spriteset:
    SPRITE_ADDRESS_OFFSET = 0x4000

    def __init__(self, romData, sprite : dict, tilesets:Model_Tilesets) -> None:
        self.romData = romData
        self.tilesets = tilesets

        # read the data from the JSON file
        self.address = int(str(sprite['Address']), 16)
        self.compressed = int(str(sprite['Compressed']), 16)
        self.name = str(sprite['Name'])
        self.palettesetAddress = int(str(sprite['Palette']), 16)
        self.tileset1Address = int(str(sprite['Tileset1']), 16)
        self.tileset1Index = self.tilesets.getIndexfromAddress(self.tileset1Address)
        self.tileset2Address = int(str(sprite['Tileset2']), 16)
        self.tileset2Index = self.tilesets.getIndexfromAddress(self.tileset2Address)

        # read the sprites
        sprites = sprite['Sprites']
        self.sprites = []
        self.spriteNames = []

        for sprite in sprites:
            spriteData = Model_Sprite(self.romData, sprite)
            self.sprites.append(spriteData)
            self.spriteNames.append(spriteData.name)

    def read(self):
        # read tileset1 data
        if self.tilesets.tilesets[self.tileset1Index].compSize > 0:
            # decompress the compressed tileset data (increment length of compressed data to prevent data truncation)
            self.tileset1Data, self.tileset1CompSize = Model_Compression.decompress(self.romData, self.tileset1Address, 0)
        else:
            self.tileset1Data = self.romData[self.tileset1Address:self.tileset1Address + self.tilesets.tilesets[self.tileset1Index].decompSize]

        # read tileset2 data
        if self.tilesets.tilesets[self.tileset2Index].compSize > 0:
            # decompress the compressed tileset data (increment length of compressed data to prevent data truncation)
            self.tileset2Data, self.tileset2CompSize = Model_Compression.decompress(self.romData, self.tileset2Address, 0)
        else:
            self.tileset2Data = self.romData[self.tileset2Address:self.tileset2Address + self.tilesets.tilesets[self.tileset2Index].decompSize]
        
        # create array which contains the data of both tilesets used by the map
        self.tilesetBits = []
        self.tilesetBits.append(bitstring.ConstBitStream(bytes = self.tileset1Data, offset=0,
                                                         length=Model_Tileset.TILESET_BYTE_SIZE * 8))
        self.tilesetBits.append(bitstring.ConstBitStream(bytes = self.tileset2Data, offset=0,
                                                         length=Model_Tileset.TILESET_BYTE_SIZE * 8))
            
        # read the sprite data from the ROM
        if self.compressed != 0:
            # read the compressed sprite data
            self.spriteData, self.compSize = Model_Compression.decompress(self.romData, self.address, 0)
        else:
            self.spriteData = self.romData

        # read the sprite data of all sprites
        for spriteIndex in range (len(self.sprites)):
            # get the sprite data address
            if self.compressed:
                addressSpritePointer = spriteIndex * 2
                addressSpriteData = (self.spriteData[addressSpritePointer + 1] * 256) + self.spriteData[addressSpritePointer]
                addressSpriteData -= self.SPRITE_ADDRESS_OFFSET
            else:
                addressSpritePointer = self.address + (spriteIndex * 2)
                addressSpriteData = (self.address & 0xFF0000) + (self.romData[addressSpritePointer + 1] << 8) + self.romData[addressSpritePointer]
            
            # read the sprite data
            self.sprites[spriteIndex].read(self.spriteData, addressSpriteData, self.compressed)

        self.spriteFrames = []
        for spriteIndex in range (len(self.sprites)):
            for spriteFrameDataIndex in range (len(self.sprites[spriteIndex].frameData)):
                # check if the sprite frame data is already in the list
                isNewSpriteFrame = True
                spriteFrameId = 0
                for spriteFrameIndex in range (len(self.spriteFrames)):
                    if self.spriteFrames[spriteFrameIndex].address == self.sprites[spriteIndex].frameData[spriteFrameDataIndex].address:
                        isNewSpriteFrame = False
                        spriteFrameId = spriteFrameIndex
                        break

                # if the sprite frame data is not in the list, add it
                if isNewSpriteFrame:
                    spriteFrame = Model_SpriteFrame(self.romData, self.spriteData, self.sprites[spriteIndex].frameData[spriteFrameDataIndex].address, self.palettesetAddress)
                    self.spriteFrames.append(spriteFrame)

                    self.sprites[spriteIndex].frameData[spriteFrameDataIndex].frameId = len(self.spriteFrames) - 1
                else:
                    self.sprites[spriteIndex].frameData[spriteFrameDataIndex].frameId = spriteFrameId
        
    