from pubsub import pub

print('pubsub API version', pub.VERSION_API)

# notification
from pubsub.utils.notification import useNotifyByWriteFile
import sys

import os
import re

class Model_ProjectData:
    def __init__(self) -> None:
        pub.subscribe(self.saveProjectPath, "project_save")
    
    def saveProjectPath(self, projectPath):
        extractProjectNamePattern = '[\w-]+?(?=\.)'
        self.projectName = re.search(extractProjectNamePattern, projectPath).group()
        print("Saved project name: " + self.projectName)
        self.projectPath = os.path.dirname(projectPath)
        print("Saved project path: " + self.projectPath)