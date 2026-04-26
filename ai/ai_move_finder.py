from .minimax import minimax, transposition_table
import random


def find_best_move(gs, depth):

    transposition_table.clear()

    best_move = None
    moves = gs.get_valid_moves()
    random.shuffle(moves)

    maximizing = gs.white_to_move

    best_score = float("-inf") if maximizing else float("inf")   

    for move in moves:

        gs.make_move(move)

        score = minimax(gs, depth-1, -10000, 10000, not maximizing)

        gs.undo_move()

        if maximizing:

            if score > best_score:
                best_score = score
                best_move = move

        else:

            if score < best_score:
                best_score = score
                best_move = move

    return best_move