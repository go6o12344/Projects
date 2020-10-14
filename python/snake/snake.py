import pygame
import sys
import random

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
score = 0
pygame.init()
pygame.font.init()
defaultFont = pygame.font.SysFont('Comic Sans MS', 30)
screen = pygame.display.set_mode((600,650))
pygame.display.set_caption("Snek")
clock = pygame.time.Clock()

#This draws the starting screen
def startingScreen():
	global game_over
	screen.fill(WHITE)
	text = defaultFont.render('SNAKE', False, SHADOW, WHITE)
	textRect = text.get_rect() 
	textRect.center = (300, 150)
	screen.blit(text, textRect)
	text = defaultFont.render('Press any key to play', False, SHADOW, WHITE)
	textRect = text.get_rect() 
	textRect.center = (300, 300)
	screen.blit(text, textRect)
	pygame.display.flip()
	while game_over:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			if event.type == pygame.KEYDOWN:
				game_over = False
				return
		clock.tick(1)

#This method is used in move to generate a new apple.
def generateApple(board):
	temp = [] #This variable stores all empty fields on the board.
	
	#Next we get all the empty fields on the board inside temp.
	
	for i in range(0,10):
		for j in range(0,10):
			if board[i][j]==0:
				temp.append([i,j])
	temp1 = temp[random.randint(0, len(temp)-1)]
	board[temp1[0]][temp1[1]] = 2

#This method moves the snake (surprise, surprise).
def move(board, snake, direction):
	head = list(map(lambda x,y:x+y, snake[0], direction)) #This is the new head.
	#Check for collision
	if head[0]<0 or head[1]<0 or head[0]>9 or head[1]>9 or board[head[0]][head[1]]==3 or (head in snake and head!=snake[-1]):
		global game_over
		game_over = True
	snake.insert(0, head)
	#Check if apple eaten
	if board[head[0]][head[1]]==2:
		board[head[0]][head[1]] = 1
		generateApple(board)
		global score
		score+=15
		return
	#Remove tail and update snake position on board 
	del snake[-1]
	for i in snake:
		board[i[0]][i[1]]=1

#Game over.
def gameOverScreen(board, snake, direction, lastdirection):
	
	#Here we draw the game over screen.
	global game_over
	global score
	screen.fill(WHITE)
	text = defaultFont.render('GAME OVER!', False, SHADOW, WHITE)
	textRect = text.get_rect() 
	textRect.center = (300, 150)
	screen.blit(text, textRect)
	text = defaultFont.render('Press any key to start over', False, SHADOW, WHITE)
	textRect = text.get_rect() 
	textRect.center = (300, 450)
	screen.blit(text, textRect)
	text = defaultFont.render('Your score was '+ str(score) , False, SHADOW, WHITE)
	textRect = text.get_rect() 
	textRect.center = (300, 350)
	screen.blit(text, textRect)
	pygame.display.flip()
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

#This is where we draw the actual board on-screen for the first time.
generateApple(board)
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
clock.tick(2)
game_over = False
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP and lastdirection!=[0,1]:
				direction = [0,-1]
			if event.key == pygame.K_DOWN and lastdirection!=[0,-1]:
				direction = [0,1]
			if event.key == pygame.K_LEFT and lastdirection!=[1,0]:
				direction = [-1,0]
			if event.key == pygame.K_RIGHT and lastdirection!=[-1,0]:
				direction = [1,0]
	lastdirection = direction
	move(board, snake, direction)
	if(game_over):
		#Here we reset all the variables.
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
		snake = [[4,4],[5,4]]
		direction = [-1,0]
		lastdirection = [-1,0]
		generateApple(board)
		gameOverScreen(board, snake, direction, lastdirection)
		score = 0
		game_over = False
		continue
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
	clock.tick(2)
sys.exit()