from pubsub import pub

# notification
from pubsub.utils.notification import useNotifyByWriteFile

import shutil

from model.Model_RomData import Model_RomData
from model.Model_ProjectData import Model_ProjectData
from model.Model_Text import Model_Text
from view.View_Main import View_Main

class Controller_Project:
    def __init__(self, view:View_Main) -> None:
        self.projectData = Model_ProjectData()
        self.romData = Model_RomData()

        self.text = Model_Text(self.romData)
        
        self.view = view

        self.isProjectLoaded = False

        pub.subscribe(self.close, "project_close")
        pub.subscribe(self.load, "project_load")
        pub.subscribe(self.open, "project_open")
        pub.subscribe(self.save, "project_save")

    def close(self):
        self.projectData.close()

        self.isProjectLoaded = False

        # display status message
        self.view.statusBar.pushStatus("No project loaded.")

    def load(self):
        self.projectData.open()

        self.romData.romData = self.projectData.extractRomData()
        
        self.isProjectLoaded = True
        
        # display status message
        self.view.statusBar.pushStatus("Loaded project " + self.projectData.projectName + ".")

    def open(self, projectPath):
        self.projectData.saveProject(projectPath)

        self.load()

    def save(self, projectPath):
        self.projectData.saveProject(projectPath)

        # create and save the project file
        self.createProjectFile()

        pub.sendMessage("project_load")

    def createProjectFile(self):
        # copy the project data file
        sourceFilePath = "../data/Data_Rom.json"
        
        shutil.copy(sourceFilePath, self.projectData.projectFilePath)
        print("Created project file: " + self.projectData.projectFilePath)

        self.projectData.open()

        self.projectData.appendRomData(self.romData.romData)
        print("Appended ROM data to project file")