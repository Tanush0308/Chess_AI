piece_score = {
    "K": 0,
    "Q": 9,
    "R": 5,
    "B": 3,
    "N": 3,
    "P": 1
}

# -----------------------------
# PIECE-SQUARE TABLES
# -----------------------------

knight_table = [
[-5,-4,-3,-3,-3,-3,-4,-5],
[-4,-2, 0, 0, 0, 0,-2,-4],
[-3, 0, 1,1.5,1.5,1, 0,-3],
[-3,0.5,1.5,2,2,1.5,0.5,-3],
[-3,0,1.5,2,2,1.5,0,-3],
[-3,0.5,1,1.5,1.5,1,0.5,-3],
[-4,-2,0,0.5,0.5,0,-2,-4],
[-5,-4,-3,-3,-3,-3,-4,-5]
]

pawn_table = [
[0,0,0,0,0,0,0,0],
[1,1,1,1,1,1,1,1],
[0.5,0.5,1,1.5,1.5,1,0.5,0.5],
[0.2,0.2,0.5,1,1,0.5,0.2,0.2],
[0,0,0,0.8,0.8,0,0,0],
[0.2,-0.2,-0.5,0,0,-0.5,-0.2,0.2],
[0.2,0.5,0.5,-1,-1,0.5,0.5,0.2],
[0,0,0,0,0,0,0,0]
]

bishop_table = [
[-2,-1,-1,-1,-1,-1,-1,-2],
[-1,0,0,0,0,0,0,-1],
[-1,0,0.5,1,1,0.5,0,-1],
[-1,0.5,0.5,1,1,0.5,0.5,-1],
[-1,0,1,1,1,1,0,-1],
[-1,1,1,1,1,1,1,-1],
[-1,0.5,0,0,0,0,0.5,-1],
[-2,-1,-1,-1,-1,-1,-1,-2]
]

rook_table = [
[0,0,0,0,0,0,0,0],
[0.5,1,1,1,1,1,1,0.5],
[-0.5,0,0,0,0,0,0,-0.5],
[-0.5,0,0,0,0,0,0,-0.5],
[-0.5,0,0,0,0,0,0,-0.5],
[-0.5,0,0,0,0,0,0,-0.5],
[-0.5,0,0,0,0,0,0,-0.5],
[0,0,0,0,0,0,0,0]
]

queen_table = [
[-2,-1,-1,-0.5,-0.5,-1,-1,-2],
[-1,0,0,0,0,0,0,-1],
[-1,0,0.5,0.5,0.5,0.5,0,-1],
[-0.5,0,0.5,0.5,0.5,0.5,0,-0.5],
[0,0,0.5,0.5,0.5,0.5,0,-0.5],
[-1,0.5,0.5,0.5,0.5,0.5,0,-1],
[-1,0,0.5,0,0,0,0,-1],
[-2,-1,-1,-0.5,-0.5,-1,-1,-2]
]

# -----------------------------
# EVALUATION FUNCTION
# -----------------------------

def evaluate_board(gs):

    board = gs.board
    score = 0

    for r in range(8):
        for c in range(8):

            piece = board[r][c]

            if piece == "--":
                continue

            value = piece_score[piece[1]]

            # positional bonus
            if piece[1] == "P":
                value += pawn_table[r][c]
            elif piece[1] == "N":
                value += knight_table[r][c]
            elif piece[1] == "B":
                value += bishop_table[r][c]
            elif piece[1] == "R":
                value += rook_table[r][c]
            elif piece[1] == "Q":
                value += queen_table[r][c]

            # add/subtract based on color
            if piece[0] == "w":
                score += value
            else:
                score -= value

    # -----------------------------
    # MOBILITY BONUS
    # -----------------------------
    mobility = len(gs.get_all_possible_moves())
    score += 0.1 * mobility if gs.white_to_move else -0.1 * mobility

    # -----------------------------
    # SIMPLE PAWN STRUCTURE
    # -----------------------------
    for col in range(8):
        white_pawns = 0
        black_pawns = 0

        for row in range(8):
            if board[row][col] == "wP":
                white_pawns += 1
            elif board[row][col] == "bP":
                black_pawns += 1

        if white_pawns > 1:
            score -= 0.2 * white_pawns
        if black_pawns > 1:
            score += 0.2 * black_pawns

    return score