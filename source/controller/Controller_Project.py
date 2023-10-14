from pubsub import pub

# notification
from pubsub.utils.notification import useNotifyByWriteFile

import shutil

from model.Model_RomData import Model_RomData
from model.Model_ProjectData import Model_ProjectData
from view.View_Main import View_Main

class Controller_Project:
    def __init__(self, view:View_Main) -> None:
        self.projectModel = Model_ProjectData()
        self.romData = Model_RomData()
        
        self.view = view

        self.isProjectLoaded = False

        pub.subscribe(self.close, "project_close")
        pub.subscribe(self.load, "project_load")
        pub.subscribe(self.open, "project_open")
        pub.subscribe(self.save, "project_save")

    def close(self):
        self.projectModel.close()

        self.isProjectLoaded = False

        # display status message
        self.view.statusBar.pushStatus("No project loaded.")

    def load(self):
        self.projectModel.open()
        
        self.isProjectLoaded = True
        
        # display status message
        self.view.statusBar.pushStatus("Loaded project " + self.projectModel.projectName + ".")

    def open(self, projectPath):
        self.projectModel.saveProject(projectPath)

        self.load()

    def save(self, projectPath):
        self.projectModel.saveProject(projectPath)

        # create and save the project file
        self.createProjectFile()

        pub.sendMessage("project_load")

    def createProjectFile(self):
        # copy the project data file
        sourceFilePath = "../data/Data_Rom.json"
        
        shutil.copy(sourceFilePath, self.projectModel.projectFilePath)
        print("Created project file: " + self.projectModel.projectFilePath)