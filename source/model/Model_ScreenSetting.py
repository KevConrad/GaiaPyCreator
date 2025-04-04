
class Model_ScreenSetting:
    MAP_LAYER_ORDER_IS_DOUBLE_BG1_WIDTH_BIT_MASK = 0x01
    MAP_LAYER_ORDER_IS_DOUBLE_BG1_HEIGHT_BIT_MASK = 0x02
    MAP_LAYER_ORDER_IS_DOUBLE_BG1_WIDTH_BIT_MASK = 0x04
    MAP_LAYER_ORDER_IS_DOUBLE_BG1_HEIGHT_BIT_MASK = 0x08
    MAP_LAYER_ORDER_IS_BIT4_BIT_MASK = 0x10
    MAP_LAYER_ORDER_IS_BIT5_BIT_MASK = 0x20
    MAP_LAYER_ORDER_IS_BIT6_BIT_MASK = 0x40
    MAP_LAYER_ORDER_HAS_NORMAL_MAP_LAYERS = 0x80

    def __init__(self, romData, address) -> None:
        self.romData = romData

        # read the screen settings data
        self.enableMapLayerBits = romData[address]
        address += 1
        self.enableMapSubscreenLayerBits = romData[address]
        address += 1
        self.translucencySettingsABits = romData[address]
        address += 1
        self.translucencySettingsBBits = romData[address]
        address += 1
        self.byte4Bits = romData[address]
        address += 1
        self.mapLayerOrderBits = romData[address]
        address += 1
        self.BGModeSettingsBits = romData[address]
        address += 1
        self.byte7Bits = romData[address]
        address += 1
        self.byte8Bits = romData[address]
        address += 1
        self.byte9Bits = romData[address]
    