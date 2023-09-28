from tkinter import *

root = Tk()

# eliminate tear-off menus as they're not a part of any modern user interface style
root.option_add('*tearOff', FALSE)

menubar = Menu(root)
root['menu'] = menubar

menu_file = Menu(menubar)
menu_edit = Menu(menubar)
menubar.add_cascade(menu=menu_file, label='File')
menubar.add_cascade(menu=menu_edit, label='Edit')

root.wm_title("GaiaTheCreator")

root.mainloop()

