
class Model_SpriteFrameData:
    SPRITE_ADDRESS_OFFSET = 0x4000

    def __init__(self, spriteData, address, isCompressed) -> None:
        readOffset = address

        # Read the sprite frame duration
        self.duration = spriteData[readOffset]
        readOffset += 1
        self.duration |= (spriteData[readOffset] << 8)
        readOffset += 1

        # Read the sprite frame address
        if isCompressed:
            self.address = spriteData[readOffset]
            readOffset += 1
            self.address |= (spriteData[readOffset] << 8)
            readOffset += 1
            self.address -= self.SPRITE_ADDRESS_OFFSET
        else:
            self.address = readOffset & 0xFF0000
            self.address |= spriteData[readOffset]
            readOffset += 1
            self.address |= (spriteData[readOffset] << 8)
            readOffset += 1

        self.size = readOffset - address

    