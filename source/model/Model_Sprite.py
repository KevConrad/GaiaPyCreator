
from model.Model_SpriteFrameData import Model_SpriteFrameData

class Model_Sprite:
    SPRITE_DELIMITER = 0xFF

    def __init__(self, romData, sprite : dict) -> None:
        self.romData = romData

        # read the data from the JSON file
        self.name = str(sprite['Name'])

    def read(self, spriteData, address, isCompressed):
        # read the sprite frame data
        self.frameData = []
        while (spriteData[address] != self.SPRITE_DELIMITER) or \
              (spriteData[address + 1] != self.SPRITE_DELIMITER):
            # Add a new sprite frame to the list
            frameData = Model_SpriteFrameData(spriteData, address, isCompressed)
            self.frameData.append(frameData)

            address += frameData.size

            

    