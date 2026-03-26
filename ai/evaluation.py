piece_score = {
    "K": 0,
    "Q": 9,
    "R": 5,
    "B": 3,
    "N": 3,
    "P": 1
}

knight_table = [
[-5,-4,-3,-3,-3,-3,-4,-5],
[-4,-2, 0, 0, 0, 0,-2,-4],
[-3, 0, 1, 1.5,1.5,1, 0,-3],
[-3,0.5,1.5,2,2,1.5,0.5,-3],
[-3,0,1.5,2,2,1.5,0,-3],
[-3,0.5,1,1.5,1.5,1,0.5,-3],
[-4,-2,0,0.5,0.5,0,-2,-4],
[-5,-4,-3,-3,-3,-3,-4,-5]
]


def evaluate_board(board):

    score = 0

    for r in range(8):
        for c in range(8):

            piece = board[r][c]

            if piece == "--":
                continue

            value = piece_score[piece[1]]

            if piece[1] == "N":
                value += knight_table[r][c]

            if piece[0] == "w":
                score += value
            else:
                score -= value

    return score