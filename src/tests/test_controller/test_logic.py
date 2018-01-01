from unittest.mock import Mock
from unittest.case import TestCase
from pprint import pprint

from same.controller import Ball
from same.controller import Box
from same.controller import Board
from same.controller import Scorer


class TestBall(TestCase):

    def test_colour(self):
        colour = 'red'
        ball = Ball(colour=colour)
        self.assertEqual(ball.colour, colour)

    def test_equals(self):
        first_red_ball = Ball(colour='red')
        second_red_ball = Ball(colour='red')
        self.assertEqual(first_red_ball, second_red_ball)


class TestBox(TestCase):

    def test_colour(self):
        colour = 'red'
        box = Box(colour=colour)
        self.assertEqual(box.colour, colour)


class TestBoard(TestCase):

    def setUp(self):
        self.COLOURS = [1, 3, 4, 5, 6]
        self.height = 5
        self.width = 3
        self.scorer = Mock(spec_set=Scorer)
        self.Board = Board(WIDTH=self.width, HEIGHT=self.height, COLOURS=self.COLOURS, scorer=self.scorer)
        self.Board.start_game()


class TestGenerateRandomBalls(TestBoard):

    # make sure there are balls on every position on the board
    def test_balls_non_empty(self):
        balls = self.Board._generate_random_arrangement_of_balls()
        for row_balls in balls:
            for ball in row_balls:
                self.fail('ball cannot be None') if ball is None else None

    # make sure there size is what we expect
    def test_board_size(self):
        balls = self.Board._generate_random_arrangement_of_balls()
        self.assertEqual(len(balls[0]), self.width)
        self.assertEqual(len(balls), self.height)

    # make sure only the colours from COLOURS are used.
    def test_colours(self):
        balls = self.Board._generate_random_arrangement_of_balls()
        colours = set()
        for row_balls in balls:
            for ball in row_balls:
                colours.add(ball.colour)
        expected_colours = set(self.COLOURS)
        self.assertTrue(colours <= expected_colours)


class TestGenerateBoxes(TestBoard):

    def test_size_box_arrays(self):
        boxes = self.Board.generate_boxes()
        self.assertEqual(2*self.height-1, len(boxes))
        self.assertEqual(2*self.width-1, len(boxes[0]))

    def test_all_balls_the_same_colour(self):
        self.Board.balls = [[Ball(colour='red') for i in range(self.width)] for j in range(self.height)]
        boxes = self.Board.generate_boxes()
        n_rows = len(boxes)
        n_cols = len(boxes[0])
        for i in range(n_rows):
            for j in range(n_cols):
                if (i+j)%2 == 1:
                    if boxes[i][j].colour != 'red':
                        self.fail()

    def test_no_boxes(self):
        self.Board = Board(WIDTH=2, HEIGHT=2, COLOURS=self.COLOURS, scorer=self.scorer)
        self.Board.balls = [[Ball(colour='red'), Ball(colour='blue')], [Ball(colour='blue'), Ball(colour='red')]]
        boxes = self.Board.generate_boxes()
        n_rows = len(boxes)
        n_cols = len(boxes[0])
        for i in range(n_rows):
            for j in range(n_cols):
                if boxes[i][j] is not None:
                    self.fail()

    def test_a_boxes(self):
        self.Board = Board(WIDTH=2, HEIGHT=2, COLOURS=self.COLOURS, scorer=self.scorer)
        self.Board.balls = [[Ball(colour='red'), Ball(colour='red')], [Ball(colour='blue'), Ball(colour='blue')]]
        boxes = self.Board.generate_boxes()
        expectedBoxes = [[None, Box(colour='red'), None], [None, None, None], [None, Box(colour='blue'), None]]
        self.assertListEqual(boxes, expectedBoxes)


class TestAdjacentBalls(TestBoard):

    def setUp(self):
        super().setUp()
        self.Board = Board(WIDTH=2, HEIGHT=2, COLOURS=self.COLOURS, scorer=self.scorer)

    def test_adjacent_balls(self):
        self.Board.balls = [[Ball(colour='red'), Ball(colour='red')], [Ball(colour='blue'), Ball(colour='blue')]]
        adjacent_balls = self.Board._adjacent((0, 0))
        expected_balls = set([(0,0), (0, 1)])
        self.assertEqual(adjacent_balls, expected_balls)

    def test_adjacent_balls_all(self):
        self.Board.balls = [[Ball(colour='red'), Ball(colour='red')], [Ball(colour='red'), Ball(colour='red')]]
        adjacent_balls = self.Board._adjacent((0, 0))
        expected_balls = set([(0,0), (0, 1), (1, 0), (1, 1)])
        self.assertEqual(adjacent_balls, expected_balls)

    def test_adjacent_balls_random(self):
        self.Board = Board(WIDTH=3, HEIGHT=2, COLOURS=self.COLOURS, scorer=self.scorer)
        self.Board.balls = [[Ball(colour='red'), Ball(colour='red'), Ball(colour='red')], [Ball(colour='red'), Ball(colour='blue'), Ball(colour='blue')]]
        adjacent_balls = self.Board._adjacent((0, 0))
        expected_balls = set([(0,0), (0, 1), (0, 2), (1, 0)])
        self.assertEqual(adjacent_balls, expected_balls)

    def test_just_one_adjacent_ball(self):
        self.Board = Board(WIDTH=3, HEIGHT=2, COLOURS=self.COLOURS, scorer=self.scorer)
        self.Board.balls = [[Ball(colour='red'), Ball(colour='red'), Ball(colour='red')], [Ball(colour='red'), Ball(colour='red'), Ball(colour='blue')]]
        adjacent_balls = self.Board._adjacent((1, 2))
        expected_balls = set([(1, 2)])
        self.assertEqual(adjacent_balls, expected_balls)


