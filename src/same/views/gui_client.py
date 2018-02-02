class GuiClient:
    '''Abstract class implemented by a client class for a particular GUI framework'''

    def __init__(self, size, num_columns, num_rows, board_position, score_board_height, colours):  # pylint: disable=unused-argument
        raise NotImplementedError

    def game_over(self):
        raise NotImplementedError

    def end_game(self):
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
