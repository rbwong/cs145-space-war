import os, sys
import pygame
from pygame.locals import *
from tile import Tile
from unit import Unit

BLACK = (0,0,0)

UnitList = {
    "Rifleman" : {"HP" : 10, "AP" : 10, "attack": 3, "defense" : 0 , "walkCost" : 1, "turnCost" : 0},
    "Heavy Gunner" : {"HP" : 15, "AP" : 10, "attack": 8, "defense" : 2 , "walkCost" : 2, "turnCost" : 1,  "sprite" : "rheavy_down.png"}
}

class Map:
    def __init__(self):
        self.map_width = 15
        self.map_height = 15
        self.pix_width = 50
        self.pix_height = 50
        self.margin = 1

        with open("map.txt") as myfile: #load map from txt
            self.grid = [row.split(";") for row in myfile]


if __name__ == "__main__":
    grid = Map()

    pygame.init()
    # Set the pix_height and pix_width of the screen
    size = [grid.map_width*grid.margin+grid.map_width*grid.pix_width, grid.map_height*grid.margin+grid.map_height*grid.pix_height]
    screen = pygame.display.set_mode(size)
    # Set title of screen
    pygame.display.set_caption("Space Crusade")
    #Loop until the user clicks the close button.
    done = False
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    screen.fill(BLACK)

    # Draw Tiles
    tiles = pygame.sprite.Group()
    for x in range(grid.map_width):
        for y in range(grid.map_height):
            print grid.grid[y][x]
            tiles.add(Tile(pygame.Rect(x*51, y*51, 50, 50), grid.grid[y][x]))

    # Draw units (experimental)
    units = pygame.sprite.Group()
    snake = Unit(pygame.Rect(7*51, 2*51, 50, 50), "Heavy Gunner", UnitList["Heavy Gunner"], "red")
    units.add(snake)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                sys.exit()
            elif event.type == KEYDOWN:
                if ((event.key == K_RIGHT)
                or (event.key == K_LEFT)
                or (event.key == K_UP)
                or (event.key == K_DOWN)):
                    snake.move(event.key)

        tiles.draw(screen)
        units.draw(screen)
        pygame.display.flip()
        pass