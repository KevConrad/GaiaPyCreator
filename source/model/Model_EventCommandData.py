
import json

class Model_EventCommandData:
    FILE_PATH = '../data/Data_EventCommands.json'

    def __init__(self) -> None:
        self.data = json.load(open(self.FILE_PATH, 'r'))
