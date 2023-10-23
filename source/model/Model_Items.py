

class Model_Items:
    def __init__(self) -> None:
        pass
        
    def load(self, projectData : dict):
        try:
            # get the item data
            items = projectData['Items']

            # save the item names in a list
            self.itemNames = []
            for item in items:
                self.itemNames.append(item['Name'])
            
            # print the item names
            print(self.itemNames)
        except:
            print("EXCEPTION: No items found in project file!")