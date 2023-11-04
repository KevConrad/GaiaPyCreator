import base64
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

        self.close()

        print("Loaded project file " + self.projectFilePath + ".")
    
    def saveProject(self, projectPath):
        extractProjectNamePattern = '[\w-]+?(?=\.)'
        self.projectName = re.search(extractProjectNamePattern, projectPath).group()
        print("Saved project name: " + self.projectName)

        self.projectPath = os.path.dirname(projectPath)
        print("Saved project path: " + self.projectPath)

        self.projectFilePath = self.projectPath + "/" + self.projectName + ".json"

    def appendRomData(self, romData):
        # convert the ROM data byte array to a string to store it in the JOSN project file
        romDataString = str(romData)
        romDataBase64String = base64.b64encode(romDataString.encode('utf-8'))
        self.projectData['romData'] = romDataBase64String.decode('ascii')

        # Serializing json
        jsonData = json.dumps(self.projectData, indent=4)
        
        with open(self.projectFilePath, "w") as outfile:
            outfile.write(jsonData)
