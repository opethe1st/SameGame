#I need to have a click function - that gives which ball was clicked. clicked marks the ball and clears the ball then displays the modified 
# board
#I need to have a display board that draws the board on the screen.
from Logic import Board,WHITE,BLACK,RED,BLUE,GREEN
import pygame
import pygame.gfxdraw
import sys
import math
import os

GREY = (150,150,150)
#These are the settings for pyinstaller
if getattr(sys, 'frozen', False):
    # we are running in a bundle
    basedir = sys._MEIPASS
else:
    # we are running in a normal Python environment
    basedir = '.'



class GameDisplay:
    def __init__(self):
        self.DIAMETER = 32 #size of the balls
        self.RADIUS = self.DIAMETER/2
        self.GameOver = False
        self.WIDTH = 20
        self.HEIGHT =16
        self.SCOREBOARD_HEIGHT = 48
        self.GAME_HEIGHT = self.DIAMETER*self.HEIGHT
        self.SCREEN_WIDTH = self.DIAMETER*self.WIDTH
        self.SCREEN_HEIGHT = self.GAME_HEIGHT + self.SCOREBOARD_HEIGHT
        
        pygame.init()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH,self.SCREEN_HEIGHT))
        pygame.display.set_caption('Same!')
        self.board = Board(width=self.WIDTH,height=self.HEIGHT)

    def _drawSquare(self,width,height):
        pygame.draw.rect(self.screen, WHITE, (0,0,width*self.DIAMETER,height*self.DIAMETER), 0)

    def _drawCircle(self,position,colour):
        x,y = position
        pygame.gfxdraw.filled_circle(self.screen, x, y , self.RADIUS-2, colour )
        pygame.gfxdraw.aacircle(self.screen, x, y , self.RADIUS-2, colour )

    def _drawJoiningSquare(self):
        squares = self.board.joiningSquares()
        for square in squares:
            x,y = square.position
            pygame.draw.rect(self.screen, square.colour, (x*self.DIAMETER+2,y*self.DIAMETER+2,self.DIAMETER-3,self.DIAMETER-3), 0)
    
    def _displayScore(self,current):
        pygame.draw.rect(self.screen, GREY, (0,self.GAME_HEIGHT,self.SCREEN_WIDTH,self.SCOREBOARD_HEIGHT), 0)
        pygame.font.init()
        myfont = pygame.font.Font(basedir + os.sep + "Fonts/angrybirds-regular.ttf", 24)
        textsurface = myfont.render(' Score: %s Moves: %s Current move: %s Top Score: %s'%(self.board.score,self.board.nmoves,current,self.board.highScore), 1, BLACK,GREY).convert()
        self.screen.blit(textsurface,(1,self.GAME_HEIGHT+1))
        pygame.display.update()

    def display(self):
        self._drawSquare(self.board.width,self.board.height)
        for x in range(self.board.width):
            for y in range(self.board.height):
                if self.board.balls[x][y]:
                    self._drawCircle((self.RADIUS+x*self.DIAMETER,self.RADIUS+y*self.DIAMETER), self.board.balls[x][y].colour)
        self._drawJoiningSquare()
        self._displayScore(0)
        pygame.display.update()

    def _getPosition(self,radius):
        x1,y1 = pygame.mouse.get_pos()
        for x in range(self.board.width):
            for y in range(self.board.height):
                x2,y2 = self.RADIUS+x*self.DIAMETER,self.RADIUS+y*self.DIAMETER
                distance = math.hypot(x1 - x2, y1 - y2)
                if distance <= radius and self.board.balls[int((x2-self.RADIUS)/self.DIAMETER)][int((y2-self.RADIUS)/self.DIAMETER)]:
                    return int((x2-self.RADIUS)/self.DIAMETER),int((y2-self.RADIUS)/self.DIAMETER)
        return None
    
    def gameOverDisplay(self):
        self.GameOver = True
        
        pygame.font.init()
        myfont = pygame.font.Font(basedir + os.sep + "Fonts/angrybirds-regular.ttf", 72)
        textsurface = myfont.render('GAME OVER !!', 1, BLACK)
        text_rect = textsurface.get_rect(center=(self.SCREEN_WIDTH/2, (self.SCREEN_HEIGHT-48)/2))
        self.screen.blit(textsurface,text_rect)
        
        pygame.draw.rect(self.screen, GREY, (0,self.GAME_HEIGHT,self.SCREEN_WIDTH,self.SCOREBOARD_HEIGHT), 0)
        myfont = pygame.font.Font(basedir + os.sep + "Fonts/angrybirds-regular.ttf", 24)
        textsurface = myfont.render('Your Score: %s Top Score: %s '%(self.board.score,self.board.highScore), 1, BLACK,GREY).convert()
        self.screen.blit(textsurface,(1,515))
        pygame.display.update()

    def run(self):
        self.display()
        while True:
            position = self._getPosition(radius=self.RADIUS)
            if position and not self.GameOver:
                currentScore = self.board.getScore(position)
                self._displayScore(currentScore)
            
            for event in pygame.event.get():
                if event.type==pygame.MOUSEBUTTONDOWN:
                    position = self._getPosition(radius=self.RADIUS)
                    if position:
                        self.board.removeBalls(position)
                        self.display()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if self.board.isGameOver():
                self.gameOverDisplay()
 
if __name__ == "__main__":
    myGame = GameDisplay()
    myGame.run()

