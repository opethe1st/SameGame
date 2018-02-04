from unittest import mock
from unittest.mock import Mock
from unittest.case import TestCase

from same.model import Ball
from same.model import Box
from same.model import SameBoard
from same.model import Scorer


class BoardTestCase(TestCase):

    def setUp(self):
        self.num_colours = 5
        self.num_rows = 5
        self.num_columns = 3
        self.scorer = mock.create_autospec(spec=Scorer, spec_set=True)
        self.board = SameBoard(num_columns=self.num_columns, num_rows=self.num_rows, num_colours=self.num_colours, scorer=self.scorer)


class TestGenerateRandomBalls(BoardTestCase):

    # make sure there are balls on every position on the board
    def test_balls_non_empty(self):
        balls = self.board.generate_random_balls()
        for row_balls in balls:
            for ball in row_balls:
                if ball is None:
                    self.fail('ball cannot be None')

    # make sure there size is what we expect
    def test_board_size(self):
        balls = self.board.generate_random_balls()
        self.assertEqual(len(balls[0]), self.num_columns)
        self.assertEqual(len(balls), self.num_rows)

    # make sure only the colours from colours are used.
    def test_colours(self):
        balls = self.board.generate_random_balls()
        colours = set()
        for row_balls in balls:
            for ball in row_balls:
                colours.add(ball.colour)
        expected_colours = set([i for i in range(self.num_colours)])
        self.assertTrue(colours <= expected_colours)


class TestGenerateBoxes(BoardTestCase):

    def test_size_box_arrays(self):
        boxes = self.board.generate_boxes()
        self.assertEqual(2 * self.num_rows - 1, len(boxes))
        self.assertEqual(2 * self.num_columns - 1, len(boxes[0]))

    def test_all_balls_the_same_colour(self):
        self.board.balls = [[Ball(colour='red') for i in range(self.num_columns)] for j in range(self.num_rows)]
        boxes = self.board.generate_boxes()
        n_rows = len(boxes)
        n_cols = len(boxes[0])
        for i in range(n_rows):
            for j in range(n_cols):
                if (i + j) % 2 == 1:
                    if boxes[i][j].colour != 'red':
                        self.fail()

    def test_no_boxes(self):
        self.board = SameBoard(num_columns=2, num_rows=2, num_colours=self.num_colours, scorer=self.scorer)
        self.board.balls = [[Ball(colour='red'), Ball(colour='blue')], [Ball(colour='blue'), Ball(colour='red')]]
        boxes = self.board.generate_boxes()
        n_rows = len(boxes)
        n_cols = len(boxes[0])
        for i in range(n_rows):
            for j in range(n_cols):
                if boxes[i][j] is not None:
                    self.fail()

    def test_a_boxes(self):
        self.board = SameBoard(num_columns=2, num_rows=2, num_colours=self.num_colours, scorer=self.scorer)
        self.board.balls = [[Ball(colour='red'), Ball(colour='red')], [Ball(colour='blue'), Ball(colour='blue')]]
        boxes = self.board.generate_boxes()
        expected_boxes = [[None, Box(colour='red'), None], [None, None, None], [None, Box(colour='blue'), None]]
        self.assertListEqual(boxes, expected_boxes)


