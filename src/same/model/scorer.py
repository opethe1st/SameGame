#  augment later to talk to the database
class Scorer:

    def __init__(self):
        self.current_score = 0
        self.high_score = 0

    def get_current_score(self):
        return self.current_score

    def update_current_score(self, score):
        self.current_score += score
        return self.current_score

    def get_score(self, balls):  # pylint: disable=unused-argument
        return len(balls)**2 if len(balls) > 1 else 0

    def get_high_score(self):
        return 0

    def update_high_score(self, new_high_score):
        self.high_score = new_high_score
