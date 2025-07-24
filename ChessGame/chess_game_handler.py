import pygame


from Config import Chessassets, Gameassets
from ChessGame.game_graphic import Gamegraphic
from ChessGame.game_mechanics import Gamemechanic
from sys import exit





class GameHandler:
    """
    This is the handler object of the chess game, it has the responsibility of
    connecting and guiding all the core chess functions, both  mechanic and graphic part. """

    def __init__(self):
        self.main_chess_asset = Chessassets()
        self.main_game_asset = Gameassets()
        self.main_game_graphic = Gamegraphic(self.main_chess_asset,self.main_game_asset)
        self.main_game_mechanic= Gamemechanic(self.main_chess_asset)

        self.main_chess_asset.black_options = self.main_game_mechanic.check_all_options(
            self.main_chess_asset.black_pieces,self.main_chess_asset.black_pieces_locations, 'black')
        self.main_chess_asset.white_options =  self.main_game_mechanic.check_all_options(
            self.main_chess_asset.white_pieces,self.main_chess_asset.white_pieces_locations,'white')

        self.check_state = self.main_game_mechanic.check_state
        self.pawn_promotion_state = [False, None, None]   # bool, index, color
        self.castling_state = [['white', False, False], ['black', False, False]] # color queen side, king_side
       # print('Då',id(self.main_game_asset))

    def draw_game(self):
        self.main_game_graphic.draw_screen()
        self.main_game_graphic.draw_board()
        self.main_game_graphic.draw_pieces()
        self.main_game_graphic.draw_valid_move()
        if self.pawn_promotion_state[0]:
            self.main_game_graphic.draw_pawn_promotion(self.pawn_promotion_state,self.pawn_promotion_state[2])
        else:
            self.main_game_graphic.draw_captured_pieces()
        self.main_game_graphic.draw_check(self.check_state)
        #print(self.main_chess_asset.selected_piece_index)

        if self.main_chess_asset.selected_piece_index is not None:
            if  self.main_chess_asset.turn_step < 2 and \
                    self.main_chess_asset.white_pieces[self.main_chess_asset.selected_piece_index] == 'king' \
                and (self.castling_state[0][1] or self.castling_state[0][2]):
                self.main_game_graphic.draw_castling(self.main_chess_asset.selected_piece_index,
                                                     self.castling_state[0])
            if self.main_chess_asset.turn_step>=2 and \
                    self.main_chess_asset.black_pieces[self.main_chess_asset.selected_piece_index] == 'king' \
                    and (self.castling_state[1][1] or self.castling_state[1][2]):
                self.main_game_graphic.draw_castling(self.main_chess_asset.selected_piece_index,
                                                     self.castling_state[1])

    def play_game(self,current_events):

        click_state = self.main_game_mechanic.click(current_events,self.main_game_mechanic.click_type[0])

        if click_state is not None and not self.pawn_promotion_state[0]:



            self.main_game_mechanic.piece_selection(click_state)
            self.main_game_mechanic.piece_movement(click_state)
            self.check_state = self.main_game_mechanic.check_state

            # print('cheking white,')
            # print('the current pieces are,   ',self.main_chess_asset.white_pieces)
            # print('And theri location ist,   ',self.main_chess_asset.white_pieces_locations)
            # print('with the current attacks being,  ',self.main_chess_asset.white_options)
            # print('and the ones captured from black are,  ', self.main_chess_asset.captured_pieces_white)
            # print('its history is,  ',self.main_chess_asset.white_history)
            # print()
            # print()
            # print('cheking black,')
            # print('the current pieces are,   ', self.main_chess_asset.black_pieces)
            # print('And theri location ist,   ', self.main_chess_asset.black_pieces_locations)
            # print('with the current attacks being,  ', self.main_chess_asset.black_options)
            # print('and the ones captured from white are,  ', self.main_chess_asset.captured_pieces_black)
            # print('its history is,  ', self.main_chess_asset.black_history)
            if self.main_game_mechanic.pawn_promotion_white[0]:
                self.pawn_promotion_state = [True, self.main_game_mechanic.pawn_promotion_white[1], 'white']
            elif self.main_game_mechanic.pawn_promotion_black[0]:
                self.pawn_promotion_state = [True,self.main_game_mechanic.pawn_promotion_black[1],'black']
            self.castling_state[0] = ['white']+ self.main_game_mechanic.castling_white
            self.castling_state[1] = ['black']+  self.main_game_mechanic.castling_black

        elif self.pawn_promotion_state[0]:
            return_value = self.main_game_mechanic.click(current_events, self.main_game_mechanic.click_type[1])

            if type(return_value) == list and return_value[0] == False: # Time for a pawn promtion
               # print('promotion time!, )

                chosen_piece_promotion = self.main_chess_asset.pieces_list_image[return_value[1]] # wichs piece to upgarde to?

                if self.pawn_promotion_state[2] == 'white': # chnage pieces
                    self.main_chess_asset.white_pieces[self.pawn_promotion_state[1]] = chosen_piece_promotion
                else: # change pieces
                    self.main_chess_asset.black_pieces[self.pawn_promotion_state[1]] = chosen_piece_promotion

                # now lets uptade options
                self.main_chess_asset.white_options = self.main_game_mechanic.check_all_options(
                        self.main_chess_asset.white_pieces, self.main_chess_asset.white_pieces_locations, 'white')
                self.main_chess_asset.black_options = self.main_game_mechanic.check_all_options(
                        self.main_chess_asset.black_pieces, self.main_chess_asset.black_pieces_locations, 'black')

                self.main_game_mechanic.temp_king_check('black')
                fixed_black_attack__list = self.main_chess_asset.black_options
                self.main_game_mechanic.temp_king_check('white')
                self.main_chess_asset.black_options = fixed_black_attack__list


               # now se if there is a check mate
                self.main_game_mechanic.check_state[1] = ['black_king'] + self.main_game_mechanic.check_mate('black')
                self.main_game_mechanic.check_state[0] = ['white_king'] + self.main_game_mechanic.check_mate('white')
                self.check_state = self.main_game_mechanic.check_state

                # reset the promoiton dependet variables
                self.pawn_promotion_state = [False, None, None]  # bool, index, color
                self.main_game_mechanic.pawn_promotion_white = [False, None]
                self.main_game_mechanic.pawn_promotion_black = [False, None]

            # print('cheking white,')
            # print('the current pieces are,   ', self.main_chess_asset.white_pieces)
            # print('And theri location ist,   ', self.main_chess_asset.white_pieces_locations)
            # print('with the current attacks being,  ', self.main_chess_asset.white_options)
            # print('and the ones captured from black are,  ', self.main_chess_asset.captured_pieces_white)
            # print('its history is,  ', self.main_chess_asset.white_history)
            # print()
            # print()
            # print('cheking black,')
            # print('the current pieces are,   ', self.main_chess_asset.black_pieces)
            # print('And theri location ist,   ', self.main_chess_asset.black_pieces_locations)
            # print('with the current attacks being,  ', self.main_chess_asset.black_options)
            # print('and the ones captured from white are,  ', self.main_chess_asset.captured_pieces_black)
            # print('its history is,  ', self.main_chess_asset.black_history)





               # print('promotion time!', chosen_piece_promotion )







        #print(self.main_game_mechanic.check_pawn([3,4],'white'))

    def obsereve_events(self):
        current_events = pygame.event.get()
        return current_events

    def quit_game(self,current_events):
      for event in current_events:
          if event.type == pygame.QUIT:
                exit()

    def end_game(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or self.check_state[0][2]:
            return False, 'black'
        elif self.check_state[1][2]:
            return False,'white'
        else:
            return True,None

    def draw_game_over(self, winn_color, current_events):
        mouse_pos = pygame.mouse.get_pos()
        click = False
        for event in current_events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
        start_over_bool = self.main_game_graphic.draw_game_over(winn_color,click,mouse_pos)
        return start_over_bool


