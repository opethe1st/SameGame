class Ball:

    def __init__(self, colour):
        self.colour = colour

    def __eq__(self, other):
        return self.colour == other.colour if type(self) == type(other) else False  # pylint: disable=C0123

    def __repr__(self):
        return 'Ball(colour={colour})'.format(colour=self.colour)
