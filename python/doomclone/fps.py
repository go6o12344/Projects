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
BLACK = (0, 0, 0)

#PI
pi = 3.1415926535897932


#Game parameters
running = True
game_over = True
sbeve = False
score = 0
FOV  = pi/3

#Settings
mapD = 10
sensitivity = 1/20
speed = 0.15
windowWidth = 720
windowHeight = 480

pygame.init()
pygame.font.init()
defaultFont = pygame.font.SysFont('Comic Sans MS', 30)
screen = pygame.display.set_mode((windowWidth,windowHeight))
pygame.display.set_caption("Doom clone")
clock = pygame.time.Clock()

#Player class
class Player:
	#Starting coordinates for the player
	x = 1.5
	y = 1.5
	
	#Direction at which the player is looking initially. This is the angle between the leftmost part of the FOV and the X-axis. The player is technically looking at an angle of 0.
	AOV = FOV/2
	
	#Use this variable to store player movement direction. It keeps the sine and the cosine of the angle defined by the movement vector and the X-axis
	direction = [0,0]
	
	#Rotate method for player
	def rotate(self,dir):
		self.AOV+= dir * pi*sensitivity
	
	#Collision check
	def checkCollision(self, map):
		if map[math.floor(self.y + self.direction[1]*speed)][math.floor(self.x + self.direction[1]*speed)]==1:
			return True
		return False
		
	#Move method
	def move(self, map):
		#Check for collision
		if self.checkCollision(map):
			self.direction = [0,0]
			return
		
		#Now move player in current direction
		self.x+= self.direction[0]*speed
		self.y+= self.direction[1]*speed
		
		#Teleportation prototype. It's a bit buggy 
		#if math.floor(self.x)==1 and math.floor(self.y)==1:
		#	self.x = 7
		#	self.y = 7
		#if math.floor(self.x)==8 and math.floor(self.y)==8:
		#	self.x = 2
		#	self.y = 1
		#Reset direction
		self.direction = [0,0]
	def __init__(self):
		return
	


#Declare our player
player = Player()

#This is the game map. 1 means wall, 0 means empty space
map = []
map.append([1,1,1,1,1,1,1,1,1,1])
map.append([1,0,0,0,0,0,0,0,0,1])
map.append([1,0,1,1,0,0,0,0,0,1])
map.append([1,0,1,1,0,0,0,0,0,1])
map.append([1,0,0,0,0,0,0,0,0,1])
map.append([1,0,0,0,0,0,1,1,1,1])
map.append([1,0,0,0,0,0,1,0,1,1])
map.append([1,0,0,0,0,0,1,0,1,1])
map.append([1,0,0,0,0,0,0,0,0,1])
map.append([1,1,1,1,1,1,1,1,1,1])

	
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
	screen.fill(BLACK)
	global windowWidth
	global windowHeight
	
	#This is an approximation of the optimal ceiling wideness. It isn't the best approximation but it works for now. Also I call it wideness for lack of a better word
	min = math.sqrt(2)*120 - 96
	
	#Draw  ceiling and floor. Floor has the same wideness as the ceiling
	pygame.draw.rect(screen, BLUE, (0, 0, windowWidth, (windowHeight-min)/2))
	pygame.draw.rect(screen, RED, (0, (windowHeight+min)/2, windowWidth, (windowHeight-min)/2))
	#Now we draw everything else
	for i in range(0,windowWidth):
		#Ray casting
		
		#We get the angle at which the ray is cast, its sine and its cosine
		currAngle = player.AOV - (i*FOV)/windowWidth
		sinA = math.sin(currAngle)
		cosA = math.cos(currAngle)
		
		#Now trace along the ray for collision with objects
		for j in range(1,96):
			#Check if ray collides with anything, currently we only need to worry about walls
			if map[math.floor(player.y+j*sinA/32)][math.floor(player.x+j*cosA/32)]==1:
				#If it collides, get length of segment to draw on screen
				#This is where shit gets real. If you don't like math you can just call it magic
				#Assume that the image we initially get is the surface of a cylinder (it would actually be a sphere, but this isn't a real 3D game, no need to other with a third dimension)
				#Now get leftmost and rightmost lines on the segment we see (we dont see the whole thing, we have a limited FOV
				#Draw a plane through those two lines (you can always do that, those lines are parallel)
				#Project the surface onto the plane and adjust wrt actual distance. 
				#The best adjustment wrt distance I have found thus far is 8/distance, i cant think of an actual formula for it. You can goof around with it and find a better estimate if you feel like it
				lengthSegment = math.floor(windowHeight*math.cos(FOV/2)/(math.cos(FOV/2-i*FOV/windowWidth))*16/j)
				
				#Draw segment on screen
				pygame.draw.rect(screen, (192-3*j/2,192-3*j/2,192-3*j/2), (i,(windowHeight-lengthSegment)//2,1,lengthSegment))
				break
	pygame.display.flip()
startingScreen()

while running:
	#If the 'X' in the top right corner of the window is pressed, quit
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			break
			
	#If ESC is pressed, quit
	if keyboard.is_pressed('Esc'):
		break
	
	#Rotate player. 'Q' rotates the player left, 'E' rotates right, pressing both cancels them out. This changes the direction in which the player is looking
	if keyboard.is_pressed('q'):
		player.rotate(1)
	if keyboard.is_pressed('e'):
		player.rotate(-1)
		
	#Get player movement direction. 'W' for forward, 'S' for backward, 'A' for left, 'D' for right. 'W' and 'S' cancel eachother out, same for 'A' and 'D'
	if keyboard.is_pressed('w'):
		player.direction[0]+=math.cos(player.AOV - pi/6)
		player.direction[1]+=math.sin(player.AOV - pi/6)
	if keyboard.is_pressed('a'):
		player.direction[0]+=math.cos(player.AOV - pi/6 + pi/2)
		player.direction[1]+=math.sin(player.AOV - pi/6 + pi/2)
	if keyboard.is_pressed('s'):
		player.direction[0]+=math.cos(player.AOV - pi/6 + pi)
		player.direction[1]+=math.sin(player.AOV - pi/6 + pi)
	if keyboard.is_pressed('d'):
		player.direction[0]+=math.cos(player.AOV - pi/6 - pi/2)
		player.direction[1]+=math.sin(player.AOV - pi/6 - pi/2)
		
	#Actually move player
	player.move(map)
	
	#Draw what the player sees
	drawVision(player,map)
	clock.tick(12)