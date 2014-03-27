import os, sys
import pygame
from pygame.locals import *

class Door(pygame.sprite.Sprite):
	def __init__(self, rect,orientation="horizontal"):
		self.open = False

		self.orientation = orientation
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(os.path.join("images", ("door_o.png" if self.open else "door_c.png")))
		
		if orientation == "vertical":
			self.image = pygame.transform.rotate(self.image,90)
		if rect != None:
			self.rect = rect

	def setDoor(self):
		self.image = pygame.image.load(os.path.join("images", ("door_o.png" if self.open else "door_c.png")))

		if self.orientation == "vertical":
			self.image = pygame.transform.rotate(self.image,90)