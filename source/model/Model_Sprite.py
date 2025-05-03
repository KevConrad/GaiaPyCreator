
class Model_Sprite:
    def __init__(self, romData, sprite : dict) -> None:
        self.romData = romData

        # read the data from the JSON file
        self.name = str(sprite['Name'])

    