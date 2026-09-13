
from nicegui import ui
        
class View_Tabs:
    def __init__(self):
        with ui.expansion('Events', icon='work').classes('w-full') as self.expansion_events:
            pass
        with ui.expansion('Items', icon='inventory').classes('w-full') as self.expansion_items:
            pass
        with ui.expansion('Maps', icon='map').classes('w-full') as self.expansion_maps:
            pass
        with ui.expansion('Misc', icon='settings').classes('w-full') as self.expansion_misc:
            pass
        with ui.expansion('Sprites', icon='image').classes('w-full') as self.expansion_sprites:
            pass
        with ui.expansion('Tilemaps', icon='grid_view').classes('w-full') as self.expansion_tilemaps:
            pass
        with ui.expansion('Tilesets', icon='grid_on').classes('w-full') as self.expansion_tilesets:
            pass
