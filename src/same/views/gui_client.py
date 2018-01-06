class GuiClient:
    '''Abstract class implemented by a client object for a particular GUI framework'''
    def __init__(self, board_position, board_dimensions, score_board_position, score_board_dimensions):
        self.board_position = board_position
        self.board_dimensions = board_dimensions
        self.score_board_position = score_board_position
        self.score_board_dimensions = score_board_dimensions

    def start_game(self):  # needed??? Just the draw initial game
        raise NotImplementedError

    def draw_game(self, balls, boxes, score, highest_score, current_move_score):  # pylint: disable=too-many-arguments
        self.draw_board(balls=balls, boxes=boxes)
        self.draw_score_board(score=score, highest_score=highest_score, current_move_score=current_move_score)

    def draw_board(self, balls, boxes):  # pylint: disable=unused-argument
        raise NotImplementedError

    def draw_score_board(self, score, highest_score, current_move_score):  # pylint: disable=unused-argument
        raise NotImplementedError

    @staticmethod
    def get_clicked_ball():
        '''if a ball was clicked return the position else return None'''
        raise NotImplementedError

    @staticmethod
    def get_current_ball():
        '''return the position of the ball that the mouse is over else None'''
        raise NotImplementedError

    @staticmethod
    def get_events():
        '''return the events if any else None'''
        raise NotImplementedError
