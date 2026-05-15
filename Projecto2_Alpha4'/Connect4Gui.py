# =========================
# PYGAME UI
# =========================
import sys

import pygame
from numpy.ma.extras import row_stack

from HumanPlayer import HumanPlayer

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

SQUARESIZE = 100
RADIUS = SQUARESIZE // 2 - 5

class Connect4Gui:
    def __init__(self, board, rows, cols):
        self.board = board
        self.rows = rows
        self.cols = cols


        self.width = self.cols * SQUARESIZE
        self.height = (self.rows + 2) * SQUARESIZE

    def init(self, board):
        pygame.init()
        pygame.display.set_caption("Connect 4")
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.draw_board(board)
        self.font = pygame.font.SysFont("monospace", 50)

    def draw_board(self, board):
        for c in range(self.cols):
            for r in range(self.rows):
                pygame.draw.rect(self.screen, BLUE,
                                 (c*SQUARESIZE, (r+2)*SQUARESIZE, SQUARESIZE, SQUARESIZE))
                pygame.draw.circle(self.screen, BLACK,
                                   (c*SQUARESIZE + SQUARESIZE//2,
                                    (r+2)*SQUARESIZE + SQUARESIZE//2),
                                   RADIUS)

        for c in range(self.cols):
            for r in range(self.rows):
                if board.grid[r][c] == 1:
                    color = RED
                elif board.grid[r][c] == 2:
                    color = YELLOW
                else:
                    continue

                pygame.draw.circle(self.screen, color,
                                   (c*SQUARESIZE + SQUARESIZE//2,
                                    (r+2)*SQUARESIZE + SQUARESIZE//2),
                                   RADIUS)

        pygame.display.update()

    def deal_with_events(self, board, current_player):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if isinstance(current_player, HumanPlayer):
                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(self.screen, BLACK, (0, 0, self.width, SQUARESIZE * 2))
                    posx = event.pos[0]
                    color = RED if current_player.piece == 1 else YELLOW
                    pygame.draw.circle(self.screen, color, (posx, SQUARESIZE + SQUARESIZE // 2), RADIUS)
                    pygame.display.update()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    col = event.pos[0] // SQUARESIZE
                    current_player.set_move(col)


    def update_winner(self, winner):
        label = self.font.render(f"Player {winner.piece} wins!", True,
                                 RED if winner.piece == 1 else YELLOW)
        self.screen.blit(label, (40, 10))

    def draw_game(self):
        label = self.font.render("Draw!", True, YELLOW)
        self.screen.blit(label, (40, 10))

    def game_over(self):
        pygame.display.update()
        pygame.time.wait(3000)