from pubsub import pub

# notification
from pubsub.utils.notification import useNotifyByWriteFile

from controller.Controller_Project import Controller_Project
from model.Model_Tilesets import Model_Tilesets
from view.View_Main import View_Main

class Controller_Tilesets:
    def __init__(self, project : Controller_Project, view:View_Main) -> None:
        self.project = project
        self.view = view

        self.tilesets = Model_Tilesets(self.project.romData.romData, self.project.projectData.projectData)

        pub.subscribe(self.load, "tilesets_load")
        pub.subscribe(self.update, "tilesets_update")

    def load(self):
        if self.project.isProjectLoaded == True:
            # display the tilesets in the GUI
            self.view.tilesets.load(self.tilesets.tilesetNames)

    def update(self, tilesetIndex):
        self.tilesets.tilesets[tilesetIndex].read()
        tilesetImage = self.tilesets.tilesets[tilesetIndex].getImage(0)
        
        