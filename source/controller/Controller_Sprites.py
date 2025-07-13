from pubsub import pub

# notification
from pubsub.utils.notification import useNotifyByWriteFile

from controller.Controller_Project import Controller_Project
from model.Model_Spritesets import Model_Spritesets
from view.View_Main import View_Main

class Controller_Sprites:
    def __init__(self, project : Controller_Project, view:View_Main) -> None:
        self.project = project
        self.view = view

        self.spritesets = Model_Spritesets(self.project.romData.romData, self.project.projectData.projectData)

        pub.subscribe(self.load, "sprites_load")
        pub.subscribe(self.updateSpriteset, "sprites_update_spriteset")
        pub.subscribe(self.updateSprite, "sprites_update_sprite")

    def load(self):
        if self.project.isProjectLoaded == True:
            # display the spritesets in the GUI
            self.view.sprites.load(self.spritesets)

    def updateSpriteset(self, spritesetIndex):
        self.spritesetIndex = spritesetIndex
        self.spritesets.spritesets[spritesetIndex].read()
        self.view.sprites.updateSpriteset(self.spritesets.spritesets[spritesetIndex])

    def updateSprite(self, spriteIndex):
        tilesetBits = self.spritesets.spritesets[self.spritesetIndex].tilesetBits
        self.spriteFrameImage = self.spritesets.spritesets[self.spritesetIndex].spriteFrames[spriteIndex].createImage(128, 128, tilesetBits)
        self.view.sprites.updateSprite(spriteIndex)
        