
from model.Model_SpriteFrameTileData import Model_SpriteFrameTileData

class Model_SpriteFrame:
    def __init__(self, spriteData, address) -> None:
        readOffset = address
        self.address = address

        self.offsetX = spriteData[readOffset]
        readOffset += 1
        self.frameByte0 = spriteData[readOffset]
        readOffset += 1
        self.offsetY = spriteData[readOffset]
        readOffset += 1
        self.frameByte1 = spriteData[readOffset]
        readOffset += 1
        self.frameByte2 = spriteData[readOffset]
        readOffset += 1
        self.frameByte3 = spriteData[readOffset]
        readOffset += 1
        self.frameByte4 = spriteData[readOffset]
        readOffset += 1
        self.frameByte5 = spriteData[readOffset]
        readOffset += 1
        self.frameByte6 = spriteData[readOffset]
        readOffset += 1
        self.frameByte7 = spriteData[readOffset]
        readOffset += 1
        self.frameByte8 = spriteData[readOffset]
        readOffset += 1
        self.frameByte9 = spriteData[readOffset]
        readOffset += 1
        tileCount = spriteData[readOffset]
        readOffset += 1

        # Read the tile data
        self.tileData = []
        for tileIndex in range (tileCount):
            tileData = Model_SpriteFrameTileData(spriteData, readOffset)
            self.tileData.append(tileData)
            readOffset += tileData.size

        self.size = readOffset - address



    