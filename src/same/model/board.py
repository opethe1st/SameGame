import random
from typing import List

from same.model.ball import Ball
from same.model.box import Box


class SameBoard:

    def __init__(self, num_columns: int, num_rows: int, num_colours: int, scorer: 'Scorer'):
        self.num_columns = num_columns
        self.num_rows = num_rows
        self.colours = [i for i in range(num_colours)]
        self.balls = self.generate_random_balls()
        self.scorer = scorer
        self.num_moves = 0

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
                if self.balls[row // 2][col // 2]:
                    colour = self.balls[row // 2][col // 2].colour
                    if col % 2 == 1 and row % 2 == 0 and self.balls[row // 2][col // 2] == self.balls[row // 2][col // 2 + 1]:
                        boxes[row][col] = Box(colour=colour)
                    if col % 2 == 0 and row % 2 == 1 and self.balls[row // 2][col // 2] == self.balls[row // 2 + 1][col // 2]:
                        boxes[row][col] = Box(colour=colour)
        return boxes

    def is_game_over(self):
        "Returns True if the Game is over and False otherwise"
        for x_pos in range(self.num_columns):
            for y_pos in range(self.num_rows):
                if len(self.adjacent(balls=self.balls, position=(x_pos, y_pos))) > 1:
                    return False
        return True

    def make_move(self, position: tuple):
        positions_of_balls_to_remove = self.adjacent(balls=self.balls, position=position)
        modified_balls = self.mark_balls_to_remove(balls=self.balls, positions_of_balls_to_remove=positions_of_balls_to_remove)
        csr_balls = self.make_balls_fall(balls=modified_balls)
        csr_balls = self.remove_empty_rows(csr_balls=csr_balls)
        self.update_current_score(current_move_score=self.calculate_score(ball_position=position))
        if len(positions_of_balls_to_remove) > 1:
            self.num_moves += 1
        self.balls = self.transpose(balls=csr_balls)

    @staticmethod
    def mark_balls_to_remove(balls: List[List[Ball]], positions_of_balls_to_remove: List[tuple]):
        balls = [[ball for ball in ball_row] for ball_row in balls]
        for pos in positions_of_balls_to_remove:
            x_pos, y_pos = pos
            balls[x_pos][y_pos] = None
        return balls

    @staticmethod
    def adjacent(balls: List[List[Ball]], position: tuple) -> List[tuple]:
        "returns the list of positions with balls of the same colour adjacent to the ball at position"
        if position is None or balls[position[1]][position[0]] is None:
            return []
        num_rows = len(balls)
        num_columns = len(balls[0])
        y_pos, x_pos = position
        colour = balls[x_pos][y_pos].colour
        adjacent_balls = set()
        stack = [(x_pos, y_pos)]
        visited = set([x_pos, y_pos])
        while stack:
            x_pos, y_pos = stack.pop()
            for (i, j) in [(max(0, x_pos - 1), y_pos), (min(num_rows - 1, x_pos + 1), y_pos), (x_pos, max(0, y_pos - 1)), (x_pos, min(num_columns - 1, y_pos + 1))]:
                if balls[i][j] is not None and balls[i][j].colour == colour and (i, j) not in visited:
                    adjacent_balls.add((i, j))
                    stack.append((i, j))
                visited.add((i, j))
        return adjacent_balls

    @staticmethod
    def transpose(balls: List[List[Ball]]) -> List[List[Ball]]:
        num_rows = len(balls)
        num_columns = len(balls[0])
        columns_to_rows = [[None for j in range(num_rows)] for i in range(num_columns)]
        for j in range(num_rows):
            for i in range(num_columns):
                columns_to_rows[i][j] = balls[j][i]
        return columns_to_rows

    def make_balls_fall(self, balls: List[List[Ball]]) -> List[List[Ball]]:
        columns_to_rows = self.transpose(balls=balls)
        csr_num_columns = len(columns_to_rows[0])
        for i, _ in enumerate(columns_to_rows):
            non_empty_columns = list(filter(lambda x: x is not None, columns_to_rows[i]))  # remove the Nones
            empty_cols = [None for i in range(csr_num_columns - len(non_empty_columns))]
            columns_to_rows[i] = empty_cols + non_empty_columns  # pad with Nones
        return columns_to_rows

    @staticmethod
    def remove_empty_rows(csr_balls: List[List[Ball]]) -> List[List[Ball]]:
        num_columns = len(csr_balls[0])
        columns_list = []
        for i, _ in enumerate(csr_balls):
            if any(csr_balls[i]):
                columns_list.append(i)
        for i, column in enumerate(columns_list):
            csr_balls[i] = csr_balls[column]
        for i in range(len(columns_list), len(csr_balls)):
            csr_balls[i] = [None] * num_columns
        return csr_balls

    def calculate_score(self, ball_position: tuple):
        ball_positions = self.adjacent(balls=self.get_balls(), position=ball_position)
        return self.scorer.calculate_score(ball_positions=ball_positions)

    def get_current_score(self):
        return self.scorer.get_current_score()

    def update_current_score(self, current_move_score: int):
        return self.scorer.update_current_score(score=current_move_score)

    def get_high_score(self) -> int:
        return self.scorer.get_high_score()

    def update_high_score(self, new_high_score: int) -> int:
        return self.scorer.update_high_score(new_high_score=new_high_score)
