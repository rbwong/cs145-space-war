import os, sys
import pygame
from pygame.locals import *
from tile import Tile
from unit import Unit

class Map:
    def __init__(self):
        self.map_width = 17
        self.map_height = 15
        self.pix_width = 50
        self.pix_height = 50
        self.margin = 1

        with open("map.txt") as myfile: #load map from txt
            self.grid = [row.split(";") for row in myfile]