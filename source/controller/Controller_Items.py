from pubsub import pub

# notification
from pubsub.utils.notification import useNotifyByWriteFile

from controller.Controller_Project import Controller_Project
from model.Model_Items import Model_Items
from view.View_Main import View_Main

class Controller_Items:
    def __init__(self, project : Controller_Project, view:View_Main) -> None:
        self.project = project
        self.view = view

        self.items = Model_Items(self.project.romData.romData)

        pub.subscribe(self.load, "items_load")

    def load(self):
        if self.project.isProjectLoaded == True:
            # load the item data from the project file
            self.items.load(self.project.projectData.projectData)

            # display the items in the GUI
            self.view.items.load(self.items.itemNames, self.items.itemDescriptions, self.items.itemIsRemovableFlags,
                                 self.items.itemFindMessages)
        