
from model.Model_SpriteFrameTileData import Model_SpriteFrameTileData

class Model_SpriteFrame:
    def __init__(self, spriteData, address) -> None:
        readOffset = address
        self.address = address

        offsetX = spriteData[readOffset]
        readOffset += 1
        frameByte0 = spriteData[readOffset]
        readOffset += 1
        offsetY = spriteData[readOffset]
        readOffset += 1
        frameByte1 = spriteData[readOffset]
        readOffset += 1
        frameByte2 = spriteData[readOffset]
        readOffset += 1
        frameByte3 = spriteData[readOffset]
        readOffset += 1
        frameByte4 = spriteData[readOffset]
        readOffset += 1
        frameByte5 = spriteData[readOffset]
        readOffset += 1
        frameByte6 = spriteData[readOffset]
        readOffset += 1
        frameByte7 = spriteData[readOffset]
        readOffset += 1
        frameByte8 = spriteData[readOffset]
        readOffset += 1
        frameByte9 = spriteData[readOffset]
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



    