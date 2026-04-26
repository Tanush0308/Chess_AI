class Move:

    def __init__(self, start_sq, end_sq, board):

        self.start_row = start_sq[0]
        self.start_col = start_sq[1]

        self.end_row = end_sq[0]
        self.end_col = end_sq[1]

        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]

        # -----------------------------
        # PAWN PROMOTION
        # -----------------------------
        self.is_pawn_promotion = False

        if self.piece_moved == "wP" and self.end_row == 0:
            self.is_pawn_promotion = True

        elif self.piece_moved == "bP" and self.end_row == 7:
            self.is_pawn_promotion = True