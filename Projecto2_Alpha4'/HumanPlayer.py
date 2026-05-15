from Player import Player

class HumanPlayer(Player):
    def __init__(self, piece):
        super().__init__(piece)
        self.selected_col = None

    def set_move(self, col):
        self.selected_col = col

    def get_move(self, board):
        move = self.selected_col
        self.selected_col = None
        return move

