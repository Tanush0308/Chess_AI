from ai.evaluation import evaluate_board


def minimax(gs, depth, alpha, beta, maximizing_player):

    moves = gs.get_valid_moves()

    if depth == 0 or len(moves) == 0:
        return evaluate_board(gs.board)

    if maximizing_player:

        max_eval = -9999

        for move in moves:

            gs.make_move(move)

            evaluation = minimax(gs, depth-1, alpha, beta, False)

            gs.undo_move()

            max_eval = max(max_eval, evaluation)

            alpha = max(alpha, evaluation)

            if beta <= alpha:
                break

        return max_eval

    else:

        min_eval = 9999

        for move in moves:

            gs.make_move(move)

            evaluation = minimax(gs, depth-1, alpha, beta, True)

            gs.undo_move()

            min_eval = min(min_eval, evaluation)

            beta = min(beta, evaluation)

            if beta <= alpha:
                break

        return min_eval