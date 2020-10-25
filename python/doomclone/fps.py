import pygame
import sys
import random
import math
import keyboard

#Some random RGB colors
SHADOW = (102, 102, 102)
WHITE = (255, 255, 255)
LIGHTGREEN = (0, 255, 0 )
GREEN = (0, 200, 0 )
BLUE = (0, 0, 128)
LIGHTBLUE= (0, 0, 255)
RED= (200, 0, 0 )
LIGHTRED= (255, 100, 100)
PURPLE = (102, 0, 102)
LIGHTPURPLE= (153, 0, 153)

#PI
pi = 3.1415926535897932


#Game parameters
running = True
game_over = True
sbeve = False
score = 0

#Settings
mapD = 10
sensitivity = 1/20
speed = 0.15

pygame.init()
pygame.font.init()
defaultFont = pygame.font.SysFont('Comic Sans MS', 30)
screen = pygame.display.set_mode((1210,750))
pygame.display.set_caption("Doom clone")
clock = pygame.time.Clock()

#Player class
class Player:
	x = 4.500
	y = 4.500
	AOV = 0
	def rotate(self,dir):
		self.AOV+= dir * pi*sensitivity
	def move(self,dir):
		self.x+= dir[0]*speed
		self.y+= dir[1]*speed
	def __init__(self):
		return
	


#Declare our player
player = Player()

#This is the game map
map = []
map.append([1,1,1,1,1,1,1,1,1,1])
map.append([1,0,0,0,1,0,0,0,0,1])
map.append([1,0,1,0,1,1,0,1,1,1])
map.append([1,0,0,0,1,0,0,1,0,1])
map.append([1,0,0,1,0,0,0,1,0,1])
map.append([1,1,0,0,0,1,0,0,0,1])
map.append([1,0,1,0,1,1,0,1,0,1])
map.append([1,0,0,0,0,1,0,1,0,1])
map.append([1,0,1,1,0,0,0,0,0,1])
map.append([1,1,1,1,1,1,1,1,1,1])

#Find Cartesian equation of a ray
def findEq(slopeAngle,x,y):
	t = math.tan(slopeAngle)
	return(t, y - x * t)
	
#Find intersection of two lines using their equations in Cartesian
#def intersect(a,b):
#	return ((a[1]-b[1])/(b[0]-a[0]), (a[0]*a[1]+b[0]*a[1]-a[0]*b[1]-b[0]*b[1])/(b[0]-a[0]))

#Draw starting screen
def startingScreen():
	global game_over
	screen.fill(WHITE)
	
	#Next four rows are a standard way of drawing text on the screen.
	text = defaultFont.render('DOOM CLONE', False, SHADOW, WHITE)
	textRect = text.get_rect() 
	textRect.center = (300, 150)
	screen.blit(text, textRect)
	
	#Draw text again
	text = defaultFont.render('Press any key to play', False, SHADOW, WHITE)
	textRect = text.get_rect() 
	textRect.center = (300, 300)
	screen.blit(text, textRect)
	
	pygame.display.flip()
	
	#Wait for a key press
	while game_over:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			if event.type == pygame.KEYDOWN:
				game_over = False
				return
		clock.tick(1)

#Draw what player sees		
def drawVision(player, map):
	screen.fill(WHITE)
	for i in range(0,46):
		#Ray casting
		currAngle = player.AOV + i*pi/180
		if currAngle != pi/2 and currAngle != -pi/2:
			slope = math.tan(currAngle)
		for j in range(1,7):
			print(1)
			wally = math.floor(player.y+j/2*math.sin(player.AOV-i*pi/180))
			wallx = math.floor(player.x+j/2*math.cos(player.AOV-i*pi/180))
			pygame.draw.rect(screen, SHADOW, (600-i*20,0,20,750))
			if map[math.floor(wally)][math.floor(wallx)]==1:
				if currAngle != pi/2 and currAngle!= -pi/2 and currAngle != 0 and currAngle != pi: 
					#intersect ray with y = wally
					pair1 = (player.x + (wally  - player.y)/slope, wally )
					#intersect ray with x = wallx + 1
					pair2 = (wallx + 1, slope * (wallx + 1 - player.x) + player.y)
					print('pair1 ', pair1)
					print('wallx ', wallx)
					if pair1[0] <= wallx or pair1[0]>=wallx+1: pair1 = pair2
				elif currAngle != pi/2 or currAngle!= -pi/2: pair1 = (wallx, player.y)
				else: pair1 = (player.x, wally)
				print()
				print('pair1 ', pair1)
				print('currAngle ', currAngle)
				print('dist ', math.sqrt((player.y-pair1[1])**2+(player.x-pair1[0])**2))
				print('slope ', slope)
				print()
				dist = math.sqrt((player.y-pair1[1])**2+(player.x-pair1[0])**2)
				pygame.draw.rect(screen, (228-50*dist,0,228-50*dist), (600+i*20-10,0,20,750))
				break
		currAngle = player.AOV - i*pi/180
		if currAngle != pi/2 and currAngle != -pi/2:
			slope = math.tan(currAngle)
		for j in range(1,7):
			print(1)
			wally = math.floor(player.y+j/2*math.sin(player.AOV-i*pi/180))
			wallx = math.floor(player.x+j/2*math.cos(player.AOV-i*pi/180))
			pygame.draw.rect(screen, SHADOW, (600+i*20,0,20,750))
			if map[math.floor(wally)][math.floor(wallx)]==1:
				if currAngle != pi/2 and currAngle!= -pi/2 and currAngle != 0 and currAngle != pi: 
					#intersect ray with y = wally
					pair1 = (player.x + (wally  - player.y)/slope, wally )
					#intersect ray with x = wallx + 1
					pair2 = (wallx + 1, slope * (wallx + 1 - player.x) + player.y)
					print('pair1 ', pair1)
					print('wallx ', wallx)
					if pair1[0] <= wallx or pair1[0]>=wallx+1: pair1 = pair2
				elif currAngle != pi/2 or currAngle!= -pi/2: pair1 = (wallx, player.y)
				else: pair1 = (player.x, wally)
				print()
				print('pair1 ', pair1)
				print('currAngle ', currAngle)
				print('dist ', math.sqrt((player.y-pair1[1])**2+(player.x-pair1[0])**2))
				print('slope ', slope)
				print()
				dist = math.sqrt((player.y-pair1[1])**2+(player.x-pair1[0])**2)
				pygame.draw.rect(screen, (228-50*dist,0,228-50*dist), (600+i*20-10,0,20,750))
				break
	pygame.display.flip()
startingScreen()

while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
	if keyboard.is_pressed('Esc'):
		break
	if keyboard.is_pressed('q'):
		player.rotate(1)
	if keyboard.is_pressed('e'):
		player.rotate(-1)
	drawVision(player,map)
	clock.tick(15)