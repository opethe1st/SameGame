#  augment later to talk to the database
class Scorer:

    def __init__(self):
        self.score = 0

    def get_current_score(self):
        return 0

    def get_score(self, balls):  # pylint: disable=unused-argument
        return self.score

    def set_score(self, new_score):
        self.score = new_score

    def get_high_score(self):
        return 0

    def update_high_score(self, new_high_score):
        self.score = new_high_score
