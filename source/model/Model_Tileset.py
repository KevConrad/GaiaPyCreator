from model.Model_Compression import Model_Compression
import sys

class Model_Tileset:
    def __init__(self, romData, tilesetData : dict) -> None:
        self.name = str(tilesetData['Name'])
        self.address = int(str(tilesetData['Address']), 16)
        self.compSize = int(str(tilesetData['CompSize']), 16)
        self.decompOffset = int(str(tilesetData['DecompOffset']), 16)
        self.decompSize = int(str(tilesetData['DecompSize']), 16)
        self.format = int(str(tilesetData['Format']), 16)

        if self.compSize > 0:
            compressedData = []
            for i in range (self.compSize):
                compressedData.append(romData[self.address + i])
                
            self.data, self.decompSize = Model_Compression.decompress(compressedData)
        else:
            self.data = romData[self.address:self.decompSize]

    