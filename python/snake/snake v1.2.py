import pygame
import sys
import random
import requests
import urllib.request
import time
from bs4 import BeautifulSoup

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
running = True
game_over = True
sbeve = False
score = 0
pygame.init()
pygame.font.init()
defaultFont = pygame.font.SysFont('Comic Sans MS', 30)
screen = pygame.display.set_mode((600,650))
pygame.display.set_caption("Snek")
clock = pygame.time.Clock()

#Function to get the latest Covid-19 daily cases statistics for Bulgaria. I have no idea what the code does, but it works somehow. This clearly shows the power of stackoverflow.
def covid19():
	url = 'https://coronavirus.bg/bg/news'
	response = requests.get(url)
	soup = BeautifulSoup(response.text, "html.parser")
	t = []
	for a in soup.findAll('a', href=True, ):
		t.append(a.text.split('\n'))
	for i in t:
		print(i)
	for i in range(54, 67):
		if t[i][0] == 'Прочетете повече':
			continue
		if ord(t[i][2][0]) in range(48, 58):
			date = t[i][1]
			count = t[i][2].split()[0]
			return [date, count]

#Get latest covid stats for Bulgaria. We just call the method defined above.
covid = covid19()

#This draws the starting screen
def startingScreen():
	global game_over
	screen.fill(WHITE)
	
	#Next four rows are a standard way of drawing text on the screen.
	text = defaultFont.render('SNAKE', False, SHADOW, WHITE)
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

#This method is used in move to generate a new apple.
def generateApple(board, snake):
	temp = [] #This variable stores all empty fields on the board.
	
	#Next we get all the empty fields on the board inside temp.
	for i in range(0,10):
		for j in range(0,10):
			if board[i][j]==0 and [i,j] not in snake:
				temp.append([i,j])
				print((i,j))
	temp1 = temp[random.randint(0, len(temp)-1)] #Select one random empty field
	board[temp1[0]][temp1[1]] = 2 #Place an apple on the empty field. Apples are represented with a '2' on the board

#This method moves the snake (surprise, surprise).
def move(board, snake, direction):
	global score
	head = list(map(lambda x,y:x+y, snake[0], direction)) #This is the new head.
	
	#Check for collision. Either with board borders or the obstacles on the board (obstacles are represented with a '3' on the board)
	if head[0]<0 or head[1]<0 or head[0]>9 or head[1]>9 or board[head[0]][head[1]]==3: #or (head in snake and head!=snake[-1]):
		global game_over
		game_over = True
	#Check if snak eats itself
	if head in snake and head!=snake[-1]:
		for j in range(0,len(snake)-1) : #Find which piece of itself the snake bit
			if snake[j] == head:
				#reduce score
				score-=j*15-15
				
				#Remove the part of the snake that was bitten off
				for _ in range(0,len(snake)-j):
					del snake[j]
				#Insert head
				snake.insert(0,head)
				print(snake) #Debug output
				return
	#add head. this can be done a few rows earlier but messes up the logic in snake eats itself case and im too lazy to fix it
	snake.insert(0, head)
	
	#Check if apple eaten
	if board[head[0]][head[1]]==2:
		board[head[0]][head[1]]=0
		generateApple(board, snake)
		score+=15
		return
	#Remove tail
	del snake[-1]

