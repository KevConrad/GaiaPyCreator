from nicegui import ui

from view.View_Common import View_Common

class View_Items:
    def __init__(self, expansion: ui.expansion):
        with expansion:
            with ui.row().classes('items-center gap-2'):
                self.listBoxItems = ui.select(label="Items", on_change=self.onListBox, options=["A", "B", "C"]).props('clearable')

                with ui.column().classes('gap-2'):
                    with ui.row().classes('items-center gap-2'):
                        self.labelItemName = ui.label("Name:")
                        self.textCtrlItemName = ui.input()

                    with ui.row().classes('items-center gap-2'):
                        self.labelItemDescription = ui.label("Description:")
                        self.textCtrlItemDescription = ui.input()

                    with ui.row().classes('items-center gap-2'):
                        self.labelItemIsRemovable = ui.label("Removable:")
                        self.checkBoxItemIsRemovable = ui.checkbox()

                    with ui.row().classes('items-center gap-2'):
                        self.labelItemFindMessage = ui.label("Find Message:")
                        self.textCtrlItemFindMessage = ui.input()

    def load(self, itemNames, itemDescriptions, itemRemovableFlags, itemFindMessages):
        self.listBoxItems.Set(itemNames)
        self.textCtrlItemName.Value = ""
        self.itemDescriptions = itemDescriptions
        self.itemRemovableFlags = itemRemovableFlags
        self.itemFindMessages = itemFindMessages

    def onListBox(self, event):
        selectedIndex = self.listBoxItems.GetSelection()
        self.textCtrlItemName.Value = event.GetEventObject().GetStringSelection()
        self.textCtrlItemDescription.Value = self.itemDescriptions[selectedIndex]
        self.checkBoxItemIsRemovable.SetValue(self.itemRemovableFlags[selectedIndex])
        self.textCtrlItemFindMessage.Value = self.itemFindMessages[selectedIndex]