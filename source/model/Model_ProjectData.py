import os
import re

class Model_ProjectData:
    def __init__(self) -> None:
        pass
    
    def saveProject(self, projectPath):
        extractProjectNamePattern = '[\w-]+?(?=\.)'
        self.projectName = re.search(extractProjectNamePattern, projectPath).group()
        print("Saved project name: " + self.projectName)

        self.projectPath = os.path.dirname(projectPath)
        print("Saved project path: " + self.projectPath)

        self.projectFilePath = self.projectPath + "/" + self.projectName + ".json"