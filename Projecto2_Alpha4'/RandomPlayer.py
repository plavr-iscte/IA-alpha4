import random
from Player import Player


class RandomAIPlayer(Player):
    def get_move(self, board):
        return random.choice(board.get_valid_moves())

