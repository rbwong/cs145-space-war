import os, sys
import pygame
from pygame.locals import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, rect, floortype="black"):
        self.floortype = floortype # "black", "normal", "snow#"
        self.collide = False

        if self.floortype == "black":
            self.collide = True
        if self.floortype == "doorch":
            self.collide = True
        if self.floortype == "doorcv":
            self.collide = True

        self.spriteDict = {
            "normal" : "floor.png",
            "black" : "black.png",
            "dooroh" : "door_oh.png",
            "doorch" : "door_ch.png",
            "doorov" : "door_ov.png",
            "doorcv" : "door_cv.png",
            "snow1" : "floor_ice1.png",
            "snow2" : "floor_ice2.png",
            "snow3" : "floor_ice3.png",
            "snow4" : "floor_ice4.png",
            "snow5" : "floor_ice5.png",
            "snow6" : "floor_ice6.png"
        }

        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join("images", self.spriteDict[self.floortype]))
        if rect != None:
            self.rect = rect