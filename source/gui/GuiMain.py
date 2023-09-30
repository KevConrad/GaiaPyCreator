from tkinter import *

from .GuiMenuBar import GuiMenuBar

class GuiMain:
    def __init__(self) -> None:
        root = Tk()

        menubar = GuiMenuBar(root)

        root.wm_title("GaiaTheCreator")

        root.mainloop()


