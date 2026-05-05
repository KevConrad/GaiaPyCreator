from model.Model_Event import Model_Event
from model.Model_EventCommand import Model_EventCommand
from model.Model_EventCommandData import Model_EventCommandData
from model.Model_EventCommandHierarchy import Model_EventCommandHierarchy
from model.Model_RomData import Model_RomData

class Model_EventScript:
    MAX_COUNT_COMMANDS = 512

    def __init__(self, romData, address, commandData : Model_EventCommandData) -> None:
        self.romData = romData
        self.address = address
        self.commandData = commandData

        self.read()

    def read(self):
        self.readOffset = self.address

        self.breakFlag = False

        self.commands = []
        self.calledScriptAddresses = []
        self.commandHierarchies = []
        self.commandHierarchyCount = 0

        self.read_header()

        while len(self.commands) < self.MAX_COUNT_COMMANDS:
            if len(self.commandHierarchies) > (0x39):
                break

            if ((self.breakFlag == True) or (self.readOffset < 0)):
                break

            isExistingCommand = self.get_is_branch_existing(self.readOffset)
            if isExistingCommand == False:
                command = Model_EventCommand.from_rom_data(self.romData, self.readOffset, self.commandData)
                self.readOffset += command.size
                self.commands.append(command)

                if command.get_type() == Model_EventCommandData.CommandType.CALL:
                    self.calledScriptAddresses.append(command.get_branch_address());
                elif command.get_type() == Model_EventCommandData.CommandType.CONDITION or \
                     command.get_type() == Model_EventCommandData.CommandType.CONDITION_TRUE_ONLY or \
                     command.get_type() == Model_EventCommandData.CommandType.BRANCH:
                    self.readOffset = self.createCommandBranch(command, self.readOffset)
                elif command.get_type() == Model_EventCommandData.CommandType.CHOICE:
                    self.messageBoxChoiceCount = self.romData[self.address - 4]
                    self.messageBoxChoiceId = 0
                    self.messageBoxTableAddress = self.readOffset
                    self.readOffset = self.createCommandBranch(command, self.readOffset)
                elif command.get_type() == Model_EventCommandData.CommandType.MULTIPLE_CONDITION:
                    #self.multipleConditionAddresses = command.getDataValue(Model_EventCommandData.DataType.BRANCH_RELATIVE)
                    #self.multipleConditionCount = command.getDataValue(Model_EventCommandData.DataType.CHOICE_COUNT)
                    #self.multipleConditionNames = command.getDataValue(Model_EventCommandData.DataType.MESSAGE_BOX_CHOICE)
                    self.multipleConditionIndex = 0
                    self.readOffset = self.createCommandBranch(command, self.readOffset)
                elif command.get_type() == Model_EventCommandData.CommandType.LEAVE:
                    self.remove_command_hierarchy()
                else:
                    # do nothing here
                    pass

    def read_header(self):
        # todo needed ? if self.eventType is Model_Event.TYPE_ENEMY or self.eventType is Model_Event.TYPE_NPC:
        self.spriteIndex = self.romData[self.readOffset]
        self.readOffset += 1
        self.byte0 = self.romData[self.readOffset]
        self.readOffset += 1
        self.byte1 = self.romData[self.readOffset]
        self.readOffset += 1

    def createCommandBranch(self, command: Model_EventCommand, address):
        self.add_command_hierarchy(Model_EventCommandHierarchy(address, command.get_type))

        address = command.get_branch_address()

        if (command.get_type() == Model_EventCommandData.CommandType.CONDITION or
            command.get_type() == Model_EventCommandData.CommandType.CONDITION_TRUE_ONLY):
            if command.get_type() == Model_EventCommandData.CommandType.CONDITION_TRUE_ONLY:
                command_hierarchy_type = Model_EventCommandData.CommandType.CONDITION_TRUE_ONLY
            else:
                command_hierarchy_type = Model_EventCommandData.CommandType.CONDITION_TRUE
            self.commands.append(Model_EventCommand.from_parameters(len(self.commandHierarchies), "##### TRUE #####", 0xC1, Model_EventCommandData.CommandType.CONDITION_TRUE))
            self.add_command_hierarchy(Model_EventCommandHierarchy(0, command_hierarchy_type))
        else:
            if command.get_type() == Model_EventCommandData.CommandType.CHOICE:
                self.commands.append(Model_EventCommand.from_parameters(len(self.commandHierarchies), "##### CHOICE CANCEL #####", 0xC2, Model_EventCommandData.CommandType.CHOICE_ENTRY))
                self.add_command_hierarchy(Model_EventCommandHierarchy(0, Model_EventCommandData.CommandType.CHOICE_ENTRY))
                #address = self.get_text_choice_address(self.message_box_table_address, self.message_box_choice_id)
                self.message_box_choice_id += 1
            else:
                if command.get_type() == Model_EventCommandData.CommandType.MULTIPLE_CONDITION:
                    self.commands.append(Model_EventCommand.from_parameters(len(self.commandHierarchies), self.multiple_condition_names[self.multiple_condition_index], 0xC2, Model_EventCommandData.CommandType.MULTIPLE_CONDITION_ENTRY))
                    self.add_command_hierarchy(Model_EventCommandHierarchy(0, Model_EventCommandData.CommandType.MULTIPLE_CONDITION_ENTRY))
                    self.commandHierarchies[-1].multiple_condition_addresses = self.multiple_condition_addresses
                    self.commandHierarchies[-1].multiple_condition_count = self.multiple_condition_count
                    self.commandHierarchies[-1].multiple_condition_index = 0
                    self.commandHierarchies[-1].multiple_condition_names = self.multiple_condition_names
                    self.commandHierarchies[-1].multiple_condition_index += 1
                    address = self.commandHierarchies[-1].multiple_condition_addresses[0]
        # handle a branch to an already existing command
        #self.handle_existing_command_branch(address)
        return address

    def add_command_hierarchy(self, command_hierarchy):
        """Add a command hierarchy and increment count if needed."""
        self.commandHierarchies.append(command_hierarchy)
        if len(self.commandHierarchies) > self.commandHierarchyCount:
            self.commandHierarchyCount += 1

    def remove_command_hierarchy(self):
        """Remove command hierarchy when encountering certain command types."""
        if len(self.commandHierarchies) > 0:
            command_type = self.commandHierarchies[-1].command_type

            while (command_type == Model_EventCommandData.CommandType.BRANCH or
                   command_type == Model_EventCommandData.CommandType.CHOICE_ENTRY or
                   command_type == Model_EventCommandData.CommandType.CONDITION_FALSE or
                   command_type == Model_EventCommandData.CommandType.CONDITION_TRUE or
                   command_type == Model_EventCommandData.CommandType.CONDITION_TRUE_ONLY or
                   command_type == Model_EventCommandData.CommandType.MULTIPLE_CONDITION_ENTRY):

                # read the multiple condition status
                multiple_condition_addresses = self.commandHierarchies[-1].m_multipleConditionAddresses
                multiple_condition_count = self.commandHierarchies[-1].m_multipleConditionCount
                multiple_condition_index = self.commandHierarchies[-1].m_multipleConditionIndex
                multiple_condition_names = self.commandHierarchies[-1].m_multipleConditionNames

                if len(self.commandHierarchies) > 0:
                    self.commandHierarchies.pop()
                    if len(self.commandHierarchies) > 0:
                        self.readOffset = self.commandHierarchies[-1].m_returnAddress
                    else:
                        self.breakFlag = True
                        break
                else:
                    self.breakFlag = True
                    break

                if command_type == Model_EventCommandData.CommandType.BRANCH:
                    command_type = self.commandHierarchies[-1].m_type
                else:
                    if command_type == Model_EventCommandData.CommandType.CONDITION_TRUE:
                        self.commands.append(Model_EventCommand.from_parameters(len(self.commandHierarchies), "##### FALSE #####", 0xC0, Model_EventCommandData.CommandType.CONDITION_FALSE))
                        self.add_command_hierarchy(Model_EventCommandHierarchy(0, Model_EventCommandData.CommandType.CONDITION_FALSE))
                        break
                    else:
                        if (command_type == Model_EventCommandData.CommandType.CHOICE_ENTRY and
                            self.messageBoxChoiceId <= self.messageBoxChoiceCount):
                            self.commands.append(Model_EventCommand.from_parameters(len(self.commandHierarchies), f"##### CHOICE {self.messageBoxChoiceId} #####", 0xC2, Model_EventCommandData.CommandType.CHOICE_ENTRY))
                            self.add_command_hierarchy(Model_EventCommandHierarchy(0, Model_EventCommandData.CommandType.CHOICE_ENTRY))
                            self.readOffset = self.get_text_choice_address(self.romData, self.messageBoxTableAddress, self.messageBoxChoiceId)
                            self.messageBoxChoiceId += 1
                            break
                        else:
                            if (command_type == Model_EventCommandData.CommandType.MULTIPLE_CONDITION_ENTRY and
                                multiple_condition_index < multiple_condition_count):
                                self.commands.append(Model_EventCommand.from_parameters(len(self.commandHierarchies), multiple_condition_names[multiple_condition_index], 0xC2, Model_EventCommandData.CommandType.MULTIPLE_CONDITION_ENTRY))
                                self.commandHierarchies.append(Model_EventCommandHierarchy(0, Model_EventCommandData.CommandType.MULTIPLE_CONDITION_ENTRY))

                                # save the multiple condition status
                                self.commandHierarchies[-1].m_multipleConditionAddresses = multiple_condition_addresses
                                self.commandHierarchies[-1].m_multipleConditionCount = multiple_condition_count
                                self.commandHierarchies[-1].m_multipleConditionIndex = multiple_condition_index
                                self.commandHierarchies[-1].m_multipleConditionNames = multiple_condition_names
                                self.commandHierarchies[-1].m_multipleConditionIndex += 1

                                self.readOffset = multiple_condition_addresses[multiple_condition_index]
                                break

                            self.commandHierarchies.pop()

                            if len(self.commandHierarchies) > 0:
                                self.readOffset = self.commandHierarchies[-1].m_returnAddress
                                command_type = self.commandHierarchies[-1].m_type
                            else:
                                self.breakFlag = True
                                break
        else:
            self.breakFlag = True

    def get_is_branch_existing(self, branchAddress):
        isBranchExisting = False

        for command in self.commands:
            if command.address is not None:
                if (branchAddress == command.address):
                    self.commands.append(Model_EventCommand.from_branch_command(branchAddress, len(self.commandHierarchies),
                                                                                command.id, self.commands.index(command)))
                    self.remove_command_hierarchy()
                    isBranchExisting = True
                    break

        return isBranchExisting



