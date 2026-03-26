import pygame
from config import ROWS, COLS, SQUARE_SIZE, WHITE, PINK
from ai.evaluation import evaluate_board

IMAGES = {}


# -----------------------------
# LOAD CHESS PIECE IMAGES
# -----------------------------
def load_images():

    pieces = [
        "wP","wR","wN","wB","wQ","wK",
        "bP","bR","bN","bB","bQ","bK"
    ]

    for piece in pieces:

        path = f"assets/pieces/{piece}.png"

        image = pygame.image.load(path)

        IMAGES[piece] = pygame.transform.scale(
            image,
            (SQUARE_SIZE, SQUARE_SIZE)
        )


# -----------------------------
# DRAW CHESS BOARD
# -----------------------------
def draw_board(screen):

    for row in range(ROWS):
        for col in range(COLS):

            color = WHITE if (row + col) % 2 == 0 else PINK

            pygame.draw.rect(
                screen,
                color,
                (
                    col * SQUARE_SIZE,
                    row * SQUARE_SIZE,
                    SQUARE_SIZE,
                    SQUARE_SIZE
                )
            )


# -----------------------------
# DRAW PIECES
# -----------------------------
def draw_pieces(screen, board):

    for row in range(ROWS):
        for col in range(COLS):

            piece = board[row][col]

            if piece != "--":

                screen.blit(
                    IMAGES[piece],
                    (
                        col * SQUARE_SIZE,
                        row * SQUARE_SIZE
                    )
                )


# -----------------------------
# HIGHLIGHT SELECTED PIECE
# AND LEGAL MOVES
# -----------------------------
def highlight_squares(screen, gs, valid_moves, selected_square):

    if selected_square != ():

        r, c = selected_square

        # highlight selected square
        s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
        s.set_alpha(100)
        s.fill((0, 255, 0))

        screen.blit(
            s,
            (c * SQUARE_SIZE, r * SQUARE_SIZE)
        )

        # highlight legal moves
        s.fill((255, 255, 0))

        for move in valid_moves:

            if move.start_row == r and move.start_col == c:

                screen.blit(
                    s,
                    (
                        move.end_col * SQUARE_SIZE,
                        move.end_row * SQUARE_SIZE
                    )
                )


# -----------------------------
# DRAW GAME STATE
# -----------------------------
def draw_game_state(screen, gs, valid_moves, selected_square):

    draw_board(screen)

    highlight_squares(
        screen,
        gs,
        valid_moves,
        selected_square
    )

    draw_pieces(
        screen,
        gs.board
    )


# -----------------------------
# SCORE PANEL
# -----------------------------
def draw_score(screen, board):

    # draw side panel background
    pygame.draw.rect(
        screen,
        (230, 230, 230),
        (640, 0, 160, 640)
    )

    font = pygame.font.SysFont("Arial", 24)

    score = evaluate_board(board)

    if score > 0:
        text = f"White Advantage +{score}"

    elif score < 0:
        text = f"Black Advantage {score}"

    else:
        text = "Equal Position"

    text_surface = font.render(
        text,
        True,
        (0, 0, 0)
    )

    screen.blit(
        text_surface,
        (650, 50)
    )


# -----------------------------
# GAME RESULT TEXT
# -----------------------------
def draw_game_result(screen, text):

    font = pygame.font.SysFont("Arial", 48)

    text_surface = font.render(
        text,
        True,
        (0, 0, 0)
    )

    screen.blit(
        text_surface,
        (200, 300)
    )