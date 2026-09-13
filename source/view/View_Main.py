import wx

from pubsub import pub

from nicegui import ui

# notification
from pubsub.utils.notification import useNotifyByWriteFile
import sys

useNotifyByWriteFile(sys.stdout)

#from .View_Events import View_Events
from .View_Items import View_Items
#from .View_Maps import View_Maps
from .View_MenuBar import View_MenuBar
#from .View_Misc import View_Misc
#from .View_Sprites import View_Sprites
#from .View_StatusBar import View_StatusBar
from .View_Tabs import View_Tabs
#from .View_Tilemaps import View_Tilemaps
#from .View_Tilesets import View_Tilesets

class View_Main(wx.Frame):
    def __init__(self, parent=None) -> None:
        self.create_app()

        self.menuBar = View_MenuBar()
        #self.statusBar = View_StatusBar(self)
        self.tabs = View_Tabs()
        #self.events = View_Events(self, self.tabs.notebook)
        self.items = View_Items(self.tabs.expansion_items)
        #self.maps = View_Maps(self, self.tabs.notebook)
        #self.misc = View_Misc(self, self.tabs.notebook)
        #self.sprites = View_Sprites(self, self.tabs.notebook)
        #self.tilemaps = View_Tilemaps(self, self.tabs.notebook)
        #self.tilesets = View_Tilesets(self, self.tabs.notebook)

    def create_app(self) -> None:
        ui.page_title('GaiaPyCreator')

        with ui.column().classes('w-full max-w-7xl mx-auto p-6 gap-4'):
            with ui.card().classes('w-full bg-white shadow-lg'):
                ui.label('Illusion of Gaia editor').classes('text-3xl font-bold text-slate-900')
                ui.label('A NiceGUI dashboard for the GaiaPyCreator ROM editor project.')

        ui.notify('GaiaPyCreator dashboard loaded', position='bottom-right', timeout=2000)
