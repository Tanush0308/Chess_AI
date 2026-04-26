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

        self.white_king_location = (7,4)
        self.black_king_location = (0,4)

        # castling rights
        self.white_castle_kingside = True
        self.white_castle_queenside = True
        self.black_castle_kingside = True
        self.black_castle_queenside = True

        self.move_functions = {
            "P": self.get_pawn_moves,
            "R": self.get_rook_moves,
            "N": self.get_knight_moves,
            "B": self.get_bishop_moves,
            "Q": self.get_queen_moves,
            "K": self.get_king_moves
        }


    def make_move(self, move):

        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved

        self.move_log.append(move)

        # pawn promotion
        if move.is_pawn_promotion:
            if move.piece_moved[0] == "w":
                self.board[move.end_row][move.end_col] = "wQ"
            else:
                self.board[move.end_row][move.end_col] = "bQ"

        # king move
        if move.piece_moved == "wK":
            self.white_king_location = (move.end_row, move.end_col)
            self.white_castle_kingside = False
            self.white_castle_queenside = False

        elif move.piece_moved == "bK":
            self.black_king_location = (move.end_row, move.end_col)
            self.black_castle_kingside = False
            self.black_castle_queenside = False

        # rook move → update castling rights
        if move.piece_moved == "wR":
            if move.start_col == 0:
                self.white_castle_queenside = False
            elif move.start_col == 7:
                self.white_castle_kingside = False

        if move.piece_moved == "bR":
            if move.start_col == 0:
                self.black_castle_queenside = False
            elif move.start_col == 7:
                self.black_castle_kingside = False

        # castling move
        if move.piece_moved[1] == "K" and abs(move.start_col - move.end_col) == 2:

            if move.end_col == 6:  # kingside
                self.board[move.end_row][5] = self.board[move.end_row][7]
                self.board[move.end_row][7] = "--"

            elif move.end_col == 2:  # queenside
                self.board[move.end_row][3] = self.board[move.end_row][0]
                self.board[move.end_row][0] = "--"

        self.white_to_move = not self.white_to_move


    def undo_move(self):

        if len(self.move_log) != 0:

            move = self.move_log.pop()

            # undo promotion
            if move.is_pawn_promotion:
                self.board[move.start_row][move.start_col] = move.piece_moved
                self.board[move.end_row][move.end_col] = move.piece_captured
                self.white_to_move = not self.white_to_move
                return

            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured

            # undo king position
            if move.piece_moved == "wK":
                self.white_king_location = (move.start_row, move.start_col)

            elif move.piece_moved == "bK":
                self.black_king_location = (move.start_row, move.start_col)

            # undo castling rook move
            if move.piece_moved[1] == "K" and abs(move.start_col - move.end_col) == 2:

                if move.end_col == 6:
                    self.board[move.end_row][7] = self.board[move.end_row][5]
                    self.board[move.end_row][5] = "--"

                elif move.end_col == 2:
                    self.board[move.end_row][0] = self.board[move.end_row][3]
                    self.board[move.end_row][3] = "--"

            self.white_to_move = not self.white_to_move


    def get_all_possible_moves(self):

        moves = []

        for r in range(8):
            for c in range(8):

                piece = self.board[r][c]

                if piece == "--":
                    continue

                if (piece[0] == "w" and self.white_to_move) or \
                   (piece[0] == "b" and not self.white_to_move):

                    if piece[1] == "K":
                        self.get_king_moves(r, c, moves, include_castling=True)
                    else:
                        self.move_functions[piece[1]](r, c, moves)

        return moves


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


    def in_check(self):

        if self.white_to_move:
            return self.square_under_attack(*self.white_king_location)
        else:
            return self.square_under_attack(*self.black_king_location)


    def square_under_attack(self, r, c):

        self.white_to_move = not self.white_to_move

        opponent_moves = []

        for row in range(8):
            for col in range(8):

                piece = self.board[row][col]

                if piece == "--":
                    continue

                if (piece[0] == "w" and self.white_to_move) or \
                (piece[0] == "b" and not self.white_to_move):

                    # ❗ IMPORTANT: disable castling here
                    if piece[1] == "K":
                        self.get_king_moves(row, col, opponent_moves, include_castling=False)
                    else:
                        self.move_functions[piece[1]](row, col, opponent_moves)

        self.white_to_move = not self.white_to_move

        for move in opponent_moves:
            if move.end_row == r and move.end_col == c:
                return True

        return False


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


    def get_knight_moves(self, r, c, moves):

        knight_moves = [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]
        ally = "w" if self.white_to_move else "b"

        for m in knight_moves:

            end_row = r + m[0]
            end_col = c + m[1]

            if 0 <= end_row < 8 and 0 <= end_col < 8:

                end_piece = self.board[end_row][end_col]

                if end_piece == "--" or end_piece[0] != ally:
                    moves.append(Move((r,c),(end_row,end_col),self.board))


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


    def get_queen_moves(self, r, c, moves):
        self.get_rook_moves(r,c,moves)
        self.get_bishop_moves(r,c,moves)


    def get_king_moves(self, r, c, moves, include_castling=True):

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
                    moves.append(Move((r, c), (end_row, end_col), self.board))

        # ✅ CRITICAL FIX: only include castling when allowed
        if include_castling:
            self.get_castling_moves(r, c, moves)


    def get_castling_moves(self, r, c, moves):

        if self.in_check():
            return

        if self.white_to_move:

            if self.white_castle_kingside:
                if self.board[r][5] == "--" and self.board[r][6] == "--":
                    if not self.square_under_attack(r,5) and not self.square_under_attack(r,6):
                        moves.append(Move((r,c),(r,6),self.board))

            if self.white_castle_queenside:
                if self.board[r][1] == "--" and self.board[r][2] == "--" and self.board[r][3] == "--":
                    if not self.square_under_attack(r,2) and not self.square_under_attack(r,3):
                        moves.append(Move((r,c),(r,2),self.board))

        else:

            if self.black_castle_kingside:
                if self.board[r][5] == "--" and self.board[r][6] == "--":
                    if not self.square_under_attack(r,5) and not self.square_under_attack(r,6):
                        moves.append(Move((r,c),(r,6),self.board))

            if self.black_castle_queenside:
                if self.board[r][1] == "--" and self.board[r][2] == "--" and self.board[r][3] == "--":
                    if not self.square_under_attack(r,2) and not self.square_under_attack(r,3):
                        moves.append(Move((r,c),(r,2),self.board))