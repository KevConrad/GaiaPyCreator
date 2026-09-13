import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from nicegui import ui
from controller.Controller_Main import Controller_Main
from source.view.View_Main import View_Main


if __name__ in {"__main__", "__mp_main__"}:
    controller = Controller_Main()
    #View_Main.create_app()
    ui.run(title='GaiaPyCreator', favicon='🎮', host='127.0.0.1', port=8081, reload=True)



