from unittest.case import TestCase

from same.model import Box


class TestBox(TestCase):

    def test_colour(self):
        colour = 'red'
        box = Box(colour=colour)
        self.assertEqual(box.colour, colour)
