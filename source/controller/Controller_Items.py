from pubsub import pub

# notification
from pubsub.utils.notification import useNotifyByWriteFile

from controller.Controller_Project import Controller_Project
from model.Model_Items import Model_Items
from model.Model_RomData import Model_RomData
from model.Model_ProjectData import Model_ProjectData
from view.View_Items import View_Items
from view.View_Main import View_Main

class Controller_Items:
    def __init__(self, project:Controller_Project, view:View_Main) -> None:
        self.project = project
        self.view = view

        self.items = Model_Items()

        pub.subscribe(self.load, "items_load")

    def load(self):
        if self.project.isProjectLoaded == True:
            # load the item data from the project file
            self.items.load(self.project.projectModel.projectData)

            # display the items in the GUI
            self.view.items.load(self.items.itemNames)
        