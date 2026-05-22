import math
import random
from Player import Player

class MinimaxAIPlayer(Player):
    def __init__(self, piece, max_depth=4):
        super().__init__(piece)
        self.max_depth = max_depth

    def opponent_piece(self):
        if self.piece == 1: return 2
        else: return 1

    def get_move(self, board):
        valid_moves = board.get_valid_moves()

        if not valid_moves:
            return None

        ordered_moves = self._order_moves(board, valid_moves)

        best_score = -math.inf
        best_moves = []

        alpha   = -math.inf
        beta    = math.inf

        for col in ordered_moves:
            new_board = board.copy()
            new_board.drop_piece(col, self.piece)

            score = self._minimax(
                board=new_board,
                depth=self.max_depth - 1,
                alpha=alpha,
                beta=beta,
                maximizing=False
            )

            if score > best_score:
                best_score = score
                best_moves = [col]
            elif score == best_score:
                best_moves.append(col)

            alpha = max(alpha, best_score)

        return random.choice(best_moves)

    def _minimax(self, board, depth, alpha, beta, maximizing):
        if board.check_winner(self.piece):
            return 1_000_000 + depth

        if board.check_winner(self.opponent_piece()):
            return -1_000_000 - depth

        if board.is_board_full():
            return 0

        if depth == 0: 
            return self.evaluate_board(board, self.piece)

        valid_moves = self._order_moves(board, board.get_valid_moves())

        if maximizing:
            value = -math.inf

            for col in valid_moves:
                child = board.copy()
                child.drop_piece(col, self.piece)

                value = max(
                    value,
                    self._minimax(child, depth-1, alpha, beta, False)
                )

                alpha = max(alpha, value)

                if alpha >= beta: break

            return value
        
        else:
            value = math.inf

            for col in valid_moves:
                child = board.copy()
                child.drop_piece(col, self.opponent_piece())

                value = min(
                    value,
                    self._minimax(child, depth-1, alpha, beta, True)
                )

                beta = min(beta, value)

                if alpha >= beta:
                    break

            return value

    def evaluate_board(self, game, player):
        board = game
        if player == 1: opponent = 2
        else: opponent = 1

        n = board.n_connect

        if board.check_winner(player):
            return 1_000_000

        if board.check_winner(opponent):
            return -1_000_000

        score = 0

        center_col      = board.cols // 2
        center_values   = list(board.grid[:, center_col])

        score += center_values.count(player)*6
        score -= center_values.count(opponent)*6

        for window in self._all_windows(board):
            score += self._score_window(window, player, opponent, n)

        for col in board.get_valid_moves():
            b1 = board.copy()
            b1.drop_piece(col, player)

            if b1.check_winner(player):
                score += 50_000

            b2 = board.copy()
            b2.drop_piece(col, opponent)

            if b2.check_winner(opponent):
                score -= 60_000

        return score

    def _score_window(self, window, player, opponent, n):
        player_count    = window.count(player)
        opponent_count  = window.count(opponent)
        empty_count     = window.count(0)

        if player_count > 0 and opponent_count > 0:
            return 0

        if player_count == n:
            return 100_000

        if opponent_count == n:
            return -100_000

        score = 0

        if player_count == n-1 and empty_count == 1:
            score += 1_000
        elif player_count == n-2 and empty_count == 2:
            score+=80
        elif player_count == 1 and empty_count == n-1:
            score += 5

        if opponent_count == n-1 and empty_count == 1:
            score -= 1_200
        elif opponent_count == n-2 and empty_count == 2:
            score -= 100
        elif opponent_count == 1 and empty_count == n-1:
            score -=4

        return score

    def _all_windows(self, board):
        n       = board.n_connect
        grid    = board.grid

        for r in range(board.rows):
            for c in range(board.cols - n + 1):
                yield list(grid[r, c:c+n])

        for r in range(board.rows - n + 1):
            for c in range(board.cols -n + 1):
                yield [grid[r+i,c] for i in range(n)]

        for r in range(board.rows - n +1):
            for c in range(board.cols - n + 1):
                yield[grid[r+i,c+i] for i in range(n)]

        for r in range(n-1, board.rows):
            for c in range(board.cols - n + 1):
                yield [grid[r - i, c + i] for i in range(n)]

    def _order_moves(self, board, moves):
        center = board.cols // 2
        return sorted(moves, key=lambda col: abs(col - center))