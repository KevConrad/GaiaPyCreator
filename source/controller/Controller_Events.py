from pubsub import pub

# notification
from pubsub.utils.notification import useNotifyByWriteFile

from controller.Controller_Project import Controller_Project
from view.View_Main import View_Main

class Controller_Events:
    def __init__(self, project : Controller_Project, view:View_Main) -> None:
        self.project = project
        self.view = view

        pub.subscribe(self.load, "events_load")
        pub.subscribe(self.saveEventsList, "events_list_created")

    def load(self):
        if self.project.isProjectLoaded == True:
            # display the events in the GUI
            self.view.events.load(self.eventList)

    def saveEventsList(self, eventList):
        self.eventList = eventList

    def updateEvent(self, eventIndex):
        self.eventIndex = eventIndex
        