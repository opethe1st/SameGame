import random
import os
import sys

from same.data.constants import ColourScheme

# These are the settings for pyinstaller
 # we are running in a bundle if sys.frozen else normal python
basedir = sys._MEIPASS if getattr(sys, 'frozen', False) else '.'


class Ball:
    def __init__(self, colour):
        self.colour = colour

    def __eq__(self, other):
        return self.colour == other.colour

    def __repr__(self):
        return 'Ball(colour={colour})'.format(colour=self.colour)

class Box:
    def __init__(self, colour):
        self.colour = colour

    def __eq__(self, other):
        return self.colour == other.colour

    def __repr__(self):
        return 'Box(colour={colour})'.format(colour=self.colour)


class Board:
    def __init__(self, WIDTH, HEIGHT, COLOURS):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.COLOURS = COLOURS
        self.balls = self._generate_random_arrangement_of_balls()
        self.nmoves = 0
        self.score = 0
        self.currentScore = 0
        self.highScore = self.get_high_score()

        # Public Interface

    def remove_balls(self, position):
        "Mark the balls and remove the marked balls"
        self._markBalls(position)
        self._clearBalls()

    def get_score(self, position):
        "get the score if you remove all the balls connected to the ball at position"
        return len(self._findAdjacentBalls(position))**2

    def get_high_score(self):
        with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data/TopScores.txt'), 'r') as f:
            score = f.readline()
            if len(score) > 0:
                return int(score)
            else:
                return 0

    def update_high_score(self):
        if self.score >= self.highScore:
            self.highScore = self.score
            with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data/TopScores.txt'), 'r') as f:
                score = f.write(str(self.score))

    def is_game_over(self):
        "Returns True if the Game is over and False otherwise"
        for x in range(self.width):
            for y in range(self.height):
                if len(self._adjacent((x, y))) > 0:
                    return False
        self.update_high_score()
        return True

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


    def _adjacent(self, position):
        "returns the list of balls of the same colour adjacent to the ball at position"
        x, y = position
        colour = self.balls[x][y].colour
        adjacent_balls = set([(x,y)])
        stack = [(x,y)]
        visited = set([x,y])
        while stack:
            x, y = stack.pop()
            for i in [max(0, x-1), min(self.HEIGHT-1, x+1)]: # there is an error here, right? 0 might not be adjacent
                for j in [max(0, y-1), min(self.WIDTH-1, y+1)]:
                    if self.balls[i][j].colour == colour and (i,j) not in visited:
                        adjacent_balls.add((i, j))
                        stack.append((i, j))
                    visited.add((i, j))
        return adjacent_balls

    def make_move(self, position):
        pass

    def _markBalls(self, position):
        "Mark the balls that need to be deleted"
        connectedballs = self._findAdjacentBalls(position)
        if len(connectedballs) == 1:  # means that it has no similarly coloured balls as neighbors
            return
        self.score += self.get_score(position)
        self.nmoves += 1
        for ballposition in connectedballs:
            x, y = ballposition
            self.balls[x][y] = None
            self.nballsleft -= 1

    def _clearBalls(self):
        "delete the balls and let them fall into space vacated by removed balls"
        for i in range(self.width):
            for j in range(self.height):
                if self.balls[i][j] is None:
                    for k in reversed(range(j)):
                        self.balls[i][k + 1] = self.balls[i][k]
                    self.balls[i][0] = None
        # shift to the left when the last row has an empty column
        for i in reversed(range(self.width)):  # through columns
            if self.balls[i][-1] is None:
                for j in range(self.height):
                    for k in (range(i, self.width - 1)):
                        self.balls[k][j] = self.balls[k + 1][j]
                    self.balls[-1][j] = None
        if self.score > self.highScore:
            self.highScore = self.score

