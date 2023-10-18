

class Model_Items:
    def __init__(self) -> None:
        pass
        
    def load(self, projectData : dict):
        try:
            # iterate through the item list
            for item in projectData['Items']:
                itemName = item['Name']
                print(itemName)
        except:
            print("EXCEPTION: No items found in project file!")