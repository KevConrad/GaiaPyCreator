

class Model_Items:
    def __init__(self) -> None:
        pass
        
    def load(self, projectData : dict):
        # Iterating through the json
        # list
        try:
            if 'Items' in projectData:
                print("ITEMS: ", projectData['Items'])
        except: 
            print("EXCEPTION: ", projectData)