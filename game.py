import os, sys
import pygame
from pygame.locals import *
from map import Map
from door import Door
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
            tiles.add(Tile(pygame.Rect(x*51, y*51, 50, 50), grid.grid[y][x]))

    return grid, done, clock, screen, size, tiles

def get_collidable_objects(tiles, red_units, blue_units, doors):
    collidable = []
    for tile in tiles: 
        if tile.collide: collidable.append(tile)
    for unit in red_units: 
        collidable.append(unit)
    for unit in blue_units: 
        collidable.append(unit)
    for door in doors: 
        collidable.append(door)

    return collidable

if __name__ == "__main__":
    grid, done, clock, screen, size, tiles = initialize_map()

    #environment
    turn = "red"
    selected_unit = None

    # Love is an open DOOOR
    doors = pygame.sprite.Group()
    door = Door(pygame.Rect(8*51, 3*51, 51, 51))
    doors.add(door)
    door = Door(pygame.Rect(1*51, 10*51, 51, 51))
    doors.add(door)
    door = Door(pygame.Rect(2*51, 7*51, 51, 51))
    doors.add(door)
    door = Door(pygame.Rect(7*51, 8*51, 51, 51))
    doors.add(door)
    door = Door(pygame.Rect(10*51, 9*51, 51, 51))
    doors.add(door)
    door = Door(pygame.Rect(14*51, 10*51, 51, 51))
    doors.add(door)
    door = Door(pygame.Rect(15*51, 7*51, 51, 51))
    doors.add(door)
    door = Door(pygame.Rect(3*51, 9*51, 51, 51),"vertical")
    doors.add(door)
    door = Door(pygame.Rect(12*51, 8*51, 51, 51),"vertical")
    doors.add(door)
    door = Door(pygame.Rect(6*51, 4*51, 51, 51),"vertical")
    doors.add(door)
    door = Door(pygame.Rect(10*51, 4*51, 51, 51),"vertical")
    doors.add(door)

    # Draw Red units
    red_units = pygame.sprite.Group()
    sample_red = Unit(pygame.Rect(8*51, 13*51, 51, 51), "Heavy Gunner", UnitList["Heavy Gunner"], "red")
    red_units.add(sample_red)
    sample_red = Unit(pygame.Rect(7*51, 13*51, 51, 51), "Heavy Gunner", UnitList["Heavy Gunner"], "red")
    red_units.add(sample_red)
    sample_red = Unit(pygame.Rect(6*51, 13*51, 51, 51), "Heavy Gunner", UnitList["Heavy Gunner"], "red")
    red_units.add(sample_red)
    sample_red = Unit(pygame.Rect(2*51, 13*51, 51, 51), "Heavy Gunner", UnitList["Heavy Gunner"], "red")
    red_units.add(sample_red)
    sample_red = Unit(pygame.Rect(12*51, 13*51, 51, 51), "Heavy Gunner", UnitList["Heavy Gunner"], "red")
    red_units.add(sample_red)
    sample_red = Unit(pygame.Rect(13*51, 13*51, 51, 51), "Heavy Gunner", UnitList["Heavy Gunner"], "red")
    red_units.add(sample_red)
    sample_red = Unit(pygame.Rect(14*51, 13*51, 51, 51), "Heavy Gunner", UnitList["Heavy Gunner"], "red")
    red_units.add(sample_red)

    # Draw Blue units
    blue_units = pygame.sprite.Group()
    sample_blue = Unit(pygame.Rect(5*51, 4*51, 51, 51), "Heavy Gunner", UnitList["Heavy Gunner"], "blue")
    blue_units.add(sample_blue)
    sample_blue = Unit(pygame.Rect(1*51, 4*51, 51, 51), "Heavy Gunner", UnitList["Heavy Gunner"], "blue")
    blue_units.add(sample_blue)
    sample_blue = Unit(pygame.Rect(4*51, 3*51, 51, 51), "Heavy Gunner", UnitList["Heavy Gunner"], "blue")
    blue_units.add(sample_blue)
    sample_blue = Unit(pygame.Rect(8*51, 6*51, 51, 51), "Heavy Gunner", UnitList["Heavy Gunner"], "blue")
    blue_units.add(sample_blue)
    sample_blue = Unit(pygame.Rect(13*51, 4*51, 51, 51), "Heavy Gunner", UnitList["Heavy Gunner"], "blue")
    blue_units.add(sample_blue)
    sample_blue = Unit(pygame.Rect(15*51, 4*51, 51, 51), "Heavy Gunner", UnitList["Heavy Gunner"], "blue")
    blue_units.add(sample_blue)
    sample_blue = Unit(pygame.Rect(11*51, 4*51, 51, 51), "Heavy Gunner", UnitList["Heavy Gunner"], "blue")
    blue_units.add(sample_blue)

    selected_unit = sample_red
    selected_unit.select()

    #get all collidable objects
    collidable =  get_collidable_objects(tiles, red_units, blue_units, doors)

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

                elif (event.key == K_e):
                    door = selected_unit.openDoor(doors)
                    if door:
                        collidable.remove(door)
                        door.open = True
                        door.setDoor()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x,y = event.pos

                flag = False
                for unit in red_units:
                    if unit.rect.collidepoint(x,y):
                        selected_unit.deselect()
                        selected_unit = unit
                        selected_unit.select()
                        flag = True

                if not flag:
                    for unit in blue_units:
                        if unit.rect.collidepoint(x,y):
                            selected_unit.deselect()
                            selected_unit = unit
                            selected_unit.select()

        tiles.draw(screen)
        doors.draw(screen)
        red_units.draw(screen)
        blue_units.draw(screen)
        pygame.display.flip()
        pass