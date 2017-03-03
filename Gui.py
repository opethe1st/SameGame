#I need to have a click function - that gives which ball was clicked. clicked marks the ball and clears the ball then displays the modified 
# board
#I need to have a display board that draws the board on the screen.
from Logic import Board
import pygame
import sys
import math
DIAMETER = 30
RADIUS = DIAMETER/2
def drawSquare(size):
    pygame.draw.rect(screen, (255, 255, 255), (0,0,size*DIAMETER,size*DIAMETER), 0)
    pygame.display.update()
    pass #Some pygame functions

def drawCircle(radius,position,colour):
    x,y = position
    pygame.draw.circle(screen, colour, (x,y), radius*RADIUS, 6)
    pass #Some pygame functions

def display(board):
    drawSquare(board.size)
    for x in range(board.size):
        for y in range(board.size):
            drawCircle(1,(RADIUS+x*DIAMETER,RADIUS+y*DIAMETER), board.balls[x][y].colour)

def getClickedCircle(board,radius):
    x1,y1 = pygame.mouse.get_pos()
    for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                x1,y1 = pygame.mouse.get_pos()
                for x in range(board.size):
                    for y in range(board.size):
                        x2,y2 = RADIUS+x*DIAMETER,RADIUS+y*DIAMETER
                        distance = math.hypot(x1 - x2, y1 - y2)
                        if distance <= radius:
                            return int((x2-RADIUS)/DIAMETER),int((y2-RADIUS)/DIAMETER)
    
    
    return None

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((600,600),32)
    #info = pygame.display.Info()
    #print info
    board = Board(size=20)
    board.initBoard()
    while not board.isGameOver():
        display(board)
        pygame.display.update()
        position = getClickedCircle(board,radius=RADIUS)
        if position: #board position or 
            board.markBalls(position)
            board.clearBalls()

        for event in pygame.event.get():
            #print event.type
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