#Sbeve mode
def faster(board, snake, direction, lastdirection):
	global running
	global game_over
	global sbeve
	global score
	global SHADOW
	global WHITE
	global LIGHTGREEN
	global GREEN
	global BLUE 
	global LIGHTBLUE
	global RED
	global LIGHTRED
	global PURPLE
	global LIGHTPURPLE
	while running:
		#Listen for input
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False #stop game if the 'X' on top right is pressed
			#Get direction
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP and lastdirection!=[0,1]:
					direction = [0,-1]
					sbeve = True
				if event.key == pygame.K_DOWN and lastdirection!=[0,-1]:
					direction = [0,1]
					sbeve = True
				if event.key == pygame.K_LEFT and lastdirection!=[1,0]:
					direction = [-1,0]
					sbeve = True
				if event.key == pygame.K_RIGHT and lastdirection!=[-1,0]:
					direction = [1,0]
					sbeve = True
			#Check if a button is held down. This can potentially be exploited but im too lazy to fix it
			if event.type == pygame.KEYUP:
				sbeve = False
		#All the lastdirection shenanigans prevent U-turns. It sometimes causes the snake to go the wrong way though
		lastdirection = direction
		#Move snake
		move(board, snake, direction)
		#Check if snake died
		if(game_over):
			#Here we reset all the variables.
			board = []
			board.append([0,0,0,0,0,0,0,0,0,0])
			board.append([0,3,3,3,0,0,3,3,3,0])
			board.append([0,3,0,0,0,0,0,0,3,0])
			board.append([0,3,0,0,0,0,0,0,3,0])
			board.append([0,0,0,0,0,0,0,0,0,0])
			board.append([0,0,0,0,0,0,0,0,0,0])
			board.append([0,3,0,0,0,0,0,0,3,0])
			board.append([0,3,0,0,0,0,0,0,3,0])
			board.append([0,3,3,3,0,0,3,3,3,0])
			board.append([0,0,0,0,0,0,0,0,0,0])
			snake = [[4,4],[5,4]]
			direction = [-1,0]
			lastdirection = [-1,0]
			generateApple(board,snake)
			
			#Draw the game over screen
			gameOverScreen(board, snake, direction, lastdirection)
			
			#Start a new game after a key press on the end game screen
			score = 0
			game_over = False
			continue
			
		#Draw the board
		screen.fill(WHITE)
		
		#First we display the score on top of the board
		text = defaultFont.render('Score: ' + str(score), False, SHADOW, WHITE)
		textRect = text.get_rect() 
		textRect.center = (300, 25)
		screen.blit(text, textRect)
		
		#Then we draw the board
		pygame.draw.rect(screen, (0,127,0), (snake[0][0]*60, 50+snake[0][1]*60, 60, 60))
		for i in range(1,len(snake)):
			pygame.draw.rect(screen, (0,127+i,0), (snake[i][0]*60, 50+snake[i][1]*60, 60, 60))
		for i in range(0,10):
			for j in range(0,10):
				if board[i][j]==2:
					pygame.draw.circle(screen, RED, (i*60+30, 50+j*60+30), 25)
				elif board[i][j]==3:
					pygame.draw.rect(screen, SHADOW, (i*60, 50+j*60, 60, 60))
		pygame.display.flip()
		
		#If snake is not in fast mode we break out of fast mode
		if sbeve == False:
			return
			
		#Run at 4 frames per second
		clock.tick(4)
		
#Game over.
def gameOverScreen(board, snake, direction, lastdirection):
	
	#Here we draw the game over screen.
	global game_over
	global score
	global covid
	screen.fill(WHITE)
	
	#Text
	text = defaultFont.render('GAME OVER!', False, SHADOW, WHITE)
	textRect = text.get_rect() 
	textRect.center = (300, 150)
	screen.blit(text, textRect)
	
	#More text
	text = defaultFont.render('Press any key to start over', False, SHADOW, WHITE)
	textRect = text.get_rect() 
	textRect.center = (300, 350)
	screen.blit(text, textRect)
	
	#Even more text. This one displays the score
	text = defaultFont.render('Your score was '+ str(score) , False, SHADOW, WHITE)
	textRect = text.get_rect() 
	textRect.center = (300, 250)
	screen.blit(text, textRect)
	
	#This shows some covid-19 stats
	text = defaultFont.render('На '+ covid[0] +' има ', False, SHADOW, WHITE)
	textRect = text.get_rect() 
	textRect.center = (300, 450)
	screen.blit(text, textRect)
	
	#And it is actually split on two rows, it's too long for just one
	text = defaultFont.render(covid[1] + ' нови случая на Covid-19 у нас.', False, SHADOW, WHITE)
	textRect = text.get_rect() 
	textRect.center = (300, 550)
	screen.blit(text, textRect)
	pygame.display.flip()
	
	#Listen for input
	while game_over:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			if event.type == pygame.KEYDOWN:
				return
		clock.tick(1)

#Initialize the board 
board = []
board.append([0,0,0,0,0,0,0,0,0,0])
board.append([0,3,3,3,0,0,3,3,3,0])
board.append([0,3,0,0,0,0,0,0,3,0])
board.append([0,3,0,0,0,0,0,0,3,0])
board.append([0,0,0,0,1,1,0,0,0,0])
board.append([0,0,0,0,0,0,0,0,0,0])
board.append([0,3,0,0,0,0,0,0,3,0])
board.append([0,3,0,0,0,0,0,0,3,0])
board.append([0,3,3,3,0,0,3,3,3,0])
board.append([0,0,0,0,0,0,0,0,0,0])