class TestAdjacentBalls(BoardTestCase):

    def setUp(self):
        super().setUp()
        self.board = SameBoard(num_columns=2, num_rows=2, num_colours=self.num_colours, scorer=self.scorer)

    def test_adjacent_balls(self):
        balls = [[Ball(colour='red'), Ball(colour='red')], [Ball(colour='blue'), Ball(colour='blue')]]
        adjacent_balls = self.board.adjacent(balls=balls, position=(0, 0))
        expected_balls = set([(0, 0), (0, 1)])
        self.assertEqual(adjacent_balls, expected_balls)

    def test_adjacent_balls_all(self):
        balls = [[Ball(colour='red'), Ball(colour='red')], [Ball(colour='red'), Ball(colour='red')]]
        adjacent_balls = self.board.adjacent(balls=balls, position=(0, 0))
        expected_balls = set([(0, 0), (0, 1), (1, 0), (1, 1)])
        self.assertEqual(adjacent_balls, expected_balls)

    def test_adjacent_balls_random(self):
        self.board = SameBoard(num_columns=3, num_rows=2, num_colours=self.num_colours, scorer=self.scorer)
        balls = [[Ball(colour='red'), Ball(colour='red'), Ball(colour='red')], [Ball(colour='red'), Ball(colour='blue'), Ball(colour='blue')]]
        adjacent_balls = self.board.adjacent(balls=balls, position=(0, 0))
        expected_balls = set([(0, 0), (0, 1), (0, 2), (1, 0)])
        self.assertEqual(adjacent_balls, expected_balls)

    def test_just_one_adjacent_ball(self):
        self.board = SameBoard(num_columns=3, num_rows=2, num_colours=self.num_colours, scorer=self.scorer)
        balls = [[Ball(colour='red'), Ball(colour='red'), Ball(colour='red')], [Ball(colour='red'), Ball(colour='red'), Ball(colour='blue')]]
        adjacent_balls = self.board.adjacent(balls=balls, position=(2, 1))
        expected_balls = set([(1, 2)])
        self.assertEqual(adjacent_balls, expected_balls)


class TestMakeMove(BoardTestCase):

    def test_make_move(self):
        self.board.mark_balls_to_remove = Mock()
        self.board.make_balls_fall = Mock()
        self.board.remove_empty_rows = Mock()
        self.board.transpose = Mock()

        self.board.make_move(position=(0, 0))

        self.board.mark_balls_to_remove.assert_called()
        self.board.make_balls_fall.assert_called()
        self.board.remove_empty_rows.assert_called()
        self.board.transpose.assert_called()


class TestMarkBallsToRemove(BoardTestCase):

    def test_balls_set_to_none(self):
        balls = [[Ball(colour='red'), Ball(colour='red')], [Ball(colour='blue'), Ball(colour='blue')]]
        modified_balls = self.board.mark_balls_to_remove(balls=balls, positions_of_balls_to_remove=[(0, 0), (0, 1)])
        self.assertEqual(modified_balls, [[None, None], [Ball(colour='blue'), Ball(colour='blue')]])


class TestTranspose(BoardTestCase):

    def test_balls(self):
        self.board = SameBoard(num_columns=3, num_rows=2, num_colours=self.num_colours, scorer=self.scorer)
        self.board.balls = [[None for i in range(3)] for j in range(2)]
        transposed_balls = self.board.transpose(balls=[[Ball(colour='red'), Ball(colour='blue')], [Ball(colour='red'), Ball(colour='blue')], [Ball(colour='green'), Ball(colour='green')]])
        expected_balls = [[Ball(colour='red'), Ball(colour='red'), Ball(colour='green')], [Ball(colour='blue'), Ball(colour='blue'), Ball(colour='green')]]
        self.assertEqual(transposed_balls, expected_balls)


class TestMakeBallsFall(BoardTestCase):

    def test_balls(self):
        self.board = SameBoard(num_columns=3, num_rows=2, num_colours=self.num_colours, scorer=self.scorer)
        self.board.transpose = Mock()
        balls = [[Ball(colour='red'), Ball(colour='red'), Ball(colour='green')], [None, Ball(colour='green'), None]]
        self.board.transpose.return_value = balls
        csr_balls = self.board.make_balls_fall(balls=balls)
        self.assertEqual(csr_balls, [[Ball(colour='red'), Ball(colour='red'), Ball(colour='green')], [None, None, Ball(colour='green')]])


class TestRemoveEmptyRowsBetweenColumns(BoardTestCase):

    def test_balls(self):
        self.board = SameBoard(num_columns=3, num_rows=3, num_colours=self.num_colours, scorer=self.scorer)
        csr_balls = [[Ball(colour='red'), Ball(colour='red'), Ball(colour='green')], [None, None, None], [Ball(colour='red'), Ball(colour='red'), Ball(colour='green')]]
        no_empty_cols_balls = self.board.remove_empty_rows(csr_balls=csr_balls)
        expected_no_empty_cols_balls = [[Ball(colour='red'), Ball(colour='red'), Ball(colour='green')], [Ball(colour='red'), Ball(colour='red'), Ball(colour='green')], [None, None, None]]
        self.assertEqual(no_empty_cols_balls, expected_no_empty_cols_balls)
