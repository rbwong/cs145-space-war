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

		#set sprite
		if team == "blue":
			sprite = "blue_unit.png"
			self.direction = K_DOWN
		else:
			sprite = "red_unit.png"
			self.direction = K_UP

		#tile movement rate
		self.x_dist = 50
		self.y_dist = 50

		# pygame
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(os.path.join("images", sprite))
		if rect != None:
			self.rect = rect

		#rotate red
		if team == "red":
			self.image = rot_image = pygame.transform.rotate(self.image, 180)

		# Extrinsic Properties
		self.team = team # "red", "blue"
		self.curHP = self.HP
		self.curAP = self.AP
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

	def interact(self):
		self.AP -= 1	
		
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

	def openDoor(self, doors):
		for door in doors:
			top, bottom = self.rect.top, self.rect.bottom
			left, right = self.rect.left, self.rect.right

			if door.rect.collidepoint(right+25,top+25) and self.direction == K_RIGHT:
				self.interact()
				return door
			elif door.rect.collidepoint(left-25,top+25)  and self.direction == K_LEFT:
				self.interact()
				return door
			elif door.rect.collidepoint(left+25,top-25)  and self.direction == K_UP:
				self.interact()
				return door
			elif door.rect.collidepoint(left+25,bottom+25)  and self.direction == K_DOWN:
				self.interact()
				return door

	def move(self, key, collidable):
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

		#remove self from collidable
		collidable_objects = list(collidable)
		collidable_objects.remove(self)
		collided = False	#check collision
		self.rect.move_ip(xMove,0);

		block_hit_list_x = pygame.sprite.spritecollide(self, collidable_objects, False)
		for block in block_hit_list_x:
			if xMove > 0:
				self.rect.right = block.rect.left
			else:
				self.rect.left = block.rect.right

		self.rect.move_ip(0,yMove);

		block_hit_list_y = pygame.sprite.spritecollide(self, collidable_objects, False)
		for block in block_hit_list_y:
			if yMove > 0:
				self.rect.bottom = block.rect.top
			else:
				self.rect.top = block.rect.bottom
		if not block_hit_list_x and not block_hit_list_y:
			self.interact()

	def select(self):
		if self.team == "blue":
			sprite = "blue_unit_sel.png"
			self.image = pygame.image.load(os.path.join("images", sprite))
			self.image, self.rect = self.rot_unit(self.image, self.rect, K_UP, self.direction)
		else:
			sprite = "red_unit_sel.png"
			self.image = pygame.image.load(os.path.join("images", sprite))
			self.image, self.rect = self.rot_unit(self.image, self.rect, K_UP, self.direction)
			
	def deselect(self):
		if self.team == "blue":
			sprite = "blue_unit.png"
			self.image = pygame.image.load(os.path.join("images", sprite))
			self.image, self.rect = self.rot_unit(self.image, self.rect, K_DOWN, self.direction)
		else:
			sprite = "red_unit.png"
			self.image = pygame.image.load(os.path.join("images", sprite))
			self.image, self.rect = self.rot_unit(self.image, self.rect, K_DOWN, self.direction)

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