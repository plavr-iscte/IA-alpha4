import time
import pandas as pd

from Connect4Board import Connect4Board
from RandomPlayer import RandomAIPlayer
from MinimaxAIPlayer import MinimaxAIPlayer
from MCTSAIPlayer import MCTSAIPlayer


def play_headless(player1, player2, rows=6, cols=7, n_connect=4):
    board = Connect4Board(rows, cols, n_connect)

    players = [player1, player2]
    turn = 0
    moves = 0

    start = time.perf_counter()

    while True:
        current_player = players[turn]

        move = current_player.get_move(board)

        if move is None or move not in board.get_valid_moves():
            # Invalid move loses immediately.
            winner = 2 if current_player.piece == 1 else 1
            duration = time.perf_counter() - start

            return {
                "winner": winner,
                "moves": moves,
                "duration": duration
            }

        board.drop_piece(move, current_player.piece)
        moves += 1

        if board.check_winner(current_player.piece):
            duration = time.perf_counter() - start

            return {
                "winner": current_player.piece,
                "moves": moves,
                "duration": duration
            }

        if board.is_board_full():
            duration = time.perf_counter() - start

            return {
                "winner": 0,
                "moves": moves,
                "duration": duration
            }

        turn = (turn + 1) % 2


def run_match(comparison_name, player1_factory, player2_factory, number_of_games):
    p1_wins = 0
    p2_wins = 0
    draws = 0
    durations = []

    for _ in range(number_of_games):
        player1 = player1_factory()
        player2 = player2_factory()

        result = play_headless(player1, player2)

        durations.append(result["duration"])

        if result["winner"] == 1:
            p1_wins += 1
        elif result["winner"] == 2:
            p2_wins += 1
        else:
            draws += 1

    return {
        "Comparação": comparison_name,
        "Nº de Jogos": number_of_games,
        "Vitórias Jogador 1": p1_wins,
        "Vitórias Jogador 2": p2_wins,
        "Empates": draws,
        "Taxa de Vitórias Jogador 1": p1_wins / number_of_games,
        "Taxa de Vitórias Jogador 2": p2_wins / number_of_games,
        "Duração Média do Jogo": sum(durations) / len(durations),
        "Duração Máxima": max(durations),
        "Duração Mínima": min(durations),
        "Diferenças de Comportamento Observadas": ""
    }


def main():
    number_of_games = 20

    experiments = []

    experiments.append(
        run_match(
            "Minimax vs Aleatório",
            lambda: MinimaxAIPlayer(piece=1, max_depth=4),
            lambda: RandomAIPlayer(piece=2),
            number_of_games
        )
    )

    experiments.append(
        run_match(
            "MCTS vs Aleatório",
            lambda: MCTSAIPlayer(piece=1, max_iterations=800),
            lambda: RandomAIPlayer(piece=2),
            number_of_games
        )
    )

    experiments.append(
        run_match(
            "1º comb Minimax vs MCTS",
            lambda: MinimaxAIPlayer(piece=1, max_depth=3),
            lambda: MCTSAIPlayer(piece=2, max_iterations=300),
            number_of_games
        )
    )

    experiments.append(
        run_match(
            "2º comb Minimax vs MCTS",
            lambda: MinimaxAIPlayer(piece=1, max_depth=4),
            lambda: MCTSAIPlayer(piece=2, max_iterations=800),
            number_of_games
        )
    )

    experiments.append(
        run_match(
            "3º comb Minimax vs MCTS",
            lambda: MinimaxAIPlayer(piece=1, max_depth=5),
            lambda: MCTSAIPlayer(piece=2, max_iterations=1500),
            number_of_games
        )
    )

    df = pd.DataFrame(experiments)

    df.loc[df["Comparação"] == "Minimax vs Aleatório", "Diferenças de Comportamento Observadas"] = (
        "Minimax tende a controlar o centro, bloquear ameaças imediatas e criar sequências."
    )

    df.loc[df["Comparação"] == "MCTS vs Aleatório", "Diferenças de Comportamento Observadas"] = (
        "MCTS melhora com mais iterações; joga de forma menos determinística e explora várias linhas."
    )

    df.loc[df["Comparação"].str.contains("Minimax vs MCTS"), "Diferenças de Comportamento Observadas"] = (
        "Minimax é mais tático e previsível; MCTS depende da qualidade das simulações e do número de iterações."
    )

    df.to_excel("resultados.xlsx", index=False)

    print(df)
    print("\nFicheiro resultados.xlsx criado com sucesso.")


if __name__ == "__main__":
    main()