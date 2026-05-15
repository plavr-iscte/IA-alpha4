# =========================
# GAME LOGIC (UI-agnostic)
# =========================
import numpy as np


class Connect4Board:
    def __init__(self, rowns=6, cols=7, n_connect = 4):
        self.rows = rowns
        self.cols = cols
        self.n_connect = n_connect
        self.grid = np.zeros((self.rows, self.cols), dtype=int)

    def copy(self):
        new_board = Connect4Board(self.rows, self.cols, self.n_connect)
        new_board.grid = self.grid.copy()
        return new_board

    def get_valid_moves(self):
        return [c for c in range(self.cols) if self.grid[0][c] == 0]

    def drop_piece(self, col, piece):
        for row in reversed(range(self.rows)):
            if self.grid[row][col] == 0:
                self.grid[row][col] = piece
                return row, col
        raise ValueError("Column is full")

    def is_board_full(self):
        return all(self.grid[0][c] != 0 for c in range(self.cols))

    def check_winner(self, piece):
        # Horizontal
        for r in range(self.rows):
            for c in range(self.cols - self.n_connect +1):
                if all(self.grid[r][c+i] == piece for i in range(self.n_connect)):
                    return True

        # Vertical
        for c in range(self.cols):
            for r in range(self.rows - self.n_connect +1):
                if all(self.grid[r+i][c] == piece for i in range(self.n_connect)):
                    return True

        # Diagonal /
        for r in range(self.n_connect - 1, self.rows):
            for c in range(self.cols - self.n_connect +1):
                if all(self.grid[r-i][c+i] == piece for i in range(self.n_connect)):
                    return True

        # Diagonal \
        for r in range(self.rows - self.n_connect +1):
            for c in range(self.cols - self.n_connect +1):
                if all(self.grid[r+i][c+i] == piece for i in range(self.n_connect)):
                    return True

        return False
