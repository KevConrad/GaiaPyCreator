from pubsub import pub

# notification
from pubsub.utils.notification import useNotifyByWriteFile

import shutil

from model.Model_RomData import Model_RomData
from model.Model_ProjectData import Model_ProjectData
from view.View_Main import View_Main

class Controller_Project:
    def __init__(self, view:View_Main) -> None:
        self.projectData = Model_ProjectData()
        self.romData = Model_RomData()
        
        self.view = view

        pub.subscribe(self.save, "project_save")

    def close():
        pub.sendMessage("project_closed")

    def create():
        pub.sendMessage("project_created")

    def open():
        pub.sendMessage("project_opened")

    def save(self, projectPath):
        self.projectData.saveProject(projectPath)

        # create and save the project file
        self.createProjectFile()

        # display status message
        self.view.statusBar.pushStatus("Loaded project " + self.projectData.projectName + ".")

    def createProjectFile(self):
        # copy the project data file
        sourceFilePath = "../data/Data_Rom.json"
        
        shutil.copy(sourceFilePath, self.projectData.projectFilePath)
        print("Created project file: " + self.projectData.projectFilePath)