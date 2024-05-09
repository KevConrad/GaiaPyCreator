
from model.Model_RomDataTable import Model_RomDataTable
from model.Model_Text import Model_Text
import sys

class Model_Items:
    def __init__(self, romData) -> None:
        self.romData = romData

    def load(self, projectData : dict):
        #try:
            # load the item name table
            self.loadItemRomNames(projectData)

            # load the item data
            itemData = projectData['Items']
            self.loadItemNames(itemData)
            self.loadItemEvents(itemData)
            
        #except:
            print("EXCEPTION: Invalid item data in project file!")

    def loadItemEvents(self, itemData : dict):
        # save the item event addresses in a list
        self.itemEvents = []
        #for item in itemData:
        #    self.itemEvents.append(item['Event'])

    def loadItemNames(self, itemData : dict):
        # save the item names in a list
        self.itemNames = []
        for item in itemData:
            self.itemNames.append(item['Name'])
        
        # print the item names
        print(self.itemNames)
    
    def loadItemRomNames(self, projectData : dict):
        itemNameTableAddress = int(str(projectData['ItemNameTable']['Address']), 16)
        itemNameTableSize = int(projectData['ItemNameTable']['Size'])
        print(itemNameTableAddress)

        itemNameTable = Model_RomDataTable(self.romData, itemNameTableAddress, itemNameTableSize)
        print(sys.getsizeof(self.romData))

        self.itemRomNames = []
        for item in range (itemNameTableSize):
            self.itemRomNames.append(Model_Text.readAsciiText(self.romData, itemNameTable.getDataAddress(item)))
        
        print(self.itemRomNames)