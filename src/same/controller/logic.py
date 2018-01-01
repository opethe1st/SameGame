import random
from typing import List


class Ball:

    def __init__(self, colour):
        self.colour = colour

    def __eq__(self, other):
        return self.colour == other.colour if type(self) == type(other) else False  # pylint: disable=C0123

    def __repr__(self):
        return 'Ball(colour={colour})'.format(colour=self.colour)


class Box:

    def __init__(self, colour):
        self.colour = colour

    def __eq__(self, other) -> bool:
        return self.colour == other.colour if type(self) == type(other) else False  # pylint: disable=C0123

    def __repr__(self):
        return 'Box(colour={colour})'.format(colour=self.colour)

#  augment later to talk to the database
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

    def __init__(self, width, height, colours, scorer):
        self.width = width
        self.height = height
        self.colours = colours
        self.balls = None
        self.scorer = scorer

    def start_game(self):
        self.balls = self.generate_random_balls()

    def generate_random_balls(self):
        balls = []
        for _ in range(self.height):
            row_of_balls = []
            for __ in range(self.width):
                random_colour = random.choice(self.colours)
                row_of_balls.append(Ball(colour=random_colour))
            balls.append(row_of_balls)
        return balls

    def generate_boxes(self):
        row_edges = 2 * self.height - 1
        col_edges = 2 * self.width - 1
        boxes = [[None for col in range(col_edges)] for row in range(row_edges)]
        for row in range(row_edges):
            for col in range(col_edges):
                colour = self.balls[row//2][col//2].colour
                if col%2 == 1 and row%2 == 0 and self.balls[row//2][col//2] == self.balls[row//2][col//2+1]:
                    boxes[row][col] = Box(colour=colour)
                if col%2 == 0 and row%2 == 1 and self.balls[row//2][col//2] == self.balls[row//2+1][col//2]:
                    boxes[row][col] = Box(colour=colour)
        return boxes

    def is_game_over(self):
        "Returns True if the Game is over and False otherwise"
        for x_pos in range(self.width):
            for y_pos in range(self.height):
                if len(self.adjacent((x_pos, y_pos))) > 1:
                    return False
        return True

    def make_move(self, position: tuple):
        self.mark_balls_to_remove(position=position)
        csr_balls = self.make_balls_fall()
        csr_balls = self.remove_empty_rows(csr_balls=csr_balls)
        self.convert_cols_to_rows(csr_balls=csr_balls)

    def mark_balls_to_remove(self, position: tuple):
        positions_of_balls_to_remove = self.adjacent(position)
        for pos in positions_of_balls_to_remove:
            x_pos, y_pos = pos
            self.balls[x_pos][y_pos] = None

    def adjacent(self, position: tuple) -> List[tuple]:
        "returns the list of positions with balls of the same colour adjacent to the ball at position"
        x_pos, y_pos = position
        colour = self.balls[x_pos][y_pos].colour
        adjacent_balls = set([(x_pos, y_pos)])
        stack = [(x_pos, y_pos)]
        visited = set([x_pos, y_pos])
        while stack:
            x_pos, y_pos = stack.pop()
            for i in [max(0, x_pos-1), min(self.height-1, x_pos+1)]: # there is an error here, right? 0 might not be adjacent
                for j in [max(0, y_pos-1), min(self.width-1, y_pos+1)]:
                    if self.balls[i][j] is not None and self.balls[i][j].colour == colour and (i, j) not in visited:
                        adjacent_balls.add((i, j))
                        stack.append((i, j))
                    visited.add((i, j))
        return adjacent_balls

    def convert_rows_to_columns(self):
        columns_to_rows = [[None for i in range(self.height)] for j in  range(self.width)]
        for i in range(self.height):
            for j in range(self.width):
                columns_to_rows[j][i] = self.balls[(-i-1)%self.height][j]
        return columns_to_rows

    def make_balls_fall(self):
        columns_to_rows = self.convert_rows_to_columns()
        for i, _ in enumerate(columns_to_rows):
            columns_to_rows[i] = list(filter(lambda x: x is not None, columns_to_rows[i]))  # remove the Nones
            number_of_empty_positions = self.width-len(columns_to_rows[i])
            columns_to_rows[i] += [None] * number_of_empty_positions  # pad with Nones
        return columns_to_rows

    def remove_empty_rows(self, csr_balls):
        columns_list = []
        for i, _ in enumerate(csr_balls):
            if any(csr_balls[i]):
                columns_list.append(i)
        for i, column in enumerate(columns_list):
            csr_balls[i] = csr_balls[column]
        for i in range(len(columns_list), len(csr_balls)):
            csr_balls[i] = [None]*self.height
        return csr_balls

    def convert_cols_to_rows(self, csr_balls):
        for i in range(self.height):
            for j in range(self.width):
                self.balls[i][j] = csr_balls[j][(-i-1)%self.height]
