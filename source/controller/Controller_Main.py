import wx

from pubsub import pub

# notification
from pubsub.utils.notification import useNotifyByWriteFile
import sys

useNotifyByWriteFile(sys.stdout)

# the following two modules don't know about each other yet will
# exchange data via pubsub:
from .Controller_Project import Controller_Project
from view.View_Main import View_Main

class Controller_Main:
    def __init__(self):
        view = View_Main()

        view.Show()

        self.project = Controller_Project()