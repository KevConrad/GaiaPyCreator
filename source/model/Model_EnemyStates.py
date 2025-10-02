
from model.Model_EnemyState import Model_EnemyState

class Model_EnemyStates:
    DATA_ENTRY_SIZE = 4

    def __init__(self, romData, projectData : dict) -> None:
        self.romData = romData

        # read the map event data
        enemyTableAddress = int(str(projectData['DataTables']['EnemyStateDataTable']['Address']), 16)
        enemyTableSize = int(projectData['DataTables']['EnemyStateDataTable']['Size'], base=16)
        enemyTableSize = int(float(enemyTableSize / self.DATA_ENTRY_SIZE))
        enemies = projectData['DataTables']['EnemyStateDataTable']['Enemies']
        
        # read the enemy names
        self.enemyNames = []
        for enemy in enemies:
            self.enemyNames.append(enemy['Name'])

        # read the enemy data
        self.enemies = []
        for enemyIndex in range (enemyTableSize):
            enemyAddress = enemyTableAddress + (enemyIndex * self.DATA_ENTRY_SIZE)
            self.enemies.append(Model_EnemyState(self.romData, enemyAddress))
    