class TestMakeMove(TestBoard):

    def test_make_move(self):
        self.Board.mark_balls_to_remove = Mock()
        self.Board.make_balls_fall = Mock()
        self.Board.remove_empty_rows_between_columns = Mock()
        self.Board.convert_cols_to_rows = Mock()

        self.Board.make_move(position=(0, 0))

        self.Board.mark_balls_to_remove.assert_called()
        self.Board.make_balls_fall.assert_called()
        self.Board.remove_empty_rows_between_columns.assert_called()
        self.Board.convert_cols_to_rows.assert_called()


class TestMarkBallsToRemove(TestBoard):

    def test_balls_set_to_None(self):
        self.Board.balls = [[Ball(colour='red'), Ball(colour='red')], [Ball(colour='blue'), Ball(colour='blue')]]
        self.Board._adjacent = Mock()
        self.Board._adjacent.return_value = set([(0, 0), (0, 1)])
        self.Board.mark_balls_to_remove(position=(0, 0))
        self.assertEqual(self.Board.balls, [[None, None], [Ball(colour='blue'), Ball(colour='blue')]])


class TestConvertRowsToColumn(TestBoard):

    def test_balls(self):
        self.Board = Board(WIDTH=3, HEIGHT=2, COLOURS=self.COLOURS, scorer=self.scorer)
        self.Board.balls = [[Ball(colour='red'), Ball(colour='red'), Ball(colour='green')], [Ball(colour='blue'), Ball(colour='blue'), Ball(colour='green')]]
        csr_balls = self.Board.convert_rows_to_columns()
        self.assertEqual(csr_balls, [[Ball(colour='blue'), Ball(colour='red')], [Ball(colour='blue'), Ball(colour='red')], [Ball(colour='green'), Ball(colour='green')]])


class TestMakeBallsFall(TestBoard):

    def test_balls(self):
        self.Board = Board(WIDTH=3, HEIGHT=2, COLOURS=self.COLOURS, scorer=self.scorer)
        self.Board.convert_rows_to_columns = Mock()
        self.Board.convert_rows_to_columns.return_value = [[Ball(colour='red'), Ball(colour='red'), Ball(colour='green')], [None, None, Ball(colour='green')]]
        csr_balls = self.Board.make_balls_fall()
        self.assertEqual(csr_balls, [[Ball(colour='red'), Ball(colour='red'), Ball(colour='green')], [Ball(colour='green'), None, None]])


class TestRemoveEmptyRowsBetweenColumns(TestBoard):

    def test_balls(self):
        self.Board = Board(WIDTH=3, HEIGHT=3, COLOURS=self.COLOURS, scorer=self.scorer)
        csr_balls = [[Ball(colour='red'), Ball(colour='red'), Ball(colour='green')], [None, None, None], [Ball(colour='red'), Ball(colour='red'), Ball(colour='green')]]
        no_empty_cols_balls = self.Board.remove_empty_rows_between_columns(csr_balls=csr_balls)
        expected_no_empty_cols_balls = [[Ball(colour='red'), Ball(colour='red'), Ball(colour='green')], [Ball(colour='red'), Ball(colour='red'), Ball(colour='green')], [None, None, None]]
        self.assertEqual(no_empty_cols_balls, expected_no_empty_cols_balls)


class TestConvertColsToRows(TestBoard):

    def test_balls(self):
        self.Board = Board(WIDTH=3, HEIGHT=2, COLOURS=self.COLOURS, scorer=self.scorer)
        self.Board.balls = [[None for i in range(3)] for j in range(2)]
        self.Board.convert_cols_to_rows(csr_balls=[[Ball(colour='blue'), Ball(colour='red')], [Ball(colour='blue'), Ball(colour='red')], [Ball(colour='green'), Ball(colour='green')]])
        expected_balls = [[Ball(colour='red'), Ball(colour='red'), Ball(colour='green')], [Ball(colour='blue'), Ball(colour='blue'), Ball(colour='green')]]
        self.assertEqual(self.Board.balls, expected_balls)
