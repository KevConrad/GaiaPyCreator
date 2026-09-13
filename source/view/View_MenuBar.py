from pathlib import Path

from nicegui import ui
from pubsub import pub


class View_MenuBar:
    def __init__(self):
        self.romPath = ""
        self.projectPath = ""
        self.header = None

        self.header = ui.header().classes('bg-slate-900 text-white shadow-md')
        with self.header:
            with ui.row().classes('items-center gap-2 w-full px-4 py-2'):
                ui.label('GaiaPyCreator').classes('text-lg font-bold mr-4 text-white')

                ui.button('Create', icon='add', on_click=self.createProject).props('flat dense color=white')
                ui.button('Open', icon='folder_open', on_click=self.openProject).props('flat dense color=white')
                ui.button('Close', icon='close', on_click=self.closeProject).props('flat dense color=white')

    def _show_project_menu(self):
        ui.notify('Project menu actions are available from the toolbar buttons.', position='top-right')

    def closeProject(self, parent=None):
        pub.sendMessage("project_close")
        ui.notify('Project closed', position='bottom-right')

    def _make_file_picker(self, path_attr, label, accept, on_selected=None):
        def _handle(event):
            if not event or not getattr(event, 'files', None):
                return
            file = event.files[0]
            selected = str(file.name)
            setattr(self, path_attr, selected)
            
            if on_selected is not None:
                on_selected(selected)

        return ui.upload(label=label, auto_upload=True, on_upload=_handle).props(f'accept={accept}').classes('w-full')

    def _make_directory_picker(self, input_widget, path_attr, label, on_selected=None):
        picker_id = f'project-folder-picker-{id(self)}-{id(input_widget)}'
        file_input = ui.element('input').props(f'type=file webkitdirectory id={picker_id}').style(
            'position: absolute; width: 1px; height: 1px; opacity: 0; pointer-events: none;'
        )

        def _handle(event):
            if not event or not getattr(event, 'args', None):
                return
            selected = str(event.args[0] or '')
            if not selected:
                return
            setattr(self, path_attr, selected)
            input_widget.value = selected
            if on_selected is not None:
                on_selected(selected)

        file_input.on(
            'change',
            handler=_handle,
            js_handler='(event) => { '
                       'const files = event.target.files || []; '
                       'const first = files[0]; '
                       'const folder = first && first.webkitRelativePath ? '
                       'first.webkitRelativePath.split("/")[0] : (first ? first.name : ""); '
                       'emit(folder); '
                       '}'
        )

        def _trigger_picker():
            ui.run_javascript(f"const el = document.getElementById('{picker_id}'); if (el) {{ el.click(); }}")

        return ui.button(label, on_click=_trigger_picker).props('icon=folder_open flat').classes('w-full justify-start')

    def createProject(self, parent=None):
        self.create_dialog = ui.dialog()
        with self.create_dialog, ui.card().classes('w-96'):
            ui.label('Create new project').classes('text-lg font-semibold')

            self._make_file_picker(
                'romPath',
                'Choose ROM',
                '.smc,.sfc,.gb,.gba,.zip',
                lambda selected: pub.sendMessage('rom_opened', romPath=selected),
            )

            self.projectInput = ui.input(label='Project folder', placeholder='Select project folder')
            self._make_directory_picker(
                self.projectInput,
                'projectPath',
                'Choose project folder',
                None,
            )

            with ui.row().classes('justify-end gap-2'):
                ui.button('Cancel', on_click=self.create_dialog.close)
                ui.button('Create', on_click=self._save_project_dialog)

        self.create_dialog.open()

    def _on_rom_upload(self, event):
        if event and getattr(event, 'files', None):
            file = event.files[0]
            self.romPath = str(file.name)
            self.romInput.value = self.romPath
            pub.sendMessage("rom_opened", romPath=self.romPath)

    def _on_project_upload(self, event):
        if event and getattr(event, 'files', None):
            file = event.files[0]
            self.projectPath = str(file.name)
            self.projectInput.value = self.projectPath

    def _save_project_dialog(self):
        if not self.romPath:
            ui.notify('Please select a ROM file first.', color='negative')
            return
        if not self.projectPath:
            ui.notify('Please select a project folder first.', color='negative')
            return

        pub.sendMessage("rom_opened", romPath=self.romPath)
        pub.sendMessage("project_save", projectPath=self.projectPath)
        ui.notify(f'Project saved to {self.projectPath}', position='bottom-right')

    def openProject(self, parent=None):
        self.open_dialog = ui.dialog()
        with self.open_dialog, ui.card().classes('w-96'):
            ui.label('Open project').classes('text-lg font-semibold')

            self.projectInput = ui.input(label='Project folder', placeholder='Choose a project folder')
            self._make_directory_picker(
                self.projectInput,
                'projectPath',
                'Choose project folder',
                None,
            )

            with ui.row().classes('justify-end gap-2'):
                ui.button('Cancel', on_click=self.open_dialog.close)
                ui.button('Open', on_click=self._open_project_dialog)

        self.open_dialog.open()

    def _on_open_project_upload(self, event):
        if event and getattr(event, 'files', None):
            file = event.files[0]
            self.projectPath = str(file.name)
            self.projectInput.value = self.projectPath

    def _open_project_dialog(self):
        if not self.projectPath:
            ui.notify('Please select a project folder first.', color='negative')
            return

        pub.sendMessage("project_open", projectPath=self.projectPath)
        ui.notify(f'Opening {self.projectPath}', position='bottom-right')

