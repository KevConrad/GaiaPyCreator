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

        self.tilesets = Model_Tilesets(self.project.romData.romData)

        pub.subscribe(self.load, "tilesets_load")

    def load(self):
        if self.project.isProjectLoaded == True:
            # load the item data from the project file
            self.tilesets.load(self.project.projectData.projectData)

            # display the tilesets in the GUI
            self.view.tilesets.load(self.tilesets.tilesetNames)
        