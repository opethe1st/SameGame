import random
import os
import sys
from typing import List
from same.data.constants import ColourScheme

# These are the settings for pyinstaller
# we are running in a bundle if sys.frozen else normal python
basedir = sys._MEIPASS if getattr(sys, 'frozen', False) else '.'


class Ball:
    def __init__(self, colour: str):
        self.colour = colour

    def __eq__(self, other):
        return self.colour == other.colour if type(self) == type(other) else False

    def __repr__(self):
        return 'Ball(colour={colour})'.format(colour=self.colour)


class Box:
    def __init__(self, colour: str):
        self.colour = colour

    def __eq__(self, other) -> bool:
        return self.colour == other.colour if type(self) == type(other) else False

    def __repr__(self):
        return 'Box(colour={colour})'.format(colour=self.colour)


class Scorer:

    def __init__(self):
        self.score = 0

    @property
    def score(self):
        return self.score

    @score.setter
    def set_score(self, new_score):
        self.score = new_score

    @property
    def high_score(self):
        return 0

    @high_score.setter
    def update_high_score(self, new_high_score):
        self.score = new_high_score


class Board:
    def __init__(self, WIDTH, HEIGHT, COLOURS, scorer):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.COLOURS = COLOURS
        self.balls = None
        self.scorer = scorer

    def start_game(self):
        self.balls = self._generate_random_arrangement_of_balls()

    def _generate_random_arrangement_of_balls(self):
        balls = []
        for row in range(self.HEIGHT):
            row_of_balls = []
            for col in range(self.WIDTH):
                random_colour = random.choice(self.COLOURS)
                row_of_balls.append(Ball(colour=random_colour))
            balls.append(row_of_balls)
        return balls

    def generate_boxes(self):
        row_edges = 2 * self.HEIGHT - 1
        col_edges = 2 * self.WIDTH - 1
        boxes = [[None for col in range(col_edges)] for row in range(row_edges)]
        for row in range(row_edges):
            for col in range(col_edges):
                colour = self.balls[row//2][col//2].colour
                if col%2==1 and row%2==0 and self.balls[row//2][col//2] == self.balls[row//2][col//2+1]:
                    boxes[row][col] = Box(colour=colour)
                if col%2==0 and row%2==1 and self.balls[row//2][col//2] == self.balls[row//2+1][col//2]:
                    boxes[row][col] = Box(colour=colour)
        return boxes

    def is_game_over(self):
        "Returns True if the Game is over and False otherwise"
        for x in range(self.width):
            for y in range(self.height):
                if len(self._adjacent((x, y))) > 0:
                    return False
        return True

    def make_move(self, position: tuple):
        self.mark_balls_to_remove(position=position)
        csr_balls = self.make_balls_fall()
        csr_balls = self.remove_empty_rows_between_columns(csr_balls=csr_balls)
        self.convert_cols_to_rows(csr_balls=csr_balls)

    def mark_balls_to_remove(self, position: tuple):
        positions_of_balls_to_remove = self._adjacent(position)
        for position in positions_of_balls_to_remove:
            x, y = position
            self.balls[x][y] = None

    def _adjacent(self, position: tuple) -> List[tuple]:
        "returns the list of positions with balls of the same colour adjacent to the ball at position"
        x, y = position
        colour = self.balls[x][y].colour
        adjacent_balls = set([(x,y)])
        stack = [(x,y)]
        visited = set([x,y])
        while stack:
            x, y = stack.pop()
            for i in [max(0, x-1), min(self.HEIGHT-1, x+1)]: # there is an error here, right? 0 might not be adjacent
                for j in [max(0, y-1), min(self.WIDTH-1, y+1)]:
                    if self.balls[i][j] is not None and self.balls[i][j].colour == colour and (i,j) not in visited:
                        adjacent_balls.add((i, j))
                        stack.append((i, j))
                    visited.add((i, j))
        return adjacent_balls

    def convert_rows_to_columns(self):
        columns_to_rows = [[None for i in range(self.HEIGHT)] for j in  range(self.WIDTH)]
        for i in range(self.HEIGHT):
            for j in range(self.WIDTH):
                columns_to_rows[j][i] = self.balls[(-i-1)%self.HEIGHT][j]
        return columns_to_rows

    def make_balls_fall(self):
        columns_to_rows = self.convert_rows_to_columns()
        for i in range(len(columns_to_rows)):
            columns_to_rows[i] = list(filter(lambda x: x is not None, columns_to_rows[i]))  # remove the Nones
            number_of_empty_positions = self.WIDTH-len(columns_to_rows[i])
            columns_to_rows[i] += [None] * number_of_empty_positions  # pad with Nones
        return columns_to_rows

    def remove_empty_rows_between_columns(self, csr_balls):
        columnsList = []
        for i in range(len(csr_balls)):
            if any(csr_balls[i]):
                columnsList.append(i)
        for i, column in enumerate(columnsList):
            csr_balls[i] = csr_balls[column]
        number_of_empty_cols = self.WIDTH - len(columnsList)
        for i in range(len(columnsList), len(csr_balls)):
            csr_balls[i] = [None]*self.HEIGHT
        return csr_balls

    def convert_cols_to_rows(self, csr_balls):
        for i in range(self.HEIGHT):
            for j in range(self.WIDTH):
                self.balls[i][j] = csr_balls[j][(-i-1)%self.HEIGHT]
