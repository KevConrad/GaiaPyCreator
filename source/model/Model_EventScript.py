from model.Model_Event import Model_Event
from model.Model_EventCommand import Model_EventCommand
from model.Model_EventCommandData import Model_EventCommandData
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

        breakFlag = False

        self.commands = []
        self.calledScriptAddresses = []
        self.commandHierarchies = []
        self.commandHierarchyCount = 0

        self.readHeader()

        while len(self.commands) < self.MAX_COUNT_COMMANDS:
            if len(self.commandHierarchies) > (0x39):
                break

            if ((breakFlag == True) or (self.readOffset < 0)):
                break

            isExistingCommand = self.getIsBranchExisting(self.readOffset)
            if isExistingCommand == False:
                command = Model_EventCommand(self.romData, self.readOffset, self.commandData)
                self.readOffset += command.size
                self.commands.append(command)

                if command.getCommandType() == Model_EventCommand.CommandType.CALL:
                    pass
                    #self.calledScriptAddresses.append(commandcmd[cmd.Count - 1].GetCommandBranchAddress());
                elif command.getCommandType() == Model_EventCommand.CommandType.CONDITION or \
                     command.getCommandType() == Model_EventCommand.CommandType.CONDITION_TRUE_ONLY or \
                     command.getCommandType() == Model_EventCommand.CommandType.BRANCH:
                    pass
                    #CreateCommandBranch(source, ref i);
                elif command.getCommandType() == Model_EventCommand.CommandType.CHOICE:
                    self.messageBoxChoiceCount = self.romData[self.address - 4]
                    self.messageBoxChoiceId = 0
                    self.messageBoxTableAddress = i
                    #CreateCommandBranch(source, ref i);
                elif command.getCommandType() == Model_EventCommand.CommandType.MULTIPLE_CONDITION:
                    #self.multipleConditionAddresses = command.GetMultipleConditionAddresses()
                    #self.multipleConditionCount = command.GetMultipleConditionCount()
                    #self.multipleConditionNames = command.GetMultipleConditionNames()
                    self.multipleConditionIndex = 0
                    #CreateCommandBranch(source, ref i);
                elif command.getCommandType() == Model_EventCommand.CommandType.LEAVE:
                    pass
                    #RemoveCommandHierarchy(source, ref i);
                else:
                    # do nothing here
                    pass

    def readHeader(self):
        # todo needed ? if self.eventType is Model_Event.TYPE_ENEMY or self.eventType is Model_Event.TYPE_NPC:
        self.spriteIndex = self.romData[self.readOffset]
        self.readOffset += 1
        self.byte0 = self.romData[self.readOffset]
        self.readOffset += 1
        self.byte1 = self.romData[self.readOffset]
        self.readOffset += 1

    def getIsBranchExisting(self, branchAddress):
        isBranchExisting = False

        for commandIndex in range (len(self.commands)):
            if (branchAddress == self.commands[commandIndex].address):
                #cmd.Add(new EventCommand(branchAddress, m_commandHierarchies.Count, cmd[j].GetId(), j));
                #RemoveCommandHierarchy(source, ref i);
                isBranchExisting = True
                break

        return isBranchExisting