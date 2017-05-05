from Logic import Board
import pygame
import pygame.gfxdraw
import sys
import math
import os

#COLOURS
GREY = (150,150,150)
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)

#COLOUR SCHEMES
MONFAVORITE =[(247, 193, 187),(136, 90, 90),(220, 19, 108),(53, 58, 71), (132, 176, 130)]

SOMBRE = [(35, 0, 7),(215, 207, 7),(217, 131, 36),(164, 6, 6), (90, 0, 2)]

COOL = [(237, 37, 78), (249, 220, 92), (244, 255, 253),(1, 25, 54),(70, 83, 98)]

COOL2 = [(73, 88, 103), (87, 115, 153),(189, 213, 234), (247, 247, 255), (254, 95, 85) ]

COLD = [(25, 83, 95), (11, 122, 117), (215, 201, 170), (123, 45, 38), (240, 243, 245)]

ICY = [(216, 219, 226), (169, 188, 208), (88, 164, 176),(55, 63, 81), (218, 164, 154)]

SAVANNAH = [(91, 192, 235), (253, 231, 76), (155, 197, 61),(229, 89, 52),(250, 121, 33) ]
#These are the settings for pyinstaller
if getattr(sys, 'frozen', False):
    # we are running in a bundle
    basedir = sys._MEIPASS
else:
    # we are running in a normal Python environment
    basedir = '.'



