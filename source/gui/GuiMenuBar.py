from tkinter import *
from tkinter import filedialog as fd

class GuiMenuBar:
    def __init__(self, root):
        # eliminate tear-off menus as they're not a part of any modern user interface style
        root.option_add('*tearOff', FALSE)

        menubar = Menu(root)
        root['menu'] = menubar

        menu_file = Menu(menubar)
        menu_edit = Menu(menubar)
        menubar.add_cascade(menu=menu_file, label='Project')
        menubar.add_cascade(menu=menu_edit, label='Edit')

        menu_file.add_command(label='Create...', command=self.createNewProject)
        menu_file.add_command(label='Open...', command=self.openProject)

    def createNewProject():
        filetypes = (
            ('ROM file (SFC format)', '*.sfc'),
            ('ROM file (SMC format)', '*.smc')
        )

        filename = fd.askopenfilename(
            title='Open Illusion of Gaia ROM file',
            initialdir='/',
            filetypes=filetypes)
        return

    def openProject():
        filetypes = (
            ('GaiaTheCreator project file', '*.gtc'),
        )

        filename = fd.askopenfilename(
            title='Open GaiaTheCreator project file',
            initialdir='/',
            filetypes=filetypes)
        return

