#! python2
import sys
import math
import os

from logic import Board
import pygame
import pygame.gfxdraw
from constants import ColourScheme, Colour

# These are the settings for pyinstaller
if getattr(sys, 'frozen', False):
    # we are running in a bundle
    basedir = sys._MEIPASS
else:
    # we are running in a normal Python environment
    basedir = '.'


class GameDisplay:
    def __init__(self, BallColours=ColourScheme.MONFAVORITE, boardColour=Colour.WHITE):
        self.DIAMETER = 32  # size of the balls
        self.RADIUS = self.DIAMETER / 2
        self.GameOver = False
        self.WIDTH = 20
        self.HEIGHT = 16
        self.SCOREBOARD_HEIGHT = 48
        self.GAME_HEIGHT = self.DIAMETER * self.HEIGHT
        self.SCREEN_WIDTH = self.DIAMETER * self.WIDTH
        self.SCREEN_HEIGHT = self.GAME_HEIGHT + self.SCOREBOARD_HEIGHT
        self.boardColour = boardColour

        pygame.init()
        self.screen = pygame.display.set_mode(
            (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption('Same!')
        self.board = Board(
            width=self.WIDTH, height=self.HEIGHT, BallColours=BallColours)

    def _drawSquare(self, width, height):
        pygame.draw.rect(self.screen, self.boardColour, (0, 0,
                                                         width * self.DIAMETER, height * self.DIAMETER), 0)

    def _drawCircle(self, position, colour):
        x, y = position
        pygame.gfxdraw.filled_circle(self.screen, int(x), int(y),
                                     int(self.RADIUS - 2), colour)
        pygame.gfxdraw.aacircle(self.screen, int(
            x), int(y), int(self.RADIUS - 2), colour)

    def _drawJoiningSquares(self):
        squares = self.board.joiningSquares()
        for square in squares:
            x, y = square.position
            pygame.draw.rect(self.screen, square.colour, (x * self.DIAMETER + 2,
                                                          y * self.DIAMETER + 2, self.DIAMETER - 3, self.DIAMETER - 3), 0)

    def _displayScore(self, current):
        pygame.draw.rect(self.screen, Colour.GREY, (0, self.GAME_HEIGHT,
                                             self.SCREEN_WIDTH, self.SCOREBOARD_HEIGHT), 0)
        pygame.font.init()
        myfont = pygame.font.Font(
            basedir + os.sep + "../resources/Fonts/angrybirds-regular.ttf", 22)
        textsurface = myfont.render(' Score: %s Moves: %s Current move: %s Top Score: %s' % (
            self.board.score, self.board.nmoves, current, self.board.highScore), 1, Colour.BLACK, Colour.GREY).convert()
        self.screen.blit(textsurface, (1, self.GAME_HEIGHT + 1))
        self._newGame()
        # pygame.display.update()

    def _display(self):
        self._drawSquare(self.board.width, self.board.height)
        for x in range(self.board.width):
            for y in range(self.board.height):
                if self.board.balls[x][y]:
                    self._drawCircle((self.RADIUS + x * self.DIAMETER, self.RADIUS +
                                      y * self.DIAMETER), self.board.balls[x][y].colour)
        self._drawJoiningSquares()
        self._displayScore(0)
        # pygame.display.update()

    def _getPosition(self, radius):
        x1, y1 = pygame.mouse.get_pos()
        for x in range(self.board.width):
            for y in range(self.board.height):
                x2, y2 = self.RADIUS + x * self.DIAMETER, self.RADIUS + y * self.DIAMETER
                distance = math.hypot(x1 - x2, y1 - y2)
                if distance <= self.RADIUS and self.board.balls[int((x2 - self.RADIUS) / self.DIAMETER)][int((y2 - self.RADIUS) / self.DIAMETER)]:
                    return int((x2 - self.RADIUS) / self.DIAMETER), int((y2 - self.RADIUS) / self.DIAMETER)
        return None

    def _gameOverDisplay(self):
        self.GameOver = True

        pygame.font.init()
        myfont = pygame.font.Font(
            basedir + os.sep + "../resources/Fonts/angrybirds-regular.ttf", 72)
        textsurface = myfont.render('GAME OVER !!', 1, BLACK)
        text_rect = textsurface.get_rect(
            center=(self.SCREEN_WIDTH / 2, (self.SCREEN_HEIGHT - 48) / 2))
        self.screen.blit(textsurface, text_rect)

        pygame.draw.rect(self.screen, Colour.GREY, (0, self.GAME_HEIGHT,
                                             self.SCREEN_WIDTH, self.SCOREBOARD_HEIGHT), 0)
        myfont = pygame.font.Font(
            basedir + os.sep + "../resources/Fonts/angrybirds-regular.ttf", 22)
        textsurface = myfont.render('Your Score: %s Top Score: %s ' % (
            self.board.score, self.board.highScore), 1, Colour.BLACK, Colour.GREY).convert()
        self.screen.blit(textsurface, (1, 515))
        self._newGame()
        # pygame.display.update()

    def _newGame(self):
        # NewGame button in the scoreboard
        DARKGREY = (100, 100, 100)
        LIGHTGREY = (230, 230, 230)
        x1, y1 = pygame.mouse.get_pos()
        if self.SCREEN_WIDTH * 0.8 < x1 < self.SCREEN_WIDTH * 0.8 + self.SCREEN_WIDTH * 0.15 and self.GAME_HEIGHT + 7 < y1 < self.GAME_HEIGHT + 7 + self.SCOREBOARD_HEIGHT * 0.70:
            colour = LIGHTGREY
        else:
            colour = DARKGREY
        pygame.draw.rect(self.screen, Colour.BLACK, (self.SCREEN_WIDTH * 0.8, self.GAME_HEIGHT +
                                              7, self.SCREEN_WIDTH * 0.15, self.SCOREBOARD_HEIGHT * 0.70), 1)
        pygame.draw.rect(self.screen, colour, (self.SCREEN_WIDTH * 0.8, self.GAME_HEIGHT +
                                               7, self.SCREEN_WIDTH * 0.15, self.SCOREBOARD_HEIGHT * 0.70), 0)
        pygame.font.init()
        myfont = pygame.font.Font(
            basedir + os.sep + "../resources/Fonts/angrybirds-regular.ttf", 22)
        textsurface = myfont.render(' New Game', 1, Colour.BLACK, colour).convert()
        self.screen.blit(textsurface, (self.SCREEN_WIDTH *
                                       0.8 + 3, self.GAME_HEIGHT + 7))
        pygame.display.update()

    def _buttonClicked(self):
        # returns true if the button click was on the board area and not the
        # scoreboard area
        x1, y1 = pygame.mouse.get_pos()
        if self.SCREEN_WIDTH * 0.8 < x1 < self.SCREEN_WIDTH * 0.8 + self.SCREEN_WIDTH * 0.15 and self.GAME_HEIGHT + 7 < y1 < self.GAME_HEIGHT + 7 + self.SCOREBOARD_HEIGHT * 0.70:
            return True
        else:
            return False

    def run(self):
        self._display()
        breakLoop = False
        while True:
            self._newGame()
            # displays with the possible score if you click on this ball
            position = self._getPosition(radius=self.RADIUS)
            if position and not self.GameOver:
                currentScore = self.board.getScore(position)
                self._displayScore(currentScore)
            # handles all the events, button clicks etc
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
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
