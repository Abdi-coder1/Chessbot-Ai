import pygame
import ChessGame
pygame.init()
def main(amount):
    """
    The main function is responsible for starting the game,
    it accomplishes this by installing the Chessgame packade and chess engine class.
    It flips between play mode and menu mode.
    :param amount, how many times should the game be played?
    """
    for i in range(amount):
        # Create the chess engine with the player types defined, and other attributes
        chess_engine = ChessGame.ChessEngine('human', 'human')
        game_state = {'run':True, 'history':False, 'winning': False, 'Amount':3} # the diffrent states of the game

        while True:
            current_events = chess_engine.observe_events()
            chess_engine.quit_game(current_events)
            if game_state['run']: # Play game
                chess_engine.run_game(current_events)
                game_state['winning'],game_state['run']= chess_engine.check_winner()
            elif not game_state['run'] and not game_state['history']: # Endgame
                game_state['run'],game_state['history'] =\
                    chess_engine.run_game_over(game_state['winning'],current_events)
                if game_state['run'] and not game_state['history']:
                    break
            else: # Show history
                game_state['history'] = chess_engine.show_history(current_events)

            pygame.display.flip()
            chess_engine.game_asset.clock.tick(chess_engine.game_asset.tick_rate)
main(2)
