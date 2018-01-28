from unittest.case import TestCase

from same.model import Ball


class TestBall(TestCase):

    def test_colour(self):
        colour = 'red'
        ball = Ball(colour=colour)
        self.assertEqual(ball.colour, colour)

    def test_equals(self):
        first_red_ball = Ball(colour='red')
        second_red_ball = Ball(colour='red')
        self.assertEqual(first_red_ball, second_red_ball)
