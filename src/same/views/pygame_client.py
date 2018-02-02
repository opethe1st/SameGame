import math
import sys
import pygame
import pygame.locals
import pygame.gfxdraw

from same.data.constants import Colour
from same.views.gui_client import GuiClient
from same.views.events import BallClickedEvent, GameQuit  # pylint: disable=W0611



class PyGameClient(GuiClient):

    def __init__(self, size, num_columns, num_rows, board_position, score_board_height, colours):
        pygame.init()  # pylint: disable=all
        pygame.display.set_caption('Same!')
        self.score_board_height = score_board_height
        self.board_dimensions = (size*num_columns, size*num_rows + score_board_height)
        self.screen = pygame.display.set_mode(self.board_dimensions)
        self.size = size
        self.colours = colours
        self.num_columns = num_columns
        self.num_rows = num_rows


    def draw_board(self, balls, boxes):
        pygame.draw.rect(self.screen, Colour.WHITE, (0, 0, self.num_columns * self.size, self.num_rows * self.size), 0)
        for j, row in enumerate(balls):
            for i, ball in enumerate(row):
                if ball:
                    self.draw_circle(position=(i, j), colour=self.colours[ball.colour])
        # draw the boxes
        for j , row in enumerate(boxes):
            for i, box in enumerate(row):
                if box:
                    pygame.draw.rect(self.screen, self.colours[box.colour], (self.size//2*i+2, self.size//2*j+2, self.size-3, self.size-3), 0)
        pygame.display.update()

    def draw_circle(self, position, colour):
        x, y = position
        x, y = x + 0.5, y + 0.5
        pygame.gfxdraw.filled_circle(self.screen, int(x * self.size), int(y * self.size), self.size//2 - 2, colour)
        pygame.gfxdraw.aacircle(self.screen, int(x * self.size), int(y * self.size), self.size//2 - 2, colour)


    def draw_score_board(self, score, highest_score, current_move_score):
        pygame.draw.rect(self.screen, Colour.GREY, (0, self.board_dimensions[1]-self.score_board_height, self.board_dimensions[0], self.score_board_height), 0)
        pygame.font.init()
        myfont = pygame.font.Font("/Users/ope/Documents/code/Projects/SameGame/static/Fonts/angrybirds-regular.ttf", 22)
        text = ' Score: {score} Moves: {moves} Current move: {current_move} Top Score: {top_score}'.format(score=score, moves=0, current_move=current_move_score, top_score=highest_score)
        textsurface = myfont.render(text, 1, Colour.BLACK, Colour.GREY).convert()
        self.screen.blit(textsurface, (1, self.board_dimensions[1]-self.score_board_height + 1))
        pygame.display.update()

    def game_over(self):
        # TODO[ope]: add Game Over text to the screen.
        pass

    def end_game(self):
        pygame.quit()
        sys.exit(0)

    def get_clicked_ball(self):
        x1, y1 = pygame.mouse.get_pos()
        for x in range(self.num_columns):
            for y in range(self.num_rows):
                x2, y2 = (x + 0.5) * self.size, (y + 0.5) * self.size
                distance = math.hypot(x1 - x2, y1 - y2)
                if distance <= self.size//2:
                    return x, y
        return None

    def get_current_ball(self):
        x1, y1 = pygame.mouse.get_pos()
        for x in range(self.num_columns):
            for y in range(self.num_rows):
                x2, y2 = (x + 0.5) * self.size, (y + 0.5) * self.size
                distance = math.hypot(x1 - x2, y1 - y2)
                if distance <= self.size//2:
                    return x, y
        return None

    def get_events(self):
        events = []
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                events.append(GameQuit())
            if event.type == pygame.locals.MOUSEBUTTONDOWN:
                events.append(BallClickedEvent(position=self.get_clicked_ball()))
        return events
