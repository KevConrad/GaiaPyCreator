from pubsub import pub

# notification
from pubsub.utils.notification import useNotifyByWriteFile

from controller.Controller_Project import Controller_Project
from model.Model_Spritesets import Model_Spritesets
from view.View_Main import View_Main

class Controller_Sprites:
    def __init__(self, project : Controller_Project, view:View_Main) -> None:
        self.project = project
        self.view = view

        self.spritesets = Model_Spritesets(self.project.romData.romData, self.project.projectData.projectData)

        pub.subscribe(self.load, "sprites_load")

    def load(self):
        if self.project.isProjectLoaded == True:
            # display the spritesets in the GUI
            self.view.sprites.load(self.spritesets)

    def update(self, spritesetIndex):
        pass
        