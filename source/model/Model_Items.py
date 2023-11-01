
from Model_RomDataTable import Model_RomDataTable

class Model_Items:
    def __init__(self) -> None:
        pass
        
    def load(self, projectData : dict):
        try:
            # load the item name table
            self.loadItemNameTable(projectData)

            # load the item data
            itemData = projectData['Items']
            self.loadItemNames(itemData)
            self.loadItemEvents(itemData)
            
        except:
            print("EXCEPTION: Invalid item data in project file!")

    def loadItemEvents(self, itemData : dict):
        # save the item event addresses in a list
        self.itemEvents = []
        for item in itemData:
            self.itemEvents.append(item['Event'])

    def loadItemNames(self, itemData : dict):
        # save the item names in a list
        self.itemNames = []
        for item in itemData:
            self.itemNames.append(item['Name'])
        
        # print the item names
        print(self.itemNames)
    
    def loadItemNameTable(self, projectData : dict):
        itemNameTableAddress = int(str(projectData['ItemNameTable']['Address']), 16)
        itemNameTableSize = int(projectData['ItemNameTable']['Size'])

        self.itemNameTable = Model_RomDataTable(itemNameTableAddress, itemNameTableSize)