#Declare our snake. This snake starts at (4,4),(4,5). You can change the starting position of the snake if you want.
snake = [[4,4],[5,4]]
direction = [-1,0] #This is the initial direction of the snake. We keep it in a list just so we can add it to the head element-wise.
lastdirection = [-1,0] #We need to remember this to prevent the player from U-turning.

#Starting screen
startingScreen()

#This is where we draw the actual board on-screen for the first time. But first we need to generare an apple
generateApple(board, snake)
screen.fill(WHITE)

#This displays the score right above the board
text = defaultFont.render('Score: ' + str(score), False, SHADOW, WHITE)
textRect = text.get_rect() 
textRect.center = (300, 25)
screen.blit(text, textRect)

#This draws the snake
pygame.draw.rect(screen, (0,127,0), (snake[0][0]*60, 50+snake[0][1]*60, 60, 60))
for i in range(1,len(snake)):
	pygame.draw.rect(screen, (0,127+i,0), (snake[i][0]*60, 50+snake[i][1]*60, 60, 60))
	
#This draws the rest of the board, more precisely the apple and the obstacles
for i in range(0,10):
	for j in range(0,10):
		if board[i][j]==2:
			pygame.draw.circle(screen, RED, (i*60+30, 50+j*60+30), 25)
		elif board[i][j]==3:
			pygame.draw.rect(screen, SHADOW, (i*60, 50+j*60, 60, 60))
pygame.display.flip()

#Run at two frames per second
clock.tick(2)

game_over = False
while running:

	#Check for speed mode
	if sbeve == True:
		faster(board, snake, direction, lastdirection)
		clock.tick(2)
		continue
	#Listen for input
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP and lastdirection!=[0,1]:
				direction = [0,-1]
				sbeve = True
			if event.key == pygame.K_DOWN and lastdirection!=[0,-1]:
				direction = [0,1]
				sbeve = True
			if event.key == pygame.K_LEFT and lastdirection!=[1,0]:
				direction = [-1,0]
				sbeve = True
			if event.key == pygame.K_RIGHT and lastdirection!=[-1,0]:
				direction = [1,0]
				sbeve = True
		if event.type == pygame.KEYUP:
			sbeve = False
	lastdirection = direction
	
	#Move the snake
	move(board, snake, direction)
	
	if(game_over):
		#Here we reset all the variables.
		board = []
		board.append([0,0,0,0,0,0,0,0,0,0])
		board.append([0,3,3,3,0,0,3,3,3,0])
		board.append([0,3,0,0,0,0,0,0,3,0])
		board.append([0,3,0,0,0,0,0,0,3,0])
		board.append([0,0,0,0,0,0,0,0,0,0])
		board.append([0,0,0,0,0,0,0,0,0,0])
		board.append([0,3,0,0,0,0,0,0,3,0])
		board.append([0,3,0,0,0,0,0,0,3,0])
		board.append([0,3,3,3,0,0,3,3,3,0])
		board.append([0,0,0,0,0,0,0,0,0,0])
		snake = [[4,4],[5,4]]
		direction = [-1,0]
		lastdirection = [-1,0]
		generateApple(board,snake)
		gameOverScreen(board, snake, direction, lastdirection)
		score = 0
		game_over = False
		continue
	
	#Draw the board. It's literally the same code as above.
	screen.fill(WHITE)
	text = defaultFont.render('Score: ' + str(score), False, SHADOW, WHITE)
	textRect = text.get_rect() 
	textRect.center = (300, 25)
	screen.blit(text, textRect)
	pygame.draw.rect(screen, (0,127,0), (snake[0][0]*60, 50+snake[0][1]*60, 60, 60))
	for i in range(1,len(snake)):
		pygame.draw.rect(screen, (0,127+i,0), (snake[i][0]*60, 50+snake[i][1]*60, 60, 60))
	for i in range(0,10):
		for j in range(0,10):
			if board[i][j]==2:
				pygame.draw.circle(screen, RED, (i*60+30, 50+j*60+30), 25)
			elif board[i][j]==3:
				pygame.draw.rect(screen, SHADOW, (i*60, 50+j*60, 60, 60))
	pygame.display.flip()
	
	#FPS:2
	clock.tick(2)
sys.exit()