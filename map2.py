import os, sys
import pygame
from pygame.locals import *
from map import Map
from tile import Tile
from unit import Unit

BLACK = (0,0,0)

UnitList = {
    "Rifleman" : {"HP" : 10, "AP" : 10, "attack": 3, "defense" : 0 , "walkCost" : 1, "turnCost" : 0},
    "Heavy Gunner" : {"HP" : 15, "AP" : 10, "attack": 8, "defense" : 2 , "walkCost" : 2, "turnCost" : 1,  "sprite" : "rheavy_down.png"}
}

pygame.init() 

def initialize_map():
    grid = Map()
    size = [grid.map_width*grid.margin+grid.map_width*grid.pix_width, grid.map_height*grid.margin+grid.map_height*grid.pix_height] # Set the pix_height and pix_width of the screen
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Space Crusade") # Set title of screen
    done = False #Loop until the user clicks the close button.
    clock = pygame.time.Clock() # Used to manage how fast the screen updates
    screen.fill(BLACK)

    # Draw Tiles
    tiles = pygame.sprite.Group()
    for x in range(grid.map_width):
        for y in range(grid.map_height):
            tiles.add(Tile(pygame.Rect(x*50, y*50, 50, 50), grid.grid[y][x]))

    return grid, done, clock, screen, size, tiles

def get_collidable_objects(tiles, units):
    collidable = []
    for tile in tiles: 
        if tile.collide: collidable.append(tile)
    for unit in units: 
        collidable.append(unit)

    return collidable

if __name__ == "__main__":
    grid, done, clock, screen, size, tiles = initialize_map()

    #environment
    turn = "red"
    selected_unit = None

    # Draw units (experimental)
    units = pygame.sprite.Group()
    sample_red = Unit(pygame.Rect(12*50, 15*50, 50, 50), "Heavy Gunner", UnitList["Heavy Gunner"], "red")
    units.add(sample_red)
    sample_blue = Unit(pygame.Rect(8*50, 3*50, 50, 50), "Heavy Gunner", UnitList["Heavy Gunner"], "blue")
    units.add(sample_blue)

    selected_unit = sample_red

    #get all collidable objects
    collidable =  get_collidable_objects(tiles, units)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                sys.exit()
            elif event.type == KEYDOWN:
                if ((event.key == K_RIGHT)
                or (event.key == K_LEFT)
                or (event.key == K_UP)
                or (event.key == K_DOWN)):
                    selected_unit.move(event.key, collidable)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x,y = event.pos

                for unit in units:
                    if unit.rect.collidepoint(x,y):
                        selected_unit = unit
                        
        tiles.draw(screen)
        units.draw(screen)
        pygame.display.flip()
        pass