class GameDisplay:
    def __init__(self,BallColours = MONFAVORITE,boardColour = WHITE):
        self.DIAMETER = 32 #size of the balls
        self.RADIUS = self.DIAMETER/2
        self.GameOver = False
        self.WIDTH = 20
        self.HEIGHT =16
        self.SCOREBOARD_HEIGHT = 48
        self.GAME_HEIGHT = self.DIAMETER*self.HEIGHT
        self.SCREEN_WIDTH = self.DIAMETER*self.WIDTH
        self.SCREEN_HEIGHT = self.GAME_HEIGHT + self.SCOREBOARD_HEIGHT
        self.boardColour = boardColour
        
        pygame.init()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH,self.SCREEN_HEIGHT))
        pygame.display.set_caption('Same!')
        self.board = Board(width=self.WIDTH,height=self.HEIGHT,BallColours=BallColours)

    def _drawSquare(self,width,height):
        pygame.draw.rect(self.screen, self.boardColour, (0,0,width*self.DIAMETER,height*self.DIAMETER), 0)

    def _drawCircle(self,position,colour):
        x,y = position
        pygame.gfxdraw.filled_circle(self.screen, x, y , self.RADIUS-2, colour )
        pygame.gfxdraw.aacircle(self.screen, x, y , self.RADIUS-2, colour )

    def _drawJoiningSquares(self):
        squares = self.board.joiningSquares()
        for square in squares:
            x,y = square.position
            pygame.draw.rect(self.screen, square.colour, (x*self.DIAMETER+2,y*self.DIAMETER+2,self.DIAMETER-3,self.DIAMETER-3), 0)
    
    def _displayScore(self,current):
        pygame.draw.rect(self.screen, GREY, (0,self.GAME_HEIGHT,self.SCREEN_WIDTH,self.SCOREBOARD_HEIGHT), 0)
        pygame.font.init()
        myfont = pygame.font.Font(basedir + os.sep + "Fonts/angrybirds-regular.ttf", 22)
        textsurface = myfont.render(' Score: %s Moves: %s Current move: %s Top Score: %s'%(self.board.score,self.board.nmoves,current,self.board.highScore), 1, BLACK,GREY).convert()
        self.screen.blit(textsurface,(1,self.GAME_HEIGHT+1))
        self._newGame()
        #pygame.display.update()
    def _display(self):
        self._drawSquare(self.board.width,self.board.height)
        for x in range(self.board.width):
            for y in range(self.board.height):
                if self.board.balls[x][y]:
                    self._drawCircle((self.RADIUS+x*self.DIAMETER,self.RADIUS+y*self.DIAMETER), self.board.balls[x][y].colour)
        self._drawJoiningSquares()
        self._displayScore(0)
        #pygame.display.update()

    def _getPosition(self,radius):
        x1,y1 = pygame.mouse.get_pos()
        for x in range(self.board.width):
            for y in range(self.board.height):
                x2,y2 = self.RADIUS+x*self.DIAMETER,self.RADIUS+y*self.DIAMETER
                distance = math.hypot(x1 - x2, y1 - y2)
                if distance <= self.RADIUS and self.board.balls[int((x2-self.RADIUS)/self.DIAMETER)][int((y2-self.RADIUS)/self.DIAMETER)]:
                    return int((x2-self.RADIUS)/self.DIAMETER),int((y2-self.RADIUS)/self.DIAMETER)
        return None
    
    def _gameOverDisplay(self):
        self.GameOver = True
        
        pygame.font.init()
        myfont = pygame.font.Font(basedir + os.sep + "Fonts/angrybirds-regular.ttf", 72)
        textsurface = myfont.render('GAME OVER !!', 1,BLACK)
        text_rect = textsurface.get_rect(center=(self.SCREEN_WIDTH/2, (self.SCREEN_HEIGHT-48)/2))
        self.screen.blit(textsurface,text_rect)
        
        pygame.draw.rect(self.screen, GREY, (0,self.GAME_HEIGHT,self.SCREEN_WIDTH,self.SCOREBOARD_HEIGHT), 0)
        myfont = pygame.font.Font(basedir + os.sep + "Fonts/angrybirds-regular.ttf", 22)
        textsurface = myfont.render('Your Score: %s Top Score: %s '%(self.board.score,self.board.highScore), 1, BLACK,GREY).convert()
        self.screen.blit(textsurface,(1,515))
        self._newGame()
        #pygame.display.update()
    
    def _newGame(self):
        #NewGame button in the scoreboard
        DARKGREY = (100,100,100)
        LIGHTGREY = (230,230,230)
        x1,y1 = pygame.mouse.get_pos()
        if self.SCREEN_WIDTH*0.8<x1<self.SCREEN_WIDTH*0.8+self.SCREEN_WIDTH*0.15 and self.GAME_HEIGHT+7<y1<self.GAME_HEIGHT+7+self.SCOREBOARD_HEIGHT*0.70:
            colour = LIGHTGREY
        else:
            colour = DARKGREY
        pygame.draw.rect(self.screen, BLACK, (self.SCREEN_WIDTH*0.8,self.GAME_HEIGHT+7,self.SCREEN_WIDTH*0.15,self.SCOREBOARD_HEIGHT*0.70), 1)
        pygame.draw.rect(self.screen, colour, (self.SCREEN_WIDTH*0.8,self.GAME_HEIGHT+7,self.SCREEN_WIDTH*0.15,self.SCOREBOARD_HEIGHT*0.70), 0)
        pygame.font.init()
        myfont = pygame.font.Font(basedir + os.sep + "Fonts/angrybirds-regular.ttf", 22)
        textsurface = myfont.render(' New Game', 1, BLACK,colour).convert()
        self.screen.blit(textsurface,(self.SCREEN_WIDTH*0.8+3,self.GAME_HEIGHT+7))
        pygame.display.update()
    
    def _buttonClicked(self):
        #returns true if the button click was on the board area and not the scoreboard area
        x1,y1 = pygame.mouse.get_pos()
        if self.SCREEN_WIDTH*0.8<x1<self.SCREEN_WIDTH*0.8+self.SCREEN_WIDTH*0.15 and self.GAME_HEIGHT+7<y1<self.GAME_HEIGHT+7+self.SCOREBOARD_HEIGHT*0.70:
            return True
        else:
            return False


    def run(self):
        self._display()
        breakLoop = False
        while True:
            self._newGame()
            #displays with the possible score if you click on this ball
            position = self._getPosition(radius=self.RADIUS)
            if position and not self.GameOver:
                currentScore = self.board.getScore(position)
                self._displayScore(currentScore)
            #handles all the events, button clicks etc
            for event in pygame.event.get():
                if event.type==pygame.MOUSEBUTTONDOWN:
                    position = self._getPosition(radius=self.RADIUS)
                    if position:
                        self.board.removeBalls(position)
                        self._display()
                    elif self._buttonClicked():
                        breakLoop = True
                        break
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if self.board.isGameOver():
                self._gameOverDisplay()
            if breakLoop:
                break
 
if __name__ == "__main__":
    while True:
        myGame = GameDisplay()
        myGame.run()

