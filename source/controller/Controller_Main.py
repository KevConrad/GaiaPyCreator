import wx

from pubsub import pub

# notification
from pubsub.utils.notification import useNotifyByWriteFile
import sys

from .Controller_Items import Controller_Items

useNotifyByWriteFile(sys.stdout)

# the following two modules don't know about each other yet will
# exchange data via pubsub:
from controller.Controller_Project import Controller_Project
from model.Model_Text import Model_Text
from view.View_Main import View_Main

class Controller_Main:
    def __init__(self):
        self.view = View_Main()

        self.view.Show()

        self.project = Controller_Project(self.view)

        pub.subscribe(self.load, "project_loaded")

    def load(self):
        self.text = Model_Text()
        self.items = Controller_Items(self.project, self.view)
        print(self.project.romData.romData[8])
        print("Initialized all objects")
        
        