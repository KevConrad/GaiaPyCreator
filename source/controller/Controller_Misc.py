from pubsub import pub

# notification
from pubsub.utils.notification import useNotifyByWriteFile

from controller.Controller_Project import Controller_Project
from model.Model_Enemies import Model_Enemies
from model.Model_MapDataTable import Model_MapDataTable
from model.Model_MapData import Model_MapData
from model.Model_MapDataBuffer import Model_MapDataBuffer
from model.Model_Maps import Model_Maps
from model.Model_RoomClearingRewards import Model_RoomClearingRewards
from model.Model_ScreenSettings import Model_ScreenSettings
from model.Model_Spritesets import Model_Spritesets
from model.Model_Tilemaps import Model_Tilemaps
from model.Model_Tilesets import Model_Tilesets
from view.View_Main import View_Main

class Controller_Misc:
    def __init__(self, project : Controller_Project, view:View_Main) -> None:
        self.project = project
        self.view = view

        self.tilemaps = Model_Tilemaps(self.project.romData.romData, self.project.projectData.projectData)

        pub.subscribe(self.load, "misc_load")
        pub.subscribe(self.update, "enemyStates_update")

    def load(self):
        if self.project.isProjectLoaded == True:
            self.enemyStates = Model_Enemies(self.project.romData.romData, self.project.projectData.projectData)

            self.view.misc.load(self.enemyStates.enemyNames)
            
    def update(self, enemyStateIndex):
        enemyStateData = self.enemyStates.enemies[enemyStateIndex]
        self.view.misc.tabEnemyStates.update(enemyStateData)
