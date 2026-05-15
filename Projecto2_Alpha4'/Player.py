# =========================
# PLAYERS
# =========================

class Player:
    def __init__(self, piece):
        self.piece = piece

    def get_move(self, board):
        raise NotImplementedError
