import wx

from pubsub import pub

# notification
from pubsub.utils.notification import useNotifyByWriteFile
import sys

from .Controller_Items import Controller_Items
from .Controller_Maps import Controller_Maps
from .Controller_Tilemaps import Controller_Tilemaps
from .Controller_Tilesets import Controller_Tilesets

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
        self.text = Model_Text()

        pub.subscribe(self.load, "project_loaded")

    def load(self):
        # initialize all controllers
        self.items = Controller_Items(self.project, self.view)

        # initialize and load the map data
        self.maps = Controller_Maps(self.project, self.view)
        self.maps.load()

        self.tilemaps = Controller_Tilemaps(self.project, self.view)
        self.tilesets = Controller_Tilesets(self.project, self.view)

        print("Initialized all objects")
        
        