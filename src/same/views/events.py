class Event:
    pass


class BallClickedEvent(Event):
    def __init__(self, position):
        self.position = position


class GameQuit(Event):
    pass
