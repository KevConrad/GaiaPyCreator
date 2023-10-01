import wx

from pubsub import pub

print('pubsub API version', pub.VERSION_API)

# notification
from pubsub.utils.notification import useNotifyByWriteFile
import sys

from controller.Controller_Main import Controller_Main
from view.View_Main import View_Main

useNotifyByWriteFile(sys.stdout)

if __name__ == "__main__":
    app = wx.App()

    controller = Controller_Main()

    sys.stdout = sys.__stdout__

    print('---- Starting main event loop ----')
    app.MainLoop()
    print('---- Exited main event loop ----')

