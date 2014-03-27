#!/usr/bin/python

import socket
import connection
from threading import Thread

import os, sys
import pygame
from pygame.locals import *
from map import Map
from door import Door
from tile import Tile
from unit import Unit

pygame.init() 

host = 'localhost'
port =  5679
key = '70d9573de68a1fa96488b8fbfb9476c8'

finalquit = False

def parse_headers(headers):
    context = {}
    headers = headers.split('\r\n')

    #generate dictionary for headers
    for raw in headers:
        headings = raw.split(': ')
        context[headings[0]] = headings[1]

    return context

def receive_message(connection_layer, pygame, screen, tiles, doors, blue_units, red_units, selected_unit, collidable):
    while True:
        recv_msg = connection_layer.getMessage()

        headers = parse_headers(recv_msg)

        if recv_msg == ('QUIT2 ' + key):
            connection_layer.sendMessage('QUIT3 ' + key + '\r\n\ndate: january')
            connection_layer.disconnect()
            break
        elif 'key' in headers:
            key_pressed = headers['key']
            if ((key_pressed == str(K_RIGHT))
            or (key_pressed == str(K_LEFT))
            or (key_pressed == str(K_UP))
            or (key_pressed == str(K_DOWN))):
                selected_unit.move(int(key_pressed), collidable)
                print 'moved'

            elif (key_pressed == str(K_e)):
                door = selected_unit.openDoor(doors)
                if door:
                    collidable.remove(door)
                    door.open = True
                    door.setDoor()

            if key_pressed == "left_mouse":# and event.button == 1:
                x,y = int(headers['x']), int(headers['y'])

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
        else:
            finalquit = False
        print recv_msg

def get_input(connection_layer):
    while True:
        send_msg = raw_input('')
        send_msg = send_msg.split(' ')

        if send_msg[0] == 'QUIT':
            connection_layer.sendMessage('QUIT ' + key + '\r\n\ndate: january')
            finalquit = True
            break
        elif send_msg[0] == 'TIME':
            connection_layer.sendMessage('TIME\r\n\ndate: january')
        elif send_msg[0] == 'SETUSERNAME':
            connection_layer.sendMessage('SET\r\n\nusername: ' + send_msg[1])
        elif send_msg[0] == 'SETSTATUS':
            connection_layer.sendMessage('SET\r\n\nstatus: ' + send_msg[1])
        elif send_msg[0] == 'SAY':
            connection_layer.sendMessage('SET\r\n\nreceipient: 0\r\nmessage: ' + send_msg[1])   
        elif send_msg[0] == 'SEND':
            connection_layer.sendMessage('SET\r\n\nreceipient: ' + send_msg[1] + '\r\nmessage: ' + send_msg[2]) 
        elif send_msg[0] == 'LISTUSERS':
            connection_layer.sendMessage('GET\r\n\nuser: all')
        else:
            print send_msg[0] + ": command not recognized"

BLACK = (0,0,0)

UnitList = {
    "Rifleman" : {"HP" : 10, "AP" : 10, "attack": 3, "defense" : 0 , "walkCost" : 1, "turnCost" : 0},
    "Heavy Gunner" : {"HP" : 15, "AP" : 10, "attack": 8, "defense" : 2 , "walkCost" : 2, "turnCost" : 1,  "sprite" : "rheavy_down.png"}
}

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
    s = socket.socket()

    s.connect((host, port))

    connection_layer = connection.connection(s)

    print "Client tries to connect to server..."

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

    #start network threads
    receiver_thread = Thread(target=receive_message, args=(connection_layer, pygame, screen, tiles, doors, blue_units, red_units, selected_unit, collidable))
    receiver_thread.start()
    receiver_thread = Thread(target=get_input, args=(connection_layer,))
    receiver_thread.start()

    tiles.draw(screen)
    doors.draw(screen)
    red_units.draw(screen)
    blue_units.draw(screen)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                sys.exit()
            elif event.type == KEYDOWN:
                connection_layer.sendMessage('SET\r\n\nkey: ' + str(event.key))

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x,y = event.pos
                connection_layer.sendMessage('SET\r\n\nmouse: ' + 'left_mouse\r\n' + 'x: ' + str(x) + '\r\ny: ' + str(y))