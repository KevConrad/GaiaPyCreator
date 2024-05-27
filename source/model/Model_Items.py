from model.Model_RomDataTable import Model_RomDataTable
from model.Model_Text import Model_Text
import sys

class Model_Items:
    def __init__(self, romData) -> None:
        self.romData = romData

    def load(self, projectData : dict):
        #try:
            # load the item names and descriptions
            self.loadItemRomNames(projectData)
            self.loadItemDescriptions(projectData)
            self.loadItemFindMessages(projectData)

            # load the item data
            itemData = projectData['Items']
            self.loadItemNames(itemData)
            self.loadItemEvents(itemData)
            self.loadItemIsRemovableFlags(projectData)
            
        #except:
            print("EXCEPTION: Invalid item data in project file!")

    def loadItemDescriptions(self, projectData : dict):
        itemDescriptionTableAddress = int(str(projectData['ItemDescriptionTable']['Address']), 16)
        itemDescriptionTableSize = int(projectData['ItemDescriptionTable']['Size'])

        print('Item.ItemDescriptionTableAddress: ' + hex(itemDescriptionTableAddress))

        itemDescriptionTable = Model_RomDataTable(self.romData, itemDescriptionTableAddress, itemDescriptionTableSize)
        print(sys.getsizeof(self.romData))

        self.itemDescriptions = []
        for item in range (itemDescriptionTableSize):
            self.itemDescriptions.append(Model_Text.readAsciiText(self.romData, itemDescriptionTable.getDataAddress(item)))
        
        print('Item.ItemDescriptions:')
        print(self.itemDescriptions)

    def loadItemEvents(self, itemData : dict):
        # save the item event addresses in a list
        self.itemEvents = []
        #for item in itemData:
        #    self.itemEvents.append(item['Event'])

    def loadItemFindMessages(self, projectData : dict):
        itemFindMessagesTableAddress = int(str(projectData['ItemFindMessageTable']['Address']), 16)
        itemFindMessagesTableSize = int(projectData['ItemFindMessageTable']['Size'])

        print('Item.itemFindMessagesTableAddress: ' + hex(itemFindMessagesTableAddress))

        itemFindMessagesTable = Model_RomDataTable(self.romData, itemFindMessagesTableAddress, itemFindMessagesTableSize)
        print(sys.getsizeof(self.romData))

        self.itemFindMessages = []
        for item in range (itemFindMessagesTableSize):
            self.itemFindMessages.append(Model_Text.readMessageText(self.romData, itemFindMessagesTable.getDataAddress(item)))
        
        print('Item.ItemFindMessages:')
        print(self.itemFindMessages)

    def loadItemNames(self, itemData : dict):
        # save the item names in a list
        self.itemNames = []
        for item in itemData:
            self.itemNames.append(item['Name'])
        
        # print the item names
        print('ItemNames:')
        print(self.itemNames)
    
    def loadItemRomNames(self, projectData : dict):
        itemNameTableAddress = int(str(projectData['ItemNameTable']['Address']), 16)
        itemNameTableSize = int(projectData['ItemNameTable']['Size'])
        self.itemCount = itemNameTableSize
        print('Item.ItemNameTableAddress: ' + hex(itemNameTableAddress))

        itemNameTable = Model_RomDataTable(self.romData, itemNameTableAddress, itemNameTableSize)
        print(sys.getsizeof(self.romData))

        self.itemRomNames = []
        for item in range (itemNameTableSize):
            self.itemRomNames.append(Model_Text.readAsciiText(self.romData, itemNameTable.getDataAddress(item)))
        
        print('Item.ItemRomNames:')
        print(self.itemRomNames)

    def loadItemIsRemovableFlags(self, projectData : dict):
        itemIsRemovableFlagsAddress = int(str(projectData['ItemRemovalFlags']['Address']), 16)
        print('Item.IsRemovableFlags.Address: ' + hex(itemIsRemovableFlagsAddress))

        self.itemIsRemovableFlags = []
        for item in range (self.itemCount):
            # get the flag address and bit position for the current item index
            flagByteIndex = int(item / 8)
            bitIndex = item % 8
            flagAddress = itemIsRemovableFlagsAddress + flagByteIndex

            # check if the removable flag is cleared and save it to the flag array
            if self.romData[flagAddress] & (1 << bitIndex):
                self.itemIsRemovableFlags.append(False)
            else:
                self.itemIsRemovableFlags.append(True)
            