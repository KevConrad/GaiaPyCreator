import json
import os
import re

class Model_ProjectData:
    def __init__(self) -> None:
        pass

    def close(self):
        # close JSON project file
        self.projectFile.close()

    def open(self):
        # open JSON project file
        self.projectFile = open(self.projectFilePath)

        # save JSON object as a dictionary
        self.projectData = json.load(self.projectFile)

        if 'GaiaTheCreator' in self.projectData:
            self.projectData = self.projectData['GaiaTheCreator']

        print("Loaded project file " + self.projectFilePath + ".")
    
    def saveProject(self, projectPath):
        extractProjectNamePattern = '[\w-]+?(?=\.)'
        self.projectName = re.search(extractProjectNamePattern, projectPath).group()
        print("Saved project name: " + self.projectName)

        self.projectPath = os.path.dirname(projectPath)
        print("Saved project path: " + self.projectPath)

        self.projectFilePath = self.projectPath + "/" + self.projectName + ".json"