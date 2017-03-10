#I need to have a click function - that gives which ball was clicked. clicked marks the ball and clears the ball then displays the modified 
# board
#I need to have a display board that draws the board on the screen.
from Logic import Board,WHITE,BLACK,RED,BLUE,GREEN
import pygame
import pygame.gfxdraw
import sys
import math
import os

if getattr(sys, 'frozen', False):
    # we are running in a bundle
    basedir = sys._MEIPASS
else:
    # we are running in a normal Python environment
    basedir = '.'

DIAMETER = 32
RADIUS = DIAMETER/2
currentScore = 0
GameOver = False


def drawSquare(width,height):
    pygame.draw.rect(screen, WHITE, (0,0,width*DIAMETER,height*DIAMETER), 0)
    pygame.display.update()

def drawCircle(radius,position,colour):
    x,y = position
    pygame.gfxdraw.filled_circle(screen, x, y , radius*RADIUS-2, colour )
    pygame.gfxdraw.aacircle(screen, x, y , radius*RADIUS-2, colour )

def drawJoiningSquare(board,side):
    squares = board.joiningSquares(side)
    for square in squares:
        x,y = square.position
        pygame.draw.rect(screen, square.colour, (x*DIAMETER+2,y*DIAMETER+2,DIAMETER-3,DIAMETER-3), 0)
    #drawJoiningSquare(board,RADIUS)


def display(board):
    drawSquare(board.width,board.height)
    for x in range(board.width):
        for y in range(board.height):
            if board.balls[x][y]:
                drawCircle(1,(RADIUS+x*DIAMETER,RADIUS+y*DIAMETER), board.balls[x][y].colour)
    drawJoiningSquare(board,RADIUS)
    displayscore(board)

def getCircle(board,radius):
    x1,y1 = pygame.mouse.get_pos()
    for x in range(board.width):
        for y in range(board.height):
            x2,y2 = RADIUS+x*DIAMETER,RADIUS+y*DIAMETER
            distance = math.hypot(x1 - x2, y1 - y2)
            if distance <= radius and board.balls[int((x2-RADIUS)/DIAMETER)][int((y2-RADIUS)/DIAMETER)]:
                return int((x2-RADIUS)/DIAMETER),int((y2-RADIUS)/DIAMETER)
    return None

def displayscore(board):
    global currentScore
    pygame.draw.rect(screen, (150,150,150), (0,512,640,48), 0)
    pygame.font.init()
    myfont = pygame.font.Font(basedir + os.sep + "Fonts/angrybirds-regular.ttf", 24)
    textsurface = myfont.render(' Score: %s Moves: %s Current move: %s Top Score: %s'%(board.score,board.nmoves,currentScore,board.highScore), 1, BLACK,(150,150,150)).convert()
    screen.blit(textsurface,(1,515))
    pygame.display.update()


if __name__ == "__main__":
    WIDTH = 20
    HEIGHT =16
    SCREEN_WIDTH = DIAMETER*WIDTH
    SCREEN_HEIGHT = DIAMETER*HEIGHT + 48
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    pygame.display.set_caption('Same!')
    board = Board(width=20,height=16)
    board.initBoard()
    display(board)
    pygame.display.update()
    while True:
        position = getCircle(board,radius=RADIUS)
        if position and not GameOver:
            currentScore = len(board.findAdjacentBalls(position))**2
            displayscore(board)
            pygame.display.update()
        
        for event in pygame.event.get():
            if event.type==pygame.MOUSEBUTTONDOWN:
                position = getCircle(board,radius=RADIUS)
                if position:
                    board.markBalls(position)
                    board.clearBalls()
                    display(board)
                    pygame.display.update()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if board.isGameOver():
            GameOver = True
            pygame.font.init()
            myfont = pygame.font.Font(basedir + os.sep + "Fonts/angrybirds-regular.ttf", 50)
            textsurface = myfont.render('GAME OVER !!', 1, BLACK)
            text_rect = textsurface.get_rect(center=(SCREEN_WIDTH/2, (SCREEN_HEIGHT-48)/2))
            screen.blit(textsurface,text_rect)
            pygame.draw.rect(screen, (150,150,150), (0,512,640,48), 0)
            pygame.font.init()
            myfont = pygame.font.Font(basedir + os.sep + "Fonts/angrybirds-regular.ttf", 24)
            textsurface = myfont.render('Your Score: %s Top Score: %s '%(board.score,board.highScore), 1, BLACK,(150,150,150)).convert()
            screen.blit(textsurface,(1,515))
            pygame.display.update()
            pygame.display.update()

