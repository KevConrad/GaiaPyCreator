from model.Model_Spriteset import Model_Spriteset

class Model_Spritesets:
    def __init__(self, romData, projectData : dict) -> None:
        self.romData = romData

        # read all tilemap data initially
        spritesets = projectData['Spritesets']
        self.spritesets = []

        for spriteset in spritesets:
            spritesetData = Model_Spriteset(self.romData, spriteset)
            self.spritesets.append(spritesetData)
    