from unittest import TestCase

from same.model.scorer import Scorer

class  ScoreTestCase(TestCase):

    def setUp(self):
        self.scorer = Scorer()


class TestGetCurrentScore(ScoreTestCase):

    def test_get_current_score(self):
        score = 5
        self.scorer.current_score = score
        self.assertEqual(self.scorer.get_current_score(), score)


class TestUpdateCurrentScore(ScoreTestCase):

    def test_update_current_score(self):
        score = 5
        self.scorer.current_score = score
        self.scorer.update_current_score(score=13)
        self.assertEqual(self.scorer.get_current_score(), 18)


class TestGetScore(ScoreTestCase):

    def test_calculate_score(self):
        ball_positions = [(0, 0), (0, 1), (0, 2)]
        returned_score = self.scorer.calculate_score(ball_positions=ball_positions)
        self.assertEqual(returned_score, 9)

    def test_calculate_score_zero(self):
        ball_positions = []
        returned_score = self.scorer.calculate_score(ball_positions=ball_positions)
        self.assertEqual(returned_score, 0)
