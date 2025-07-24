import pygame
from ChessGame import GameHandler
import time
pygame.init()
def main():
    main_handler = GameHandler()
    run= True
    winning_color = None
    while True:
        current_events = main_handler.obsereve_events()
        main_handler.quit_game(current_events)
        if run:
            main_handler.draw_game()
            main_handler.play_game(current_events)
            run,winning_color = main_handler.end_game()
        else:
            run = main_handler.draw_game_over(winning_color,current_events)
            if run:
                main()
        pygame.display.flip()
        main_handler.main_game_asset.clock.tick(main_handler.main_game_asset.tick_rate)

print('running main')
time.sleep(3)
main()
print('done')