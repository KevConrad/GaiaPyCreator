import base64
import binascii
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
        projectPath = str(projectPath).strip()

        if os.path.splitext(projectPath)[1].lower() == '.json':
            self.projectName = os.path.splitext(os.path.basename(projectPath))[0]
            self.projectPath = os.path.dirname(projectPath) or '.'
        else:
            self.projectName = os.path.basename(projectPath) or 'project'
            self.projectPath = projectPath or '.'

        print("Saved project name: " + self.projectName)
        print("Saved project path: " + self.projectPath)

        self.projectFilePath = os.path.join(self.projectPath, self.projectName + ".json")

    def appendRomData(self, romData):
        # convert the ROM data byte array to a string to store it in the JOSN project file
        romDataHex = binascii.hexlify(romData)
        romDataString = romDataHex.decode('utf-8')
        self.projectData['romData'] = romDataString

        # serialize the json dict to write it to the project file
        jsonData = json.dumps(self.projectData, indent=4)
        
        with open(self.projectFilePath, "w") as outfile:
            outfile.write(jsonData)

    def extractRomData(self):
        # read the ROM data string from the project file and convert it to a byte array
        romDataString = self.projectData['romData']
        romData = binascii.unhexlify(romDataString.encode('utf-8'))

        return romData
