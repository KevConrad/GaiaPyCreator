from pubsub import pub

# notification
from pubsub.utils.notification import useNotifyByWriteFile
import sys

from model.Model_RomData import Model_RomData
from model.Model_ProjectData import Model_ProjectData

class Controller_Project:
    def __init__(self) -> None:
        self.projectData = Model_ProjectData()
        self.romData = Model_RomData()

        pub.subscribe(self.save, "project_save")


    def close():
        pub.sendMessage("project_closed")

    def create():
        pub.sendMessage("project_created")

    def open():
        pub.sendMessage("project_opened")

    def save(self, projectPath):
        pass