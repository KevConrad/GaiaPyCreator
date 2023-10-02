from pubsub import pub

# notification
from pubsub.utils.notification import useNotifyByWriteFile
import sys

from model.Model_RomData import Model_RomData

class Controller_Project:
    def __init__(self) -> None:
        self.romData = Model_RomData()

    def close():
        pub.sendMessage("project_closed")

    def create():
        pub.sendMessage("project_created")

    def open():
        pub.sendMessage("project_opened")