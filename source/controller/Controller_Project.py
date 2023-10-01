from pubsub import pub

print('pubsub API version', pub.VERSION_API)

# notification
from pubsub.utils.notification import useNotifyByWriteFile
import sys

class Controller_Project:
    def __init__(self) -> None:
        pass

    def close():
        pub.sendMessage("project_closed")

    def create():
        pub.sendMessage("project_created")

    def open():
        pub.sendMessage("project_opened")