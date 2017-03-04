#I need to have a click function - that gives which ball was clicked. clicked marks the ball and clears the ball then displays the modified 
# board
#I need to have a display board that draws the board on the screen.
from Logic import Board,WHITE,BLACK,RED,BLUE,GREEN
import pygame
import pygame.gfxdraw
import sys
import math
DIAMETER = 32
RADIUS = DIAMETER/2
def drawSquare(size):
    pygame.draw.rect(screen, WHITE, (0,0,size*DIAMETER,size*DIAMETER), 0)
    pygame.display.update()

def drawCircle(radius,position,colour):
    x,y = position
    pygame.gfxdraw.filled_circle(screen, x, y , radius*RADIUS-1, colour )
    pygame.gfxdraw.aacircle(screen, x, y , radius*RADIUS-1, colour )

def drawJoiningSquare(board,side):
    squares = board.joiningSquares(side)
    for square in squares:
        x,y = square.position
        pygame.draw.rect(screen, square.colour, (x*DIAMETER,y*DIAMETER,DIAMETER,DIAMETER), 0)
    #drawJoiningSquare(board,RADIUS)


def display(board):
    drawSquare(board.size)
    for x in range(board.size):
        for y in range(board.size):
            drawCircle(1,(RADIUS+x*DIAMETER,RADIUS+y*DIAMETER), board.balls[x][y].colour)

def getCircle(board,radius):
    x1,y1 = pygame.mouse.get_pos()
    for x in range(board.size):
        for y in range(board.size):
            x2,y2 = RADIUS+x*DIAMETER,RADIUS+y*DIAMETER
            distance = math.hypot(x1 - x2, y1 - y2)
            if distance <= radius and board.balls[int((x2-RADIUS)/DIAMETER)][int((y2-RADIUS)/DIAMETER)].colour!=WHITE:
                return int((x2-RADIUS)/DIAMETER),int((y2-RADIUS)/DIAMETER)
    return None

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((640,640))
    pygame.display.set_caption('Same!')
    board = Board(size=20)
    board.initBoard()
    display(board)
    pygame.display.update()
    while True:
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
            pygame.display.set_caption('Results!')
            pygame.font.init()
            myfont = pygame.font.SysFont('Times New Roman', 30)
            textsurface = myfont.render('Score: %s Moves: %s'%(board.score,board.nmoves), True, (0, 0, 200))
            screen.blit(textsurface,(0,0))
            pygame.display.update()

