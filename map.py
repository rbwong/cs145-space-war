import pygame

BLACK = (0,0,0)
black = pygame.image.load("black.png")
floor = pygame.image.load("floor.png")
door_ch = pygame.image.load("door_ch.png")
door_oh = pygame.image.load("door_oh.png")
door_cv = pygame.image.load("door_cv.png")
door_ov = pygame.image.load("door_ov.png")
rheavy_up = pygame.image.load("rheavy_up.png")
rheavy_down = pygame.image.load("rheavy_down.png")
rheavy_left = pygame.image.load("rheavy_left.png")
rheavy_right = pygame.image.load("rheavy_right.png")
bheavy_up = pygame.image.load("bheavy_up.png")
bheavy_down = pygame.image.load("bheavy_down.png")
bheavy_left = pygame.image.load("bheavy_left.png")
bheavy_right = pygame.image.load("bheavy_right.png")
song1 = 'LetItGo.wav'

map_width = 15
map_height = 15
pix_width = 50
pix_height = 50
margin = 1
player_turn = 1

with open("map.txt") as myfile: #load map from txt
	grid = [row.split(";") for row in myfile]

pygame.init()
# Set the pix_height and pix_width of the screen
size = [map_width*margin+map_width*pix_width, map_height*margin+map_height*pix_height]
screen = pygame.display.set_mode(size)
# Set title of screen
pygame.display.set_caption("Space Crusade")
#Loop until the user clicks the close button.
done = False
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
screen.fill(BLACK)

for row in range(map_width):
	for column in range(map_height):
		screen.blit(floor,((margin+column*(pix_width+margin)),(margin+row*(pix_height+margin))))
#pygame.mixer.init()
#pygame.mixer.music.load(song1)
#pygame.mixer.music.play()'''

while done == False:
	for event in pygame.event.get(): # User did something
		if event.type == pygame.QUIT: # If user clicked close
			done = True # Flag that we are done so we exit this loop
		elif event.type == pygame.MOUSEBUTTONDOWN:
			# User clicks the mouse. Get the position
			pos = pygame.mouse.get_pos()
			# Change the x/y screen coordinates to grid coordinates
			column = pos[0] // (pix_width + margin)
			row = pos[1] // (pix_height + margin)
			print str(column)+" "+str(row)
			# Set that location to zero
			if player_turn == 1:
				print grid[row][column]
				if grid[row][column] == "6":
					grid[row][column] = "7"
			elif player_turn == 2:
				if grid[row][column] == "10":
					grid[row][column] = "11"
				
	for row in range(map_width): #updates map
		for column in range(map_height):
			if grid[row][column] == "0":
				screen.blit(black,((margin+column*(pix_width+margin)),(margin+row*(pix_height+margin))))
			elif grid[row][column] == "1":
				screen.blit(floor,((margin+column*(pix_width+margin)),(margin+row*(pix_height+margin))))
			elif grid[row][column] == "2":
				screen.blit(floor,((margin+column*(pix_width+margin)),(margin+row*(pix_height+margin))))
				screen.blit(door_ch,((margin+column*(pix_width+margin)),(margin+row*(pix_height+margin))))
			elif grid[row][column] == "3":
				screen.blit(floor,((margin+column*(pix_width+margin)),(margin+row*(pix_height+margin))))
				screen.blit(door_oh,((margin+column*(pix_width+margin)),(margin+row*(pix_height+margin))))
			elif grid[row][column] == "4":
				screen.blit(floor,((margin+column*(pix_width+margin)),(margin+row*(pix_height+margin))))
				screen.blit(door_cv,((margin+column*(pix_width+margin)),(margin+row*(pix_height+margin))))
			elif grid[row][column] == "5":
				screen.blit(floor,((margin+column*(pix_width+margin)),(margin+row*(pix_height+margin))))
				screen.blit(door_ov,((margin+column*(pix_width+margin)),(margin+row*(pix_height+margin))))
			elif grid[row][column] == "6":
				screen.blit(floor,((margin+column*(pix_width+margin)),(margin+row*(pix_height+margin))))
				screen.blit(rheavy_up,((margin+column*(pix_width+margin)),(margin+row*(pix_height+margin))))
			elif grid[row][column] == "7":
				screen.blit(floor,((margin+column*(pix_width+margin)),(margin+row*(pix_height+margin))))
				screen.blit(rheavy_down,((margin+column*(pix_width+margin)),(margin+row*(pix_height+margin))))
			elif grid[row][column] == "8":
				screen.blit(floor,((margin+column*(pix_width+margin)),(margin+row*(pix_height+margin))))
				screen.blit(rheavy_right,((margin+column*(pix_width+margin)),(margin+row*(pix_height+margin))))
			elif grid[row][column] == "9":
				screen.blit(floor,((margin+column*(pix_width+margin)),(margin+row*(pix_height+margin))))
				screen.blit(rheavy_left,((margin+column*(pix_width+margin)),(margin+row*(pix_height+margin))))
			elif grid[row][column] == "10":
				screen.blit(floor,((margin+column*(pix_width+margin)),(margin+row*(pix_height+margin))))
				screen.blit(bheavy_up,((margin+column*(pix_width+margin)),(margin+row*(pix_height+margin))))
			elif grid[row][column] == "11":
				screen.blit(floor,((margin+column*(pix_width+margin)),(margin+row*(pix_height+margin))))
				screen.blit(bheavy_down,((margin+column*(pix_width+margin)),(margin+row*(pix_height+margin))))
			elif grid[row][column] == "12":
				screen.blit(floor,((margin+column*(pix_width+margin)),(margin+row*(pix_height+margin))))
				screen.blit(bheavy_right,((margin+column*(pix_width+margin)),(margin+row*(pix_height+margin))))
			elif grid[row][column] == "13":
				screen.blit(floor,((margin+column*(pix_width+margin)),(margin+row*(pix_height+margin))))
				screen.blit(bheavy_left,((margin+column*(pix_width+margin)),(margin+row*(pix_height+margin))))
	
	
	# Limit to 20 frames per second
	clock.tick(20)
	pygame.display.flip()
	if player_turn == 1:
		player_turn += 1
	elif player_turn == 2:
		player_turn -= 1
pygame.quit()
