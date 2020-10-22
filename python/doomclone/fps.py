import pygame
import sys
import random
import math
import keyboard

#Some random RGB colors
SHADOW = (192, 192, 192)
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
	x = 1.000
	y = 1.000
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
map.append([1,8,0,0,1,0,0,0,0,1])
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
	
	
#Find intersection of two lines using their equations in Cartesian
def intersect(a,b,c,d):
	return ((b-d)/(c-a), (a*b+c*b-a*d-c*d)/(c-a))
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
	for i in range(0,61):
		#Ray casting
		for j in range(1,3):
			wallx = math.floor(player.y+j*math.sin(player.AOV+i*pi/180))
			wally = math.floor(player.x+j*math.cos(player.AOV+i*pi/180))
			pygame.draw.rect(screen, SHADOW, (600-i*10,0,10,750))
			if map[wally][wallx]==1:
				if(intersect(
					pygame.draw.rect(screen, (128*math.sqrt((player.y-wallx)**2+(player.x-wally)**2),0,128*math.sqrt((player.y-wallx)**2+(player.x-wally)**2)), (600-i*10,0,10,750))
				break
		for j in range(1,3):
			wallx = math.floor(player.y+j*math.sin(player.AOV-i*pi/180))
			wally = math.floor(player.x+j*math.cos(player.AOV-i*pi/180))
			pygame.draw.rect(screen, SHADOW, (610+i*10,0,10,750))
			if map[wally][wallx]==1:
				pygame.draw.rect(screen, (128*math.sqrt((player.y-wallx)**2+(player.x-wally)**2),0,128*math.sqrt((player.y-wallx)**2+(player.x-wally)**2)), (610+i*10-10,0,10,750))
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
	elif keyboard.is_pressed('e'):
		player.rotate(-1)
	drawVision(player,map)
	clock.tick(15)