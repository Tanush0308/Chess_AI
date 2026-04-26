import pygame

from config import WIDTH, HEIGHT, SQUARE_SIZE
from gui.renderer import (
    draw_game_state,
    load_images,
    draw_score,
    draw_captured_pieces,
    draw_game_result
)

from engine.game_state import GameState
from engine.move import Move
from ai.ai_move_finder import find_best_move


def main():

    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess AI")

    clock = pygame.time.Clock()

    gs = GameState()
    load_images()

    valid_moves = gs.get_valid_moves()

    selected_square = ()
    player_clicks = []

    move_made = False
    running = True

    while running:

        # -----------------------------
        # AI TURN
        # -----------------------------
        if not gs.white_to_move and not move_made:

            ai_move = find_best_move(gs, 3)

            if ai_move is None:
                valid_moves = gs.get_valid_moves()
                if valid_moves:
                    ai_move = valid_moves[0]

            if ai_move:
                gs.make_move(ai_move)
                move_made = True

        # -----------------------------
        # EVENTS
        # -----------------------------
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            # -----------------------------
            # MOUSE CLICK (PLAYER MOVE)
            # -----------------------------
            elif event.type == pygame.MOUSEBUTTONDOWN:

                if gs.white_to_move:

                    location = pygame.mouse.get_pos()
                    col = location[0] // SQUARE_SIZE
                    row = location[1] // SQUARE_SIZE

                    square = (row, col)

                    if selected_square == square:
                        selected_square = ()
                        player_clicks = []

                    else:
                        selected_square = square
                        player_clicks.append(square)

                    if len(player_clicks) == 2:

                        move = Move(player_clicks[0], player_clicks[1], gs.board)

                        for valid_move in valid_moves:

                            if (
                                move.start_row == valid_move.start_row and
                                move.start_col == valid_move.start_col and
                                move.end_row == valid_move.end_row and
                                move.end_col == valid_move.end_col
                            ):
                                gs.make_move(valid_move)
                                move_made = True
                                break

                        selected_square = ()
                        player_clicks = []

            # -----------------------------
            # KEYBOARD (UNDO)
            # -----------------------------
            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_z:
                    gs.undo_move()
                    move_made = True

        # -----------------------------
        # UPDATE GAME STATE
        # -----------------------------
        if move_made:
            valid_moves = gs.get_valid_moves()
            move_made = False

        # -----------------------------
        # DRAW
        # -----------------------------
        draw_game_state(screen, gs, valid_moves, selected_square)
        draw_score(screen, gs)
        draw_captured_pieces(screen, gs)

        if gs.checkmate:
            text = "Black wins by checkmate" if gs.white_to_move else "White wins by checkmate"
            draw_game_result(screen, text)

        elif gs.stalemate:
            draw_game_result(screen, "Stalemate")

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()