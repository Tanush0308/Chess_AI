from ai.evaluation import evaluate_board

transposition_table = {}


def get_board_key(gs):
    return str(gs.board) + str(gs.white_to_move)


def minimax(gs, depth, alpha, beta, maximizing_player):

    key = get_board_key(gs)

    # ✅ Check cache FIRST
    if key in transposition_table:
        return transposition_table[key]

    # ✅ Base case
    if depth == 0:
        score = evaluate_board(gs)
        transposition_table[key] = score
        return score

    moves = gs.get_valid_moves()

    if maximizing_player:

        max_eval = float("-inf")

        for move in moves:

            gs.make_move(move)

            evaluation = minimax(gs, depth-1, alpha, beta, False)

            gs.undo_move()

            max_eval = max(max_eval, evaluation)
            alpha = max(alpha, evaluation)

            if beta <= alpha:
                break

        transposition_table[key] = max_eval
        return max_eval

    else:

        min_eval = float("inf")

        for move in moves:

            gs.make_move(move)

            evaluation = minimax(gs, depth-1, alpha, beta, True)

            gs.undo_move()

            min_eval = min(min_eval, evaluation)
            beta = min(beta, evaluation)

            if beta <= alpha:
                break

        transposition_table[key] = min_eval
        return min_eval