from typing import List
import shelve


class Scorer:

    def __init__(self):
        self.current_score = 0
        with shelve.open('high_score') as database:
            self.high_score = database.get('high_score', 0)

    def get_current_score(self):
        return self.current_score

    def update_current_score(self, score: int):
        self.current_score += score
        return self.current_score

    def calculate_score(self, ball_positions: List[tuple]):  # pylint: disable=unused-argument
        return len(ball_positions)**2 if len(ball_positions) > 1 else 0

    def get_high_score(self):
        return self.high_score

    def update_high_score(self, new_high_score: int):
        with shelve.open('high_score') as database:
            database['high_score'] = new_high_score
            self.high_score = database['high_score']
        return self.high_score
