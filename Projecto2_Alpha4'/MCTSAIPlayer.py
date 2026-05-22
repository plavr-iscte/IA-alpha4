import math
import random
from Player import Player

class MCTSNode:
    def __init__(self, board, player, parent=None, move=None):
        self.board          = board
        self.player         = player
        self.parent         = parent
        self.move           = move
        self.children       = []
        self.untried_moves  = board.get_valid_moves()
        self.visits         = 0
        self.wins           = 0.0


class MCTSAIPlayer(Player):
    def __init__(self, piece, max_iterations=800, exploration=math.sqrt(2)):
        super().__init__(piece)
        self.max_iterations = max_iterations
        self.exploration = exploration

    def get_move(self, board):
        valid_moves = board.get_valid_moves()

        if not valid_moves:
            return None

        if len(valid_moves) == 1:
            return valid_moves[0]

        root = MCTSNode(
            board=board.copy(),
            player=self.piece
        )

        for _ in range(self.max_iterations):
            node    = self._select(root)
            winner  = self._terminal_winner(node.board)

            if winner is None and not node.board.is_board_full():
                node = self._expand(node)

            winner = self._simulate(
                board   = node.board.copy(),
                player  = node.player,
            )

            self._backpropagate(node, winner)

        if not root.children:
            return random.choice(valid_moves)

        best_child = max(root.children, key=lambda child: child.visits)

        return best_child.move
    
    def _select(self, node):
        while not node.untried_moves and node.children:
            node = max(node.children, key=self._ucb1)

        return node

    def _expand(self, node):
        move = node.untried_moves.pop(
            random.randrange(len(node.untried_moves))
        )

        new_board = node.board.copy()
        new_board.drop_piece(move, node.player)

        next_player = self._opposite(node.player)

        child = MCTSNode(
            board   = new_board,
            player  = next_player,
            parent  = node,
            move    = move
        )

        node.children.append(child)
        return child

    def _simulate(self, board, player):
        current_player = player

        while True:
            winner = self._terminal_winner(board)
            if winner is not None:
                return winner
            if board.is_board_full():
                return 0

            valid_moves = board.get_valid_moves()
            if not valid_moves:
                return 0

            move = self._rollout_policy(board, current_player, valid_moves)
            board.drop_piece(move, current_player)
            current_player = self._opposite(current_player)

    def _rollout_policy(self, board, current_player, valid_moves):
        for col in valid_moves:
            test_board = board.copy()
            test_board.drop_piece(col, current_player)
        
            if test_board.check_winner(current_player):
                return col

        opponent = self._opposite(current_player)

        for col in valid_moves:
            test_board = board.copy()
            test_board.drop_piece(col, opponent)

            if test_board.check_winner(opponent):
                return col

        center = board.cols // 2

        weights = [
            1.0 / (1 + abs(col - center))
            for col in valid_moves
        ]

        return random.choices(valid_moves, weights=weights, k=1)[0]

    def _backpropagate(self, node, winner):
        while node is not None:
            node.visits += 1

            if winner == self.piece:
                node.wins += 1.0
            elif winner == 0:
                node.wins += 0.5

            node = node.parent

    def _ucb1(self, node):
        if node.visits == 0:
            return math.inf
        
        exploitation = node.wins / node.visits

        exploration = self.exploration * math.sqrt(
            math.log(node.parent.visits) / node.visits
        )

        return exploitation + exploration

    def _terminal_winner(self, board):
        if board.check_winner(1): return 1

        if board.check_winner(2): return 2

        return None

    
    def _opposite(self, piece):
        return 2 if piece == 1 else 1