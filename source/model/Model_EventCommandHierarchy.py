from .Model_EventCommandData import Model_EventCommandData

class Model_EventCommandHierarchy:
    def __init__(self, return_address, command_type: Model_EventCommandData.CommandType) -> None:
        self.return_address = return_address
        self.command_type = command_type
        self.message_box_choice_count = 0
        self.message_box_choice_id = 0
        self.message_box_table_address = 0
        self.multiple_condition_count = 0
        self.multiple_condition_index = 0
        self.multiple_condition_addresses = []
        self.multiple_condition_names = []