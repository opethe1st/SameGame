import random
from typing import List

from same.controller.ball import Ball
from same.controller.box import Box


class Board:

    def __init__(self, num_columns, num_rows, num_colours, scorer):
        self.num_columns = num_columns
        self.num_rows = num_rows
        self.colours = [i for i in range(num_colours)]
        self.balls = self.generate_random_balls()
        self.scorer = scorer

    def get_balls(self) -> List[List[Ball]]:
        return self.balls

    def generate_random_balls(self) -> List[List[Ball]]:
        balls = []
        for _ in range(self.num_rows):
            row_of_balls = []
            for __ in range(self.num_columns):
                random_colour = random.choice(self.colours)
                row_of_balls.append(Ball(colour=random_colour))
            balls.append(row_of_balls)
        return balls

    def get_boxes(self):
        return self.generate_boxes()

    def generate_boxes(self) -> List[List[Ball]]:
        row_edges = 2 * self.num_rows - 1
        col_edges = 2 * self.num_columns - 1
        boxes = [[None for col in range(col_edges)] for row in range(row_edges)]
        for row in range(row_edges):
            for col in range(col_edges):
                if self.balls[row//2][col//2]:
                    colour = self.balls[row//2][col//2].colour
                    if col%2 == 1 and row%2 == 0 and self.balls[row//2][col//2] == self.balls[row//2][col//2+1]:
                        boxes[row][col] = Box(colour=colour)
                    if col%2 == 0 and row%2 == 1 and self.balls[row//2][col//2] == self.balls[row//2+1][col//2]:
                        boxes[row][col] = Box(colour=colour)
        return boxes

    def is_game_over(self):
        "Returns True if the Game is over and False otherwise"
        for x_pos in range(self.num_columns):
            for y_pos in range(self.num_rows):
                if len(self.adjacent((x_pos, y_pos))) > 1:
                    return False
        return True

    def make_move(self, position: tuple):
        self.mark_balls_to_remove(position=position)
        print(self.balls)
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
        if position is None:
            return []
        x_pos, y_pos = position
        colour = self.balls[x_pos][y_pos].colour
        adjacent_balls = set([(x_pos, y_pos)])
        stack = [(x_pos, y_pos)]
        visited = set([x_pos, y_pos])
        while stack:
            x_pos, y_pos = stack.pop()
            for i in [max(0, x_pos-1), min(self.num_rows-1, x_pos+1)]: # there is an error here, right? 0 might not be adjacent
                for j in [max(0, y_pos-1), min(self.num_columns-1, y_pos+1)]:
                    if self.balls[i][j] is not None and self.balls[i][j].colour == colour and (i, j) not in visited:
                        adjacent_balls.add((i, j))
                        stack.append((i, j))
                    visited.add((i, j))
        return adjacent_balls

    def convert_rows_to_columns(self) -> List[List[Ball]]:
        columns_to_rows = [[None for i in range(self.num_rows)] for j in  range(self.num_columns)]
        for i in range(self.num_rows):
            for j in range(self.num_columns):
                columns_to_rows[j][i] = self.balls[(-i-1)%self.num_rows][j]
        return columns_to_rows

    def make_balls_fall(self) -> List[List[Ball]]:
        columns_to_rows = self.convert_rows_to_columns()
        for i, _ in enumerate(columns_to_rows):
            columns_to_rows[i] = list(filter(lambda x: x is not None, columns_to_rows[i]))  # remove the Nones
            number_of_empty_positions = self.num_rows-len(columns_to_rows[i])
            columns_to_rows[i] += [None] * number_of_empty_positions  # pad with Nones
        return columns_to_rows

    def remove_empty_rows(self, csr_balls: List[List[Ball]]) -> List[List[Ball]]:
        columns_list = []
        for i, _ in enumerate(csr_balls):
            if any(csr_balls[i]):
                columns_list.append(i)
        for i, column in enumerate(columns_list):
            csr_balls[i] = csr_balls[column]
        for i in range(len(columns_list), len(csr_balls)):
            csr_balls[i] = [None]*self.num_rows
        return csr_balls

    def convert_cols_to_rows(self, csr_balls: List[List[Ball]]):
        for i in range(self.num_rows):
            for j in range(self.num_columns):
                self.balls[i][j] = csr_balls[j][(-i-1)%self.num_rows]

    def get_score(self, position):
        return self.scorer.get_score(balls=self.adjacent(position=position))

    def get_current_score(self):
        return self.scorer.get_current_score()

    def set_current_score(self):
        return self.scorer.set_current_score()

    def get_high_score(self):
        return self.scorer.get_high_score()

    def set_high_score(self):
        return self.set_high_score()
