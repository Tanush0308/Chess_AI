import pygame

from config import WIDTH, HEIGHT, SQUARE_SIZE
from gui.renderer import draw_game_state, load_images, draw_score, draw_game_result
from engine.game_state import GameState
from engine.move import Move
from ai.ai_move_finder import find_best_move


def main():

    pygame.init()

    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption("Chess AI")

    clock = pygame.time.Clock()

    gs = GameState()
    valid_moves = gs.get_valid_moves()

    load_images()

    selected_square = ()
    player_clicks = []

    running = True
    move_made = False

    while running:

        if not gs.white_to_move and not move_made:

            ai_move = find_best_move(gs,3)

            if ai_move:
                gs.make_move(ai_move)

            move_made=True


        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running=False

            elif event.type == pygame.MOUSEBUTTONDOWN and gs.white_to_move:

                location = pygame.mouse.get_pos()

                col = location[0] // SQUARE_SIZE
                row = location[1] // SQUARE_SIZE

                if col >=8 or row>=8:
                    continue

                selected_square=(row,col)
                player_clicks.append(selected_square)

                if len(player_clicks)==2:

                    move = Move(player_clicks[0],player_clicks[1],gs.board)

                    for valid_move in valid_moves:

                        if move.start_row==valid_move.start_row and \
                           move.start_col==valid_move.start_col and \
                           move.end_row==valid_move.end_row and \
                           move.end_col==valid_move.end_col:

                            gs.make_move(valid_move)
                            move_made=True
                            break

                    player_clicks=[]
                    selected_square=()

        if move_made:

            valid_moves = gs.get_valid_moves()
            move_made=False

        draw_game_state(screen,gs,valid_moves,selected_square)
        draw_score(screen,gs.board)

        if gs.checkmate:

            if gs.white_to_move:
                draw_game_result(screen,"Black Wins by Checkmate")
            else:
                draw_game_result(screen,"White Wins by Checkmate")

        elif gs.stalemate:
            draw_game_result(screen,"Stalemate")

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()


if __name__=="__main__":
    main()