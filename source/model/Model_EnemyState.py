
class Model_EnemyState:
    def __init__(self, romData, address) -> None:
        self.romData = romData

        # read the enemy data
        self.healthPoints = romData[address]
        address += 1
        self.strength = romData[address]
        address += 1
        self.defense = romData[address]
        address += 1
        self.darkPower = romData[address]
