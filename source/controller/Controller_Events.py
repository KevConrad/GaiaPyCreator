from pubsub import pub

# notification
from pubsub.utils.notification import useNotifyByWriteFile

from controller.Controller_Project import Controller_Project
from model.Model_EventCommandData import Model_EventCommandData
from model.Model_EventScript import Model_EventScript
from view.View_Main import View_Main

class Controller_Events:
    def __init__(self, project : Controller_Project, view:View_Main) -> None:
        self.project = project
        self.romData = project.romData.romData
        self.view = view

        self.eventCommandData = Model_EventCommandData()

        pub.subscribe(self.load, "events_load")
        pub.subscribe(self.saveEventsList, "events_list_created")
        pub.subscribe(self.read, "events_read")

    def load(self):
        if self.project.isProjectLoaded == True:
            # display the events in the GUI
            self.view.events.load(self.eventList)

    def read(self, eventIndex):
        eventAddress = self.eventList[eventIndex]

        eventScript = Model_EventScript(self.romData, eventAddress, self.eventCommandData)

        return eventScript

    def saveEventsList(self, eventList):
        self.eventList = eventList

    def updateEvent(self, eventIndex):
        self.eventIndex = eventIndex
        