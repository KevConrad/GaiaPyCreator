from model.Model_RomData import Model_RomData

class Model_SpriteFrameData:
    SPRITE_ADDRESS_OFFSET = 0x4000

    def __init__(self, spriteData, address, isCompressed) -> None:
        readOffset = address

        # Read the sprite frame duration
        self.duration = Model_RomData.readLittleEndianValue(spriteData, readOffset)
        readOffset += 2

        # Read the sprite frame address
        if isCompressed:
            self.address = Model_RomData.readLittleEndianValue(spriteData, readOffset)
            readOffset += 2
            self.address -= self.SPRITE_ADDRESS_OFFSET
        else:
            self.address = readOffset & 0xFF0000
            self.address = Model_RomData.readLittleEndianValue(spriteData, readOffset)
            readOffset += 2

        self.size = readOffset - address

    