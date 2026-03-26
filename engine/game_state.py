from engine.move import Move


class GameState:

    def __init__(self):

        self.board = [

            ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bP","bP","bP","bP","bP","bP","bP","bP"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wP","wP","wP","wP","wP","wP","wP","wP"],
            ["wR","wN","wB","wQ","wK","wB","wN","wR"]

        ]

        self.white_to_move = True
        self.move_log = []

        self.checkmate = False
        self.stalemate = False

        self.move_functions = {
            "P": self.get_pawn_moves,
            "R": self.get_rook_moves,
            "N": self.get_knight_moves,
            "B": self.get_bishop_moves,
            "Q": self.get_queen_moves,
            "K": self.get_king_moves
        }

        self.white_king_location = (7,4)
        self.black_king_location = (0,4)


# -----------------------------
# MAKE MOVE
# -----------------------------
    def make_move(self, move):

        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved

        self.move_log.append(move)

        if move.piece_moved == "wK":
            self.white_king_location = (move.end_row, move.end_col)

        if move.piece_moved == "bK":
            self.black_king_location = (move.end_row, move.end_col)

        self.white_to_move = not self.white_to_move


# -----------------------------
# UNDO MOVE
# -----------------------------
    def undo_move(self):

        if len(self.move_log) != 0:

            move = self.move_log.pop()

            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured

            if move.piece_moved == "wK":
                self.white_king_location = (move.start_row, move.start_col)

            if move.piece_moved == "bK":
                self.black_king_location = (move.start_row, move.start_col)

            self.white_to_move = not self.white_to_move


# -----------------------------
# ALL POSSIBLE MOVES
# -----------------------------
    def get_all_possible_moves(self):

        moves = []

        for r in range(8):
            for c in range(8):

                piece = self.board[r][c]

                if piece == "--":
                    continue

                color = piece[0]
                piece_type = piece[1]

                if (color == "w" and self.white_to_move) or (color == "b" and not self.white_to_move):

                    self.move_functions[piece_type](r, c, moves)

        return moves


# -----------------------------
# VALID MOVES (LEGAL CHESS MOVES)
# -----------------------------
    def get_valid_moves(self):

        moves = self.get_all_possible_moves()

        for i in range(len(moves)-1, -1, -1):

            self.make_move(moves[i])

            self.white_to_move = not self.white_to_move

            if self.in_check():
                moves.remove(moves[i])

            self.white_to_move = not self.white_to_move

            self.undo_move()

        if len(moves) == 0:

            if self.in_check():
                self.checkmate = True
            else:
                self.stalemate = True

        else:
            self.checkmate = False
            self.stalemate = False

        return moves


# -----------------------------
# CHECK DETECTION
# -----------------------------
    def in_check(self):

        if self.white_to_move:
            return self.square_under_attack(*self.white_king_location)
        else:
            return self.square_under_attack(*self.black_king_location)


# -----------------------------
# ATTACKED SQUARE DETECTION
# -----------------------------
    def square_under_attack(self, r, c):

        self.white_to_move = not self.white_to_move
        opponent_moves = self.get_all_possible_moves()
        self.white_to_move = not self.white_to_move

        for move in opponent_moves:
            if move.end_row == r and move.end_col == c:
                return True

        return False


# -----------------------------
# PAWN MOVES
# -----------------------------
    def get_pawn_moves(self, r, c, moves):

        if self.white_to_move:

            if self.board[r-1][c] == "--":
                moves.append(Move((r,c),(r-1,c),self.board))

                if r == 6 and self.board[r-2][c] == "--":
                    moves.append(Move((r,c),(r-2,c),self.board))

            if c-1 >= 0 and self.board[r-1][c-1][0] == "b":
                moves.append(Move((r,c),(r-1,c-1),self.board))

            if c+1 <= 7 and self.board[r-1][c+1][0] == "b":
                moves.append(Move((r,c),(r-1,c+1),self.board))

        else:

            if self.board[r+1][c] == "--":
                moves.append(Move((r,c),(r+1,c),self.board))

                if r == 1 and self.board[r+2][c] == "--":
                    moves.append(Move((r,c),(r+2,c),self.board))

            if c-1 >= 0 and self.board[r+1][c-1][0] == "w":
                moves.append(Move((r,c),(r+1,c-1),self.board))

            if c+1 <= 7 and self.board[r+1][c+1][0] == "w":
                moves.append(Move((r,c),(r+1,c+1),self.board))


# -----------------------------
# ROOK MOVES
# -----------------------------
    def get_rook_moves(self, r, c, moves):

        directions = [(-1,0),(0,-1),(1,0),(0,1)]

        enemy = "b" if self.white_to_move else "w"

        for d in directions:

            for i in range(1,8):

                end_row = r + d[0]*i
                end_col = c + d[1]*i

                if 0 <= end_row < 8 and 0 <= end_col < 8:

                    end_piece = self.board[end_row][end_col]

                    if end_piece == "--":

                        moves.append(Move((r,c),(end_row,end_col),self.board))

                    elif end_piece[0] == enemy:

                        moves.append(Move((r,c),(end_row,end_col),self.board))
                        break

                    else:
                        break

                else:
                    break


# -----------------------------
# KNIGHT MOVES
# -----------------------------
    def get_knight_moves(self, r, c, moves):

        knight_moves = [
            (-2,-1),(-2,1),
            (-1,-2),(-1,2),
            (1,-2),(1,2),
            (2,-1),(2,1)
        ]

        ally = "w" if self.white_to_move else "b"

        for m in knight_moves:

            end_row = r + m[0]
            end_col = c + m[1]

            if 0 <= end_row < 8 and 0 <= end_col < 8:

                end_piece = self.board[end_row][end_col]

                if end_piece == "--" or end_piece[0] != ally:

                    moves.append(Move((r,c),(end_row,end_col),self.board))


# -----------------------------
# BISHOP MOVES
# -----------------------------
    def get_bishop_moves(self, r, c, moves):

        directions = [(-1,-1),(-1,1),(1,-1),(1,1)]

        enemy = "b" if self.white_to_move else "w"

        for d in directions:

            for i in range(1,8):

                end_row = r + d[0]*i
                end_col = c + d[1]*i

                if 0 <= end_row < 8 and 0 <= end_col < 8:

                    end_piece = self.board[end_row][end_col]

                    if end_piece == "--":

                        moves.append(Move((r,c),(end_row,end_col),self.board))

                    elif end_piece[0] == enemy:

                        moves.append(Move((r,c),(end_row,end_col),self.board))
                        break

                    else:
                        break

                else:
                    break


# -----------------------------
# QUEEN MOVES
# -----------------------------
    def get_queen_moves(self, r, c, moves):

        self.get_rook_moves(r,c,moves)
        self.get_bishop_moves(r,c,moves)


# -----------------------------
# KING MOVES
# -----------------------------
    def get_king_moves(self, r, c, moves):

        king_moves = [
            (-1,-1),(-1,0),(-1,1),
            (0,-1),(0,1),
            (1,-1),(1,0),(1,1)
        ]

        ally = "w" if self.white_to_move else "b"

        for m in king_moves:

            end_row = r + m[0]
            end_col = c + m[1]

            if 0 <= end_row < 8 and 0 <= end_col < 8:

                end_piece = self.board[end_row][end_col]

                if end_piece == "--" or end_piece[0] != ally:

                    moves.append(Move((r,c),(end_row,end_col),self.board))