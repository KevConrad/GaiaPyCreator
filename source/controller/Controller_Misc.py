from pubsub import pub

# notification
from pubsub.utils.notification import useNotifyByWriteFile

from controller.Controller_Project import Controller_Project
from model.Model_EnemyStates import Model_EnemyStates
from view.View_Main import View_Main

class Controller_Misc:
    def __init__(self, project : Controller_Project, view:View_Main) -> None:
        self.project = project
        self.view = view

        pub.subscribe(self.load, "misc_load")
        pub.subscribe(self.updateEnemyState, "enemyState_update")

    def load(self):
        if self.project.isProjectLoaded == True:
            self.enemyStates = Model_EnemyStates(self.project.romData.romData, self.project.projectData.projectData)

            self.view.misc.load(self.enemyStates.enemyNames)
            
    def updateEnemyState(self, enemyStateIndex):
        enemyStateData = self.enemyStates.enemies[enemyStateIndex]
        self.view.misc.tabEnemyStates.update(enemyStateData)
