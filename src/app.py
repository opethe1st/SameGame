import sys

from same.model import SameBoard
from same.model import Scorer
from same.data.constants import ColourScheme
from same.views.gui_client import GuiClient
from same.views.pygame_client import PyGameClient
from same.views.events import BallClickedEvent
from same.views.events import GameQuit

# These are the settings for pyinstaller
# we are running in a bundle if sys.frozen else normal python
BASE_DIR = sys._MEIPASS if getattr(sys, 'frozen', False) else '.'  # pylint: disable=E1101, protected-access


class SameGame:

    def __init__(self, board: SameBoard, gui_client: GuiClient):
        self.board = board
        self.gui_client = gui_client

    def play_game(self):
        changed = False
        self.gui_client.draw_board(balls=self.board.get_balls(), boxes=self.board.get_boxes())
        self.gui_client.draw_score_board(score=self.board.get_current_score(), highest_score=self.board.get_high_score(), current_move_score=0, moves=self.board.num_moves)
        while True:
            # handle events
            for event in self.gui_client.get_events():
                if isinstance(event, BallClickedEvent):
                    self.board.make_move(position=event.position)
                    changed = True
                elif isinstance(event, GameQuit):
                    self.gui_client.end_game()
            # draw the board again
            if changed:
                self.gui_client.draw_board(balls=self.board.get_balls(), boxes=self.board.get_boxes())
                changed = False
            current_move_score = self.board.calculate_score(ball_position=self.gui_client.get_current_ball())
            self.gui_client.draw_score_board(score=self.board.get_current_score(), highest_score=self.board.get_high_score(), current_move_score=current_move_score, moves=self.board.num_moves)
            if self.board.is_game_over():
                self.gui_client.game_over(score=self.board.get_current_score(), high_score=self.board.get_high_score())
                if self.board.get_current_score() > self.board.get_high_score():
                    self.board.update_high_score(new_high_score=self.board.get_current_score())



def main(num_columns: int = 16, num_rows: int = 14, size: int = 32):
    aScorer = Scorer()  # pylint: disable=invalid-name
    aBoard = SameBoard(num_rows=num_rows, num_columns=num_columns, num_colours=4, scorer=aScorer)  # pylint: disable=invalid-name
    aGuiClient = PyGameClient(size=size, num_rows=num_rows, num_columns=num_columns, score_board_height=100, colours=ColourScheme.MONFAVORITE)  # pylint: disable=invalid-name
    sameGame = SameGame(board=aBoard, gui_client=aGuiClient)  # pylint: disable=invalid-name
    sameGame.play_game()


main()
