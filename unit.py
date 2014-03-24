import os, sys
import pygame
from pygame.locals import *

class Unit(pygame.sprite.Sprite):
    def __init__(self, rect, unitName, unitDef, team):
        # Intrinsic Properties
        self.name = unitName
        self.HP = unitDef["HP"]
        self.AP = unitDef["AP"]
        self.attack = unitDef["attack"]
        self.defense = unitDef["defense"]
        self.walkCost = unitDef["walkCost"]
        self.turnCost = unitDef["turnCost"]

        self.x_dist = 51
        self.y_dist = 51

        # pygame
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join("images", unitDef["sprite"]))
        if rect != None:
            self.rect = rect

        # Extrinsic Properties
        self.team = team # "red", "blue"
        self.curHP = self.HP
        self.curAP = self.AP
        self.direction = K_DOWN # "up", "down", "left", "right"
        self.x = -1
        self.y = -1
        self.overwatch = False

        # Future features
        self.equipment = {"Head" : None,
                          "Body" : None,
                          "Hand1" : None,
                          "Hand2" : None,
                          "Legs" : None,
                          "Mount" : None}
        self.items = None 

    def totalAttack(self):
        bonusAttack = 0 # total bonus attack from items, etc.
        return self.attack + bonusAttack

    def totalDefense(self):
        bonusDefense = 0 # total bonus defense from items, etc.
        return self.defense + bonusDefense

    def attackEnemy(self, enemy):
        #TODO check for friendly fire (self.team == enemy.team)

        # calculate damage
        damage = self.totalAttack() - enemy.totalDefense()
        # Deal a minimum damage of 1 if attack <= enemy defense
        targetHP = enemy.curHP - (damage if damage > 0 else 1)
        # Prevent negative HP
        enemy.curHP = targetHP if targetHP > 0 else 0


    def move(self, key):
        """Move your self in one of the 4 directions according to key"""
        """Key is the pyGame define for either up,down,left, or right key
        we will adjust outselfs in that direction"""
        xMove = 0;
        yMove = 0;
        
        if (key == K_RIGHT):
            self.image, self.rect = self.rot_unit(self.image, self.rect, self.direction, key)
            xMove = self.x_dist
        elif (key == K_LEFT):
            self.image, self.rect = self.rot_unit(self.image, self.rect, self.direction, key)
            xMove = -self.x_dist
        elif (key == K_UP):
            self.image, self.rect = self.rot_unit(self.image, self.rect, self.direction, key)
            yMove = -self.y_dist
        elif (key == K_DOWN):
            self.image, self.rect = self.rot_unit(self.image, self.rect, self.direction, key)
            yMove = self.y_dist
        #self.rect = self.rect.move(xMove,yMove);
        self.rect.move_ip(xMove,yMove);


    def rot_unit(self, image, rect, direction, next_move):
        """rotate an image while keeping its center"""
        if not next_move == direction:
            #direction = KDOWN
            if direction == K_DOWN and next_move == K_UP:
                rot_image = pygame.transform.rotate(image, 180)
            elif direction == K_DOWN and next_move == K_RIGHT:
                rot_image = pygame.transform.rotate(image, 90)
            elif direction == K_DOWN and next_move == K_LEFT:
                rot_image = pygame.transform.rotate(image, 270)

            #direction = KUP
            if direction == K_UP and next_move == K_DOWN:
                rot_image = pygame.transform.rotate(image, 180)
            elif direction == K_UP and next_move == K_RIGHT:
                rot_image = pygame.transform.rotate(image, 270)
            elif direction == K_UP and next_move == K_LEFT:
                rot_image = pygame.transform.rotate(image, 90)

            #direction = KLEFT
            if direction == K_LEFT and next_move == K_UP:
                rot_image = pygame.transform.rotate(image, 270)
            elif direction == K_LEFT and next_move == K_RIGHT:
                rot_image = pygame.transform.rotate(image, 180)
            elif direction == K_LEFT and next_move == K_DOWN:
                rot_image = pygame.transform.rotate(image, 90)

            #direction = KRIGHT
            if direction == K_RIGHT and next_move == K_UP:
                rot_image = pygame.transform.rotate(image, 90)
            elif direction == K_RIGHT and next_move == K_DOWN:
                rot_image = pygame.transform.rotate(image, 270)
            elif direction == K_RIGHT and next_move == K_LEFT:
                rot_image = pygame.transform.rotate(image, 180)

            self.direction = next_move
        else:
            rot_image = image
        return rot_image,rect


UnitList = {"Rifleman" : {"HP" : 10, "AP" : 10, "attack": 3, "defense" : 0 , "walkCost" : 1, "turnCost" : 0},
            "Heavy Gunner" : {"HP" : 15, "AP" : 10, "attack": 8, "defense" : 2 , "walkCost" : 2, "turnCost" : 1,  "sprite" : "rheavy_up.png"}}

if __name__ == "__main__":
    gunner1 = Unit(unitName="Heavy Gunner", unitDef=UnitList["Heavy Gunner"], team="red")
    gunner2 = Unit(unitName="Heavy Gunner", unitDef=UnitList["Heavy Gunner"], team="blue")
    gunner1.attackEnemy(gunner2)
    print "gunner2 HP:", str(gunner2.curHP)+"/"+str(gunner2.HP)