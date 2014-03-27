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
            tiles.add(Tile(pygame.Rect(x*50, y*50, 50, 50), grid.grid[y][x]))

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
    door = Door(pygame.Rect(8*grid.pix_width, 3*grid.pix_height, 50, 50))
    doors.add(door)
    door = Door(pygame.Rect(1*grid.pix_width, 10*grid.pix_height, 50, 50))
    doors.add(door)
    door = Door(pygame.Rect(2*grid.pix_width, 7*grid.pix_height, 50, 50))
    doors.add(door)
    door = Door(pygame.Rect(7*grid.pix_width, 8*grid.pix_height, 50, 50))
    doors.add(door)
    door = Door(pygame.Rect(10*grid.pix_width, 9*grid.pix_height, 50, 50))
    doors.add(door)
    door = Door(pygame.Rect(14*grid.pix_width, 10*grid.pix_height, 50, 50))
    doors.add(door)
    door = Door(pygame.Rect(15*grid.pix_width, 7*grid.pix_height, 50, 50))
    doors.add(door)
    door = Door(pygame.Rect(3*grid.pix_width, 9*grid.pix_height, 50, 50),"vertical")
    doors.add(door)
    door = Door(pygame.Rect(12*grid.pix_width, 8*grid.pix_height, 50, 50),"vertical")
    doors.add(door)
    door = Door(pygame.Rect(6*grid.pix_width, 4*grid.pix_height, 50, 50),"vertical")
    doors.add(door)
    door = Door(pygame.Rect(10*grid.pix_width, 4*grid.pix_height, 50, 50),"vertical")
    doors.add(door)

    # Draw Red units
    red_units = pygame.sprite.Group()
    sample_red = Unit(pygame.Rect(8*grid.pix_width, 13*grid.pix_height, 50, 50), "Heavy Gunner", UnitList["Heavy Gunner"], "red")
    red_units.add(sample_red)
    sample_red = Unit(pygame.Rect(7*grid.pix_width, 13*grid.pix_height, 50, 50), "Heavy Gunner", UnitList["Heavy Gunner"], "red")
    red_units.add(sample_red)
    sample_red = Unit(pygame.Rect(6*grid.pix_width, 13*grid.pix_height, 50, 50), "Heavy Gunner", UnitList["Heavy Gunner"], "red")
    red_units.add(sample_red)
    sample_red = Unit(pygame.Rect(2*grid.pix_width, 13*grid.pix_height, 50, 50), "Heavy Gunner", UnitList["Heavy Gunner"], "red")
    red_units.add(sample_red)
    sample_red = Unit(pygame.Rect(12*grid.pix_width, 13*grid.pix_height, 50, 50), "Heavy Gunner", UnitList["Heavy Gunner"], "red")
    red_units.add(sample_red)
    sample_red = Unit(pygame.Rect(13*grid.pix_width, 13*grid.pix_height, 50, 50), "Heavy Gunner", UnitList["Heavy Gunner"], "red")
    red_units.add(sample_red)
    sample_red = Unit(pygame.Rect(14*grid.pix_width, 13*grid.pix_height, 50, 50), "Heavy Gunner", UnitList["Heavy Gunner"], "red")
    red_units.add(sample_red)

    # Draw Blue units
    blue_units = pygame.sprite.Group()
    sample_blue = Unit(pygame.Rect(5*grid.pix_width, 4*grid.pix_height, 50, 50), "Heavy Gunner", UnitList["Heavy Gunner"], "blue")
    blue_units.add(sample_blue)
    sample_blue = Unit(pygame.Rect(1*grid.pix_width, 4*grid.pix_height, 50, 50), "Heavy Gunner", UnitList["Heavy Gunner"], "blue")
    blue_units.add(sample_blue)
    sample_blue = Unit(pygame.Rect(4*grid.pix_width, 3*grid.pix_height, 50, 50), "Heavy Gunner", UnitList["Heavy Gunner"], "blue")
    blue_units.add(sample_blue)
    sample_blue = Unit(pygame.Rect(8*grid.pix_width, 6*grid.pix_height, 50, 50), "Heavy Gunner", UnitList["Heavy Gunner"], "blue")
    blue_units.add(sample_blue)
    sample_blue = Unit(pygame.Rect(13*grid.pix_width, 4*grid.pix_height, 50, 50), "Heavy Gunner", UnitList["Heavy Gunner"], "blue")
    blue_units.add(sample_blue)
    sample_blue = Unit(pygame.Rect(15*grid.pix_width, 4*grid.pix_height, 50, 50), "Heavy Gunner", UnitList["Heavy Gunner"], "blue")
    blue_units.add(sample_blue)
    sample_blue = Unit(pygame.Rect(11*grid.pix_width, 4*grid.pix_height, 50, 50), "Heavy Gunner", UnitList["Heavy Gunner"], "blue")
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
				if event.key in (K_RIGHT, K_LEFT, K_UP, K_DOWN):
					if selected_unit.AP > 0:
						selected_unit.move(event.key, collidable)

				elif (event.key == K_e):
					if selected_unit.AP > 0:
						door = selected_unit.openDoor(doors)
						if door:
							collidable.remove(door)
							door.open = True
							door.setDoor()

				elif (event.key == K_SPACE):
					pass

					direction = selected_unit.direction
					
				elif(event.key == K_RETURN):
					selected_unit.deselect()
					if turn == "red":
						turn = "blue"
						for unit in red_units:
							unit.AP = 6
						selected_unit = blue_units.sprites()[0]
					elif turn == "blue":
						turn = "red"
						for unit in blue_units:
							unit.AP = 6
						selected_unit = red_units.sprites()[0]
					selected_unit.select()
					print turn	

			elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				x,y = event.pos

				flag = False
				for unit in red_units:
					if unit.rect.collidepoint(x,y) and turn == "red" and unit.team == "red":
						selected_unit.deselect()
						selected_unit = unit
						selected_unit.select()
						flag = True

				if not flag:
					for unit in blue_units:
						if unit.rect.collidepoint(x,y) and turn == "blue" and unit.team == "blue":
							selected_unit.deselect()
							selected_unit = unit
							selected_unit.select()
				print selected_unit.AP

        tiles.draw(screen)
        doors.draw(screen)
        red_units.draw(screen)
        blue_units.draw(screen)
		if not blue_units.sprites() and red_units.sprites():
			print "RED WINS!"
			break
		elif not red_units.sprites() and blue_units.sprites():
			print "BLUE WINS!"
			break
        pygame.display.flip()
        pass