import pygame
import copy

class Gamemechanic:
    """
    An object that contains the core gameplay logic and has the capability of executing the game
    """
    def __init__(self,main_chess_asset):
        self.main_chess_asset = main_chess_asset
        self.click_type = ['piece', 'promotion', 'castling']   # what type of click is it?
        self.check_state = [['white_king', False, False], ['black_king', False, False]]
        self.valid_check_moves_white = copy.deepcopy(self.main_chess_asset.white_options)
        self.valid_check_moves_black = copy.deepcopy(self.main_chess_asset.black_options)
        self.anpassat_white = [False, [], None, [] ]   # Bool, attack, enabled, attack_move
        self.anpassat_black = [False, [], None, [] ]   # Bool, attack, enabled, attack_move
        self.pawn_promotion_white = [False, None]      # promotion_time ? index
        self.pawn_promotion_black = [False, None]       # promotion_time ? index

        self.castling_white = [False, False]  # Castling queen side, castling king side
        self.castling_black = [False, False]  # queen sid,e king side.

    def click(self,current_events,click_type):
        """
        This function observes the game state and
        preserves the coordinates of where is being clicked
        :parameter : click_type:
        :return
        """
        for event in current_events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if click_type == 'piece':
                    coordinates = [event.pos[0], event.pos[1]]
                    if all(c < self.main_chess_asset.square_dimension * 8 for c in coordinates):  # inside the board?
                        grid_coordinates =  [coordinates[0] // self.main_chess_asset.square_dimension,
                                 coordinates[1] // self.main_chess_asset.square_dimension]
                        return grid_coordinates
                if click_type == 'promotion':
                    pawn_promotion_bool = True
                    pawn_promotion_index = None
                    pawn_promotion_list = [pawn_promotion_bool,pawn_promotion_index]
                    pieces_rect_list = [pygame.Rect(self.main_chess_asset.square_dimension * 8 + i % 3 * 80,
                                                    i // 3 * 80 + 250,  67,67)
                                        for i in range(1, len(self.main_chess_asset.pieces_list_image))]
                    mouse_pos = pygame.mouse.get_pos()
                    for i in range(len(pieces_rect_list)):
                        if pieces_rect_list[i].collidepoint(mouse_pos):
                            pawn_promotion_list[0] = False
                            pawn_promotion_list[1]= i + 1 # To counter act the deletion of the pawn and king!
                    return pawn_promotion_list


        return None

    def piece_selection(self,grid_click_state):
        """

        :param grid_click_state:
        :return:
        """

        if (grid_click_state in self.main_chess_asset.white_pieces_locations and
                self.main_chess_asset.turn_step <2):
            piece_index = self.main_chess_asset.white_pieces_locations.index(grid_click_state)
            self.main_chess_asset.selected_piece_index = piece_index
            self.main_chess_asset.turn_step = 1
            self.check_valid_move()


        elif (grid_click_state in self.main_chess_asset.black_pieces_locations
              and self.main_chess_asset.turn_step >= 2):
            piece_index = self.main_chess_asset.black_pieces_locations.index(grid_click_state)
            self.main_chess_asset.selected_piece_index = piece_index
            self.main_chess_asset.turn_step = 3
            self.check_valid_move()

    def piece_capture(self,color,new_position ):
        '''
        A function that cheks wether a piece has been captured, by looking at the position list?
        '''
        white_locations = [state for states in self.main_chess_asset.white_options for state in states]
        black_locations = [state for states in self.main_chess_asset.black_options for state in states]

        if color == 'white':
            for i in range(len(self.main_chess_asset.black_pieces_locations)):
                if new_position == self.main_chess_asset.black_pieces_locations[i]:
                    captured_black_piece = self.main_chess_asset.black_pieces[i]
                    #print('hew, captured black piece!', len(self.main_chess_asset.black_history))
                    self.main_chess_asset.black_pieces.pop(i)
                    self.main_chess_asset.black_pieces_locations.pop(i)
                    self.main_chess_asset.white_history_captured.append(self.main_chess_asset.black_history[i])
                    self.main_chess_asset.black_history.pop(i)

                    self.main_chess_asset.captured_pieces_white.append(captured_black_piece)
                   # print('hew, captured black piece!', len(self.main_chess_asset.black_history))
                    break

            # capturing also includes enpassant
            if self.anpassat_white[0]: # white had the oppurtunity to move, but did it?
                pieced_moved_index = self.main_chess_asset.white_pieces_locations.index(new_position)

                if pieced_moved_index in self.anpassat_white[1] and new_position in self.anpassat_white[3]:
                    captured_place = [new_position[0] , new_position[1] + 1]
                    captured_black_piece_index = self.main_chess_asset.black_pieces_locations.index(captured_place)
                    self.main_chess_asset.captured_pieces_white.append(
                        self.main_chess_asset.black_pieces[captured_black_piece_index])
                    self.main_chess_asset.black_pieces.pop(captured_black_piece_index)
                    self.main_chess_asset.black_pieces_locations.pop(captured_black_piece_index)




        elif color == 'black':  # It was white that made the move.
            for i in range(len(self.main_chess_asset.white_pieces_locations)):
                #print('cheking',i)
                if new_position == self.main_chess_asset.white_pieces_locations[i]:  # This piece has been captured
                    captured_white_piece = self.main_chess_asset.white_pieces[i]
                    self.main_chess_asset.white_pieces.pop(i)
                    self.main_chess_asset.white_pieces_locations.pop(i)
                    self.main_chess_asset.captured_pieces_black.append(captured_white_piece)
                    self.main_chess_asset.black_history_captured.append(self.main_chess_asset.white_history[i])
                    self.main_chess_asset.white_history.pop(i)
                    break
            if self.anpassat_black[0]:  # black had the oppurtunity to move, but did it?
                pieced_moved_index = self.main_chess_asset.black_pieces_locations.index(new_position)
                if pieced_moved_index in self.anpassat_black[1] and new_position in self.anpassat_black[3]:
                    captured_place = [new_position[0], new_position[1] - 1]
                    captured_white_piece_index = self.main_chess_asset.white_pieces_locations.index(captured_place)
                    self.main_chess_asset.captured_pieces_black.append(
                        self.main_chess_asset.white_pieces[captured_white_piece_index])
                    self.main_chess_asset.white_pieces.pop(captured_white_piece_index)
                    self.main_chess_asset.white_pieces_locations.pop(captured_white_piece_index)

    def piece_movement(self,grid_click_state):
        """

        :param grid_click_state:
        :return:
        """
        if self.main_chess_asset.turn_step % 2 ==1 : # Piece has been selected
            castling_valid_move = []
            if self.main_chess_asset.turn_step == 1 and \
                    self.main_chess_asset.white_pieces[self.main_chess_asset.selected_piece_index] == 'king' :
                if self.castling_white[0]:
                    castling_valid_move.append([2,7])
                if self.castling_white[1]:
                    castling_valid_move.append([6,7])
            elif self.main_chess_asset.turn_step == 3 and \
                    self.main_chess_asset.black_pieces[self.main_chess_asset.selected_piece_index] == 'king':
                if self.castling_black[0]:
                    castling_valid_move.append([2, 0])
                if self.castling_black[1]:
                    castling_valid_move.append([6, 0])

            if grid_click_state in self.main_chess_asset.valid_moves: #  The player has selected a space valid for that move
                if self.main_chess_asset.turn_step == 1: # white turns

                    # Before the white piece moves, does it enable anpassat for black?
                    self.anpassat_black[0], self.anpassat_black[1], self.anpassat_black[2], self.anpassat_black[3] = self.anpassat(grid_click_state,
                                                                self.main_chess_asset.white_pieces_locations[
                                                                 self.main_chess_asset.selected_piece_index],
                                                                self.main_chess_asset.selected_piece_index, 'white')


                    # now the piece will be moving and we record history
                    self.main_chess_asset.white_pieces_locations[
                        self.main_chess_asset.selected_piece_index] = grid_click_state
                    self.main_chess_asset.turn_step = 2
                    self.record_history('white', self.main_chess_asset.selected_piece_index, grid_click_state ) # some overlap?

                    # If the space is occupied by a black piece, then we will capture and mov ethe name of the black piece.
                    self.piece_capture('white', grid_click_state)

                    # Lets re consider our attacks now
                    self.main_chess_asset.black_options = self.check_all_options(self.main_chess_asset.black_pieces,
                                                                                 self.main_chess_asset.black_pieces_locations,
                                                                                 'black')
                    self.main_chess_asset.white_options = self.check_all_options(self.main_chess_asset.white_pieces,
                                                                                 self.main_chess_asset.white_pieces_locations,
                                                                               'white')
                    # Next turn is black, so we apply the king safty method on it
                    self.temp_king_check('black')



                    # to complemnt the attacks we need to check the special rules, pawn promotion, anpassant and castling.
                    self.pawn_promotion('white')
                    if self.anpassat_black[0]:
                        n = 0
                        for index in self.anpassat_black[1]:
                            self.main_chess_asset.black_options[index].append(self.anpassat_black[3][n])
                            n += 1

                    self.check_castling('white')
                    self.check_castling('black')
                    # print('white', self.castling_white)
                    # print('black', self.castling_black)
                    # print()

                    # Now lets check wether it is a check mate
                    self.check_state[1] = ['black_king'] + self.check_mate('black')
                    self.check_state[0] = ['white_king'] + self.check_mate('white')
                    self.main_chess_asset.selected_piece_index = None

                if self.main_chess_asset.turn_step == 3:
                    # Before the black piece moves, does it enbale anpassat for white?
                    self.anpassat_white[0], self.anpassat_white[1], self.anpassat_white[2], self.anpassat_white[3] = self.anpassat(grid_click_state,
                                                                                 self.main_chess_asset.black_pieces_locations[
                                                                                     self.main_chess_asset.selected_piece_index],
                                                                                 self.main_chess_asset.selected_piece_index,
                                                                                 'black')
                    # Now lets move the piece, change turn and record history.
                    self.main_chess_asset.black_pieces_locations[
                        self.main_chess_asset.selected_piece_index] = grid_click_state
                    self.main_chess_asset.turn_step = 0
                    self.record_history('black', self.main_chess_asset.selected_piece_index, grid_click_state)

                    # If the space is occupied by a white piece, then we will capture and mov ethe name of the white piece.
                    self.piece_capture('black', grid_click_state)

                    # With the pieces moved and captured, lets reconsider attacks.
                    self.main_chess_asset.black_options = self.check_all_options(self.main_chess_asset.black_pieces,
                                                                                 self.main_chess_asset.black_pieces_locations,
                                                                                 'black')
                    self.main_chess_asset.white_options = self.check_all_options(self.main_chess_asset.white_pieces,
                                                                                 self.main_chess_asset.white_pieces_locations,
                                                                               'white')
                    # next turn is white, so we apply the safty matric on it

                    self.temp_king_check('white')

                    # to complemnt the attacks we need to check the special rules, pawn promotion, anpassant and castling.
                    self.pawn_promotion('black')
                    if self.anpassat_white[0]:
                        n = 0
                        for index in self.anpassat_white[1]:
                            self.main_chess_asset.white_options[index].append(self.anpassat_white[3][n])
                            n += 1

                    self.check_castling('white')
                    self.check_castling('black')
                    # print('white', self.castling_white)
                    # print('black', self.castling_black)
                    # print()

                    # lets check chek_mate and revert the selected index.
                    self.check_state[0] = ['white_king'] + self.check_mate('white')
                    self.check_state[1] = ['black_king'] + self.check_mate('black')
                    self.main_chess_asset.selected_piece_index = None


            elif grid_click_state in castling_valid_move: # we have chosen a castling move!
                if self.main_chess_asset.turn_step == 1:

                    # lets first chnage posutions and record history
                    self.main_chess_asset.white_pieces_locations[self.main_chess_asset.selected_piece_index] = grid_click_state
                    self.record_history('white', self.main_chess_asset.selected_piece_index,
                                        grid_click_state)
                    if grid_click_state == [2,7]: # Change the position of the left rook
                        left_rook_index = self.main_chess_asset.white_pieces_locations.index([0,7])
                        self.main_chess_asset.white_pieces_locations[left_rook_index] = [3,7]
                        self.record_history('white', left_rook_index,
                                           [3,7])
                    elif grid_click_state == [6,7]: # Change the position of the right rook
                        right_rook_index = self.main_chess_asset.white_pieces_locations.index([7,7])
                        self.main_chess_asset.white_pieces_locations[right_rook_index] = [5,7]
                        self.record_history('white',right_rook_index,
                                            [5,7])  # some overlap?

                    # Now lets preform the important steps, attacks, turnstep, check_mate
                    self.main_chess_asset.turn_step = 2
                    self.main_chess_asset.black_options = self.check_all_options(self.main_chess_asset.black_pieces,
                                                                                 self.main_chess_asset.black_pieces_locations,
                                                                                 'black')
                    self.main_chess_asset.white_options = self.check_all_options(self.main_chess_asset.white_pieces,
                                                                                 self.main_chess_asset.white_pieces_locations,
                                                                                 'white')
                    self.temp_king_check('black')


                    self.check_state[1] = ['black_king'] + self.check_mate('black')
                    self.check_state[0] = ['white_king'] + self.check_mate('white')
                    self.main_chess_asset.selected_piece_index = None

                if self.main_chess_asset.turn_step == 3:
                    # lets first change positions and record history
                    self.main_chess_asset.black_pieces_locations[
                        self.main_chess_asset.selected_piece_index] = grid_click_state
                    self.record_history('black', self.main_chess_asset.selected_piece_index,
                                        grid_click_state)
                    if grid_click_state == [2, 0]:  # Change the position of the left rook
                        left_rook_index = self.main_chess_asset.black_pieces_locations.index([0, 0])
                        self.main_chess_asset.black_pieces_locations[left_rook_index] = [3, 0]
                        self.record_history('black', left_rook_index,
                                            [3, 0])
                    elif grid_click_state == [6, 7]:  # Change the position of the right rook
                        right_rook_index = self.main_chess_asset.black_pieces_locations.index([7, 0])
                        self.main_chess_asset.black_pieces_locations[right_rook_index] = [5, 0]
                        self.record_history('black', right_rook_index,
                                            [5, 0])  # some overlap?

                    # Now lets preform the important steps, attacks, turnstep, check_mate
                    self.main_chess_asset.turn_step = 0
                    self.main_chess_asset.black_options = self.check_all_options(self.main_chess_asset.black_pieces,
                                                                                 self.main_chess_asset.black_pieces_locations,
                                                                                 'black')
                    self.main_chess_asset.white_options = self.check_all_options(self.main_chess_asset.white_pieces,
                                                                                 self.main_chess_asset.white_pieces_locations,
                                                                                 'white')

                    self.temp_king_check('white')


                    self.check_state[1] = ['black_king'] + self.check_mate('black')
                    self.check_state[0] = ['white_king'] + self.check_mate('white')
                    self.main_chess_asset.selected_piece_index = None

    def check_all_options(self, pieces_list, pieces_location_list, player_turn):
        """
        Given a Board, and a player, what are the total squares that a player could move to?
        """
        piece_move_list = []
        all_piece_move_list = []

        for i in range(len(pieces_list)):
            active_location = pieces_location_list[i]
            active_piece = pieces_list[i]

            if active_piece == 'pawn':
                piece_move_list = self.check_pawn(active_location,player_turn)
            elif active_piece == 'rook':
                 piece_move_list = self.check_rook(active_location,player_turn)
            elif active_piece == 'knight':
                 piece_move_list = self.check_knight(active_location,player_turn)
            elif active_piece == 'bishop':
                 piece_move_list = self.check_bishop(active_location,player_turn)
            elif active_piece == 'queen':
                 piece_move_list = self.check_queen(active_location,player_turn)
            elif active_piece == 'king':
                 piece_move_list = self.check_king(active_location,player_turn)
            all_piece_move_list.append(piece_move_list)


        return all_piece_move_list

    def check_valid_move(self):
        """Baserat påa llla möjliga drag och den pjäs som har valts,
        vad är valid moves just nu ?"""
        if self.main_chess_asset.turn_step<2:
            self.main_chess_asset.valid_moves = self.main_chess_asset.white_options[
                self.main_chess_asset.selected_piece_index]

        elif self.main_chess_asset.turn_step >= 2:
            self.main_chess_asset.valid_moves = self.main_chess_asset.black_options[
                self.main_chess_asset.selected_piece_index
            ]

    def record_history(self, color, piece_index, new_position):
        """
       This functions record the history of the pieces moves
        """
        if color == 'white':
            self.main_chess_asset.white_history[piece_index].append(new_position)
            #print(self.main_chess_asset.white_history)
        elif color == 'black':
            self.main_chess_asset.black_history[piece_index].append(new_position)

    def check_castling(self,color):
        """
        Given the games current state, can a castling e performed?
        Cheks, all sides and pikes out the one relavnt
        :return:
        """
        castling_bool = {'left_rook_history': False,
                        'right_rook_history': False,
                        'king_history': False,
                        'left_safe': True,
                        'right_safe': True,
                        'left_free': True,
                        'right_free': True,
                         'kings_safe': False,
                         'left_rook_safe': False,
                         'right_rook_safe': False}
        # First lets fill the information
        if color == 'white':
            rook_indexes = [i for i in range(len(self.main_chess_asset.white_pieces)) \
                           if self.main_chess_asset.white_pieces[i] == 'rook']
            king_index = self.main_chess_asset.white_pieces.index('king')
            rook_pos_list = [self.main_chess_asset.white_pieces_locations[rook_index]
                             for rook_index in rook_indexes]
            king_pos = self.main_chess_asset.white_pieces_locations[king_index]
            black_attacks = [pos for item in self.main_chess_asset.black_options for pos in item]

            # First lets check history
            if len(self.main_chess_asset.white_history[king_index]) == 1 \
                and king_pos == [4,7]:
                castling_bool['king_history'] = True
            for i in range(len(rook_indexes)):
                if len(self.main_chess_asset.white_history[rook_indexes[i]]) == 1 \
                    and rook_pos_list[i] == [0,7]:
                    castling_bool['left_rook_history'] = True
                elif len(self.main_chess_asset.white_history[rook_indexes[i]]) == 1 \
                    and rook_pos_list[i] == [7,7]:
                    castling_bool['right_rook_history'] = True

            # now we check for vacancy and danger in the places between, left and right side
            for i in range(1,4): # Lefts side
                grid_pos = [i,7]
                if grid_pos in self.main_chess_asset.white_pieces_locations or \
                        grid_pos in self.main_chess_asset.black_pieces_locations:
                    temporary_bool_vacancy = False
                else:   temporary_bool_vacancy = True
                castling_bool['left_free'] = castling_bool['left_free'] and temporary_bool_vacancy

                #now we check safety
                if grid_pos in black_attacks:
                    temporary_bool_attack = False
                else:   temporary_bool_attack = True
                castling_bool['left_safe'] = castling_bool['left_safe'] and temporary_bool_attack
            for i in range(5,7): # right side
                grid_pos = [i,7]
                if grid_pos in self.main_chess_asset.white_pieces_locations or \
                        grid_pos in self.main_chess_asset.black_pieces_locations:
                    temporary_bool = False
                else:   temporary_bool = True
                castling_bool['right_free'] = castling_bool['right_free'] and temporary_bool

                # Now we check safety
                if grid_pos in black_attacks:
                    temporary_bool_attack = False
                else:
                    temporary_bool_attack = True
                castling_bool['right_safe'] = castling_bool['right_safe'] and temporary_bool_attack

            # Now we need to check the king and rooks safety
            if king_pos not in black_attacks:
                castling_bool['kings_safe'] = True
            for i in range(len(rook_pos_list)):
                if rook_pos_list[i] not in black_attacks and \
                       rook_pos_list[i] == [0,7]:
                    castling_bool['left_rook_safe'] = True
                elif rook_pos_list[i] not in black_attacks and \
                        rook_pos_list[i] == [7,7]:
                    castling_bool['right_rook_safe'] = True
        elif color == 'black':
            rook_indexes = [i for i in range(len(self.main_chess_asset.black_pieces)) \
                            if self.main_chess_asset.black_pieces[i] == 'rook']
            king_index = self.main_chess_asset.black_pieces.index('king')
            rook_pos_list = [self.main_chess_asset.black_pieces_locations[rook_index]
                             for rook_index in rook_indexes]
            king_pos = self.main_chess_asset.black_pieces_locations[king_index]
            white_attacks = [pos for item in self.main_chess_asset.white_options for pos in item]

            # First lets check history
            if len(self.main_chess_asset.black_history[king_index]) == 1 \
                    and king_pos == [4, 0]:
                castling_bool['king_history'] = True
            for i in range(len(rook_indexes)):
                if len(self.main_chess_asset.black_history[rook_indexes[i]]) == 1 \
                        and rook_pos_list[i] == [0, 0]:
                    castling_bool['left_rook_history'] = True
                elif len(self.main_chess_asset.black_history[rook_indexes[i]]) == 1 \
                        and rook_pos_list[i] == [7, 0]:
                    castling_bool['right_rook_history'] = True

            # now we check for vacancy and danger in the places between, left and right side
            for i in range(1, 4):  # Lefts side
                grid_pos = [i, 0]
                if grid_pos in self.main_chess_asset.white_pieces_locations or \
                        grid_pos in self.main_chess_asset.black_pieces_locations:
                    temporary_bool_vacancy = False
                else:
                    temporary_bool_vacancy = True
                castling_bool['left_free'] = castling_bool['left_free'] and temporary_bool_vacancy

                # now we check safety
                if grid_pos in white_attacks:
                    temporary_bool_attack = False
                else:
                    temporary_bool_attack = True
                castling_bool['left_safe'] = castling_bool['left_safe'] and temporary_bool_attack
            for i in range(5, 7):  # right side
                grid_pos = [i, 0]
                if grid_pos in self.main_chess_asset.white_pieces_locations or \
                        grid_pos in self.main_chess_asset.black_pieces_locations:
                    temporary_bool = False
                else:
                    temporary_bool = True
                castling_bool['right_free'] = castling_bool['right_free'] and temporary_bool

                # Now we check safety
                if grid_pos in white_attacks:
                    temporary_bool_attack = False
                else:
                    temporary_bool_attack = True
                castling_bool['right_safe'] = castling_bool['right_safe'] and temporary_bool_attack

            # Now we need to check the king and rooks safety
            if king_pos not in white_attacks:
                castling_bool['kings_safe'] = True
            for i in range(len(rook_pos_list)):
                if rook_pos_list[i] not in white_attacks and \
                        rook_pos_list[i] == [0, 0]:
                    castling_bool['left_rook_safe'] = True
                elif rook_pos_list[i] not in white_attacks and \
                        rook_pos_list[i] == [7, 0]:
                    castling_bool['right_rook_safe'] = True

        # Now when all of the information is filled, we look if castling is possible.
        if color == 'white':
            if castling_bool['left_rook_history'] and castling_bool['king_history'] \
                    and castling_bool['left_safe'] and castling_bool['left_free'] \
                    and castling_bool['left_rook_safe'] and castling_bool['kings_safe']:
                self.castling_white[0] = True
            else:   self.castling_white[0] = False

            if castling_bool['right_rook_history'] and castling_bool['king_history'] \
                    and castling_bool['right_safe'] and castling_bool['right_free'] \
                    and castling_bool['right_rook_safe'] and castling_bool['kings_safe']:
                self.castling_white[1] = True
            else:   self.castling_white[1] = False
        elif color == 'black':
            if castling_bool['left_rook_history'] and castling_bool['king_history'] \
                    and castling_bool['left_safe'] and castling_bool['left_free'] \
                    and castling_bool['left_rook_safe'] and castling_bool['kings_safe']:
                self.castling_black[0] = True
            else:
                self.castling_black[0] = False

            if castling_bool['right_rook_history'] and castling_bool['king_history'] \
                    and castling_bool['right_safe'] and castling_bool['right_free'] \
                    and castling_bool['right_rook_safe'] and castling_bool['kings_safe']:
                self.castling_black[1] = True
            else:
                self.castling_black[1] = False

    def check_pawn(self,position,color):
        specific_valid_moves = []

        if color == 'white':
            if [position[0], position[1] -1] not in self.main_chess_asset.white_pieces_locations and \
                ([position[0], position[1] -1]) not in self.main_chess_asset.black_pieces_locations \
                    and position [1] > 0:
                specific_valid_moves.append([position[0], position[1] - 1])

            if [position[0], position[1] - 2 ] not in self.main_chess_asset.black_pieces_locations + \
                    self.main_chess_asset.white_pieces_locations and \
                    [position[0], position[1] - 1] not in self.main_chess_asset.black_pieces_locations + \
                    self.main_chess_asset.white_pieces_locations and position[1] == 6:

                specific_valid_moves.append([position[0], position[1] - 2])
            if [position[0]+1, position[1]-1] in self.main_chess_asset.black_pieces_locations:
                specific_valid_moves.append([position[0]+1,position[1]-1])
            if [position[0]-1, position[1]-1] in self.main_chess_asset.black_pieces_locations:
                specific_valid_moves.append([position[0]-1,position[1]-1])

        else:
            if [position[0], position[1] +1] not in self.main_chess_asset.black_pieces_locations and \
                ([position[0], position[1] +1]) not in self.main_chess_asset.white_pieces_locations \
                    and position [1] < 7:
                specific_valid_moves.append([position[0], position[1] + 1])

            if [position[0], position[1] + 2] not in self.main_chess_asset.black_pieces_locations + \
                self.main_chess_asset.white_pieces_locations and \
                    [position[0], position[1] + 1] not in self.main_chess_asset.black_pieces_locations + \
                    self.main_chess_asset.white_pieces_locations and position[1] == 1:
                       # it is in start positions
                specific_valid_moves.append([position[0], position[1] + 2])
            if [position[0]+1, position[1]+1] in self.main_chess_asset.white_pieces_locations:
                specific_valid_moves.append([position[0]+1,position[1]+1])
            if [position[0]-1, position[1]+1] in self.main_chess_asset.white_pieces_locations:
                specific_valid_moves.append([position[0]-1,position[1]+1])

        return specific_valid_moves

    def anpassat(self, new_pos, old_pos, chosen_index, color):
        """
        A function  that determens if the move that was just made is a en passant qualifying move for the oppponent
        :return:
        """

        anpassat_bool = False
        anpassat_piece_index = []
        anpassat_move = []
        if color == 'white' and self.main_chess_asset.white_pieces[chosen_index] == 'pawn':
            if old_pos[1] == 6 and new_pos == [old_pos[0], old_pos[1]-2]:
                for i in range(len(self.main_chess_asset.black_pieces)):
                    if self.main_chess_asset.black_pieces[i] == 'pawn' and (
                            self.main_chess_asset.black_pieces_locations[i] == [new_pos[0]-1, new_pos[1]] or
                            self.main_chess_asset.black_pieces_locations[i] == [new_pos[0]+1, new_pos[1]]):
                        if [new_pos[0], new_pos[1] + 1] not in self.main_chess_asset.white_pieces_locations and \
                            [new_pos[0], new_pos[1] + 1] not in self.main_chess_asset.black_pieces_locations:
                            anpassat_bool = True
                            anpassat_piece_index.append(i)
                            anpassat_move.append([new_pos[0], new_pos[1]+1])

        elif color == 'black' and self.main_chess_asset.black_pieces[chosen_index] == 'pawn':
            if old_pos[1] == 1 and new_pos == [old_pos[0], old_pos[1] + 2]:


                for i in range(len(self.main_chess_asset.white_pieces)):
                    if self.main_chess_asset.white_pieces[i] == 'pawn' and (
                            self.main_chess_asset.white_pieces_locations[i] == [new_pos[0]-1, new_pos[1]] or
                            self.main_chess_asset.white_pieces_locations[i] == [new_pos[0]+1, new_pos[1]]):
                            if [new_pos[0], new_pos[1] - 1] not in self.main_chess_asset.white_pieces_locations and \
                                    [new_pos[0], new_pos[1] - 1] not in self.main_chess_asset.black_pieces_locations:

                                anpassat_bool = True
                                anpassat_piece_index.append(i)
                                anpassat_move.append( [new_pos[0], new_pos[1] - 1] )

        return anpassat_bool,anpassat_piece_index,chosen_index, anpassat_move

    def pawn_promotion(self,color):
        """
        Considering the move that was just made by color, is promotion now avialble for that color?
        """


        if color == 'white':
            for i in range(len(self.main_chess_asset.white_pieces)):
                if self.main_chess_asset.white_pieces[i] == 'pawn' and \
                        self.main_chess_asset.white_pieces_locations[i][1] == 0:
                    self.pawn_promotion_white[0] = True
                    self.pawn_promotion_white[1] = i

        elif color == 'black':
            for i in range(len(self.main_chess_asset.black_pieces)):
                if self.main_chess_asset.black_pieces[i] == 'pawn' and \
                        self.main_chess_asset.black_pieces_locations[i][1] == 7:
                    self.pawn_promotion_black[0] = True
                    self.pawn_promotion_black[1] = i

    def check_rook(self,position,color):
        specific_moves_list = []

        if color == 'white':
            ally_list = self.main_chess_asset.white_pieces_locations
            enemy_list = self.main_chess_asset.black_pieces_locations
        else:
            ally_list = self.main_chess_asset.black_pieces_locations
            enemy_list = self.main_chess_asset.white_pieces_locations

        for i in range(0,4): # up, down, right, left
            if i == 0:    x_mod, y_mod = 0, -1
            elif i == 1:    x_mod,y_mod = 0, 1
            elif i == 2:    x_mod, y_mod = 1, 0
            elif i == 3:    x_mod, y_mod = -1, 0

            path = True # is the path still valid?
            chain_mod = 1 # how many squares of movement?

            while path:
                possible_new_pos = [position[0] + x_mod * chain_mod, position[1] + y_mod * chain_mod]

                if possible_new_pos not in ally_list and \
                      0 <= possible_new_pos[0] <= 7 and 0 <= possible_new_pos[1] <=7:  # square is valid
                    specific_moves_list.append(possible_new_pos)
                    chain_mod += 1
                    if possible_new_pos in enemy_list:
                        path = False
                else:
                    path = False
        return specific_moves_list

    def check_knight(self,position,color):
        specific_moves_list =[]
        if color == 'white':
            ally_list = self.main_chess_asset.white_pieces_locations
            enemy_list = self.main_chess_asset.black_pieces_locations
        else:
            ally_list = self.main_chess_asset.black_pieces_locations


        relative_pos = [[2,1],[2,-1],[-2,1],[-2,-1],[1,2],[-1,2],[1,-2],[-1,-2]]

        for pos_transformer in relative_pos:
            new_pos = [ position[0] + pos_transformer[0], position[1] + pos_transformer[1] ]
            if new_pos not in ally_list and 0<= new_pos[0] <=7 and 0<= new_pos[1] <=7: # empty and withing bounds
                specific_moves_list.append(new_pos)
        return specific_moves_list

    def check_bishop(self,position,color):
        specific_moves_list = []

        if color == 'white':
            ally_list = self.main_chess_asset.white_pieces_locations
            enemy_list = self.main_chess_asset.black_pieces_locations
        else:
            ally_list = self.main_chess_asset.black_pieces_locations
            enemy_list = self.main_chess_asset.white_pieces_locations

        for i in range(0, 4):  # up_left, up_right, down_left, down_right
            if i == 0:
                x_mod, y_mod = -1, -1
            elif i == 1:
                x_mod, y_mod = 1, -1
            elif i == 2:
                x_mod, y_mod = -1, 1
            elif i == 3:
                x_mod, y_mod = 1, 1

            path = True  # is the path still valid?
            chain_mod = 1  # how many squares of movement?

            while path:
                possible_new_pos = [position[0] + x_mod * chain_mod, position[1] + y_mod * chain_mod]

                if possible_new_pos not in ally_list and \
                        0 <= possible_new_pos[0] <= 7 and 0 <= possible_new_pos[1] <= 7:  # square is valid
                    specific_moves_list.append(possible_new_pos)
                    chain_mod += 1
                    if possible_new_pos in enemy_list:
                        path = False
                else:
                    path = False
        return specific_moves_list

    def check_queen(self, position, color):
        return self.check_bishop(position,color) + self.check_rook(position,color)

    def check_king(self,position,color):
        specific_moves_list = []
        if color == 'white':
            ally_list = self.main_chess_asset.white_pieces_locations
        else:
            ally_list = self.main_chess_asset.black_pieces_locations


        relative_pos = [[0, -1], [1, -1], [-1, -1], [1, 0], [-1, 0],[0, 1], [1, 1], [-1, 1]]

        for pos_transformer in relative_pos:
            new_pos = [position[0] + pos_transformer[0], position[1] + pos_transformer[1]]
            if new_pos not in ally_list and 0 <= new_pos[0] <= 7 and 0 <= new_pos[1] <= 7:  # empty and withing bounds
                specific_moves_list.append(new_pos)
        return specific_moves_list

    def undo_check(self,past_pos,piece_index, color, removed_bool):
        """
        A function that undoes a move and restores the board as it was before
        """

        if color == 'white':
            if removed_bool:
                # restoring the black piece, location , and history list. options gets done in anotehr spot.
                black_piece = self.main_chess_asset.captured_pieces_white[-1]
                self.main_chess_asset.black_pieces.append(black_piece)
                self.main_chess_asset.black_pieces_locations.append(
                    self.main_chess_asset.white_pieces_locations[piece_index])
                self.main_chess_asset.black_history.append(self.main_chess_asset.white_history_captured[-1])

                self.main_chess_asset.captured_pieces_white.pop(-1)
                self.main_chess_asset.white_history_captured.pop(-1)
            self.main_chess_asset.white_pieces_locations[piece_index] = past_pos



        elif color == 'black':

            if removed_bool:
                white_piece = self.main_chess_asset.captured_pieces_black[-1]
                self.main_chess_asset.white_pieces.append(white_piece)
                self.main_chess_asset.white_pieces_locations.append(
                    self.main_chess_asset.black_pieces_locations[piece_index])
                self.main_chess_asset.white_history.append(self.main_chess_asset.black_history_captured[-1])
                self.main_chess_asset.captured_pieces_black.pop(-1)
                self.main_chess_asset.black_history_captured.pop(-1)

            self.main_chess_asset.black_pieces_locations[piece_index] = past_pos

    def check_mate(self,color, recursive = True):
        """
        A function that checks the games endings state, is the King in check,
        """

        checking = [False, True]   # 1 check   2 check_mate
        if color == 'white':
            white_king_index = self.main_chess_asset.white_pieces.index('king')
            white_king_location = self.main_chess_asset.white_pieces_locations[white_king_index]
            black_attack_moves = [state for all_states in self.main_chess_asset.black_options for state in all_states]
            if white_king_location in black_attack_moves:
                checking[0] = True
                if recursive:
                    white_options_list = []
                    for i in range(len(self.main_chess_asset.white_pieces)):
                        white_piece_options_list = []
                        piece_index = i
                        piece_attack_moves =  self.main_chess_asset.white_options[piece_index]

                        for attack in piece_attack_moves:

                            past_location = self.main_chess_asset.white_pieces_locations[piece_index]
                            past_enemy_pieces = len(self.main_chess_asset.black_pieces)
                            self.main_chess_asset.white_pieces_locations[piece_index] = attack

                            self.piece_capture('white', attack)
                            self.main_chess_asset.black_options = self.check_all_options(
                                self.main_chess_asset.black_pieces, self.main_chess_asset.black_pieces_locations,'black'
                            )


                            check_temporary =  self.check_mate(color, recursive =  False)

                            checking[1] = check_temporary and checking[1]

                            if past_enemy_pieces != len(self.main_chess_asset.black_pieces):

                                removed_piece_bool = True
                            else:
                                removed_piece_bool = False

                            self.undo_check(past_location,piece_index,'white', removed_piece_bool)

                            if not check_temporary: # This move made the king safe
                                white_piece_options_list.append(attack)

                        white_options_list.append(white_piece_options_list)

                        # After the previous code, it has been determined wether the king is in check or check_mate,
                        #regardles, we need to uptade the allowed moves for the black side

                    self.main_chess_asset.white_options = white_options_list
                    return checking
                else:
                    return checking[0]
            elif not recursive :
                return checking[0]
            else:
                checking[1] = False
                return checking

        if color == 'black':
            black_king_index = self.main_chess_asset.black_pieces.index('king')
            black_king_location = self.main_chess_asset.black_pieces_locations[black_king_index]
            white_attack_moves = [state for all_states in self.main_chess_asset.white_options for state in all_states]
            if black_king_location in white_attack_moves:
                checking[0] = True
                if recursive:

                    black_options_list = []
                    for i in range(len(self.main_chess_asset.black_pieces)):
                        black_piece_options_list = []
                        piece_index = i
                        piece_attack_moves =  self.main_chess_asset.black_options[piece_index]
                        for attack in piece_attack_moves:


                            past_location = self.main_chess_asset.black_pieces_locations[piece_index]
                            past_enemy_pieces = len(self.main_chess_asset.white_pieces)
                            self.main_chess_asset.black_pieces_locations[piece_index] = attack
                            self.piece_capture('black', attack)

                            self.main_chess_asset.white_options = self.check_all_options(
                                self.main_chess_asset.white_pieces, self.main_chess_asset.white_pieces_locations,'white'
                            )


                            check_temporary =  self.check_mate(color, recursive =  False)

                            checking[1] = check_temporary and checking[1]

                            if past_enemy_pieces != len(self.main_chess_asset.white_pieces):

                                removed_piece_bool = True
                            else:
                                removed_piece_bool = False

                            self.undo_check(past_location,piece_index,'black', removed_piece_bool)

                            if not check_temporary: # This move made the king safe

                                black_piece_options_list.append(attack)


                        black_options_list.append(black_piece_options_list)

                        # After the previous code, it has been determined wether the king is in check or check_mate,
                        #regardles, we need to uptade the allowed moves for the black side

                    self.main_chess_asset.black_options = black_options_list
                    return checking
                else:
                    return checking[0]
            elif not recursive :
                return checking[0]
            else:
                checking[1] = False
                return checking

    def temp_king_check(self, color):
        """
        When all of the black and white attack options have been renders,
        whe need to look though them to make sure that id does not out ones own king in check.
        """
        if color == 'black':


            for i in range(len(self.main_chess_asset.black_pieces)):
                piece_index = i
                piece_attack_list = self.main_chess_asset.black_options[piece_index]
                piece_pos = self.main_chess_asset.black_pieces_locations[piece_index]
                white_pieces_count = len(self.main_chess_asset.white_pieces)
                piece_attacks_to_remove = []

                for attack in piece_attack_list:

                    # first lets change the position and see if there is a capture
                    self.main_chess_asset.black_pieces_locations[piece_index] = attack

                    self.piece_capture('black', new_position = attack)

                    if len(self.main_chess_asset.white_pieces) != white_pieces_count:
                        removed_bool = True
                    else:
                        removed_bool = False



                    # Now lets update the enemyies attacks
                    self.main_chess_asset.white_options = self.check_all_options(self.main_chess_asset.white_pieces,
                                           self.main_chess_asset.white_pieces_locations,
                                         'white')


                    white_attack_list = [white_attack for white_attacks in
                                         self.main_chess_asset.white_options for white_attack in white_attacks]

                    if self.main_chess_asset.black_pieces_locations[self.main_chess_asset.black_pieces.index('king')] \
                        in white_attack_list: # The king is unsafe

                        piece_attacks_to_remove.append(attack)

                    # Now lets redo or board for the next move, and white attacks
                    if len(self.main_chess_asset.white_pieces) != white_pieces_count:
                        removed_bool = True
                    else:   removed_bool = False


                    self.undo_check(piece_pos, piece_index,'black', removed_bool)
                    self.main_chess_asset.white_options = self.check_all_options(self.main_chess_asset.white_pieces,
                                                                                 self.main_chess_asset.white_pieces_locations,
                                                                                 'white')


                self.main_chess_asset.black_options[piece_index] = [
                attack for attack in piece_attack_list if attack not in piece_attacks_to_remove]

        elif color == 'white':
            print('white now')
            print('attacks now:', self.main_chess_asset.white_options)

            for i in range(len(self.main_chess_asset.white_pieces)):
                piece_index = i
                piece_attack_list = self.main_chess_asset.white_options[piece_index]
                piece_pos = self.main_chess_asset.white_pieces_locations[piece_index]
                black_pieces_count = len(self.main_chess_asset.black_pieces)
                piece_attacks_to_remove = []

                for attack in piece_attack_list:

                    # first lets change the position and see if there is a capture
                    self.main_chess_asset.white_pieces_locations[piece_index] = attack

                    self.piece_capture('white', new_position = attack)

                    if len(self.main_chess_asset.black_pieces) != black_pieces_count:
                        removed_bool = True
                    else:
                        removed_bool = False



                    # Now lets update the enemyies attacks
                    self.main_chess_asset.black_options = self.check_all_options(self.main_chess_asset.black_pieces,
                                           self.main_chess_asset.black_pieces_locations,
                                         'black')


                    black_attack_list = [black_attack for black_attacks in
                                         self.main_chess_asset.black_options for black_attack in black_attacks]

                    if self.main_chess_asset.white_pieces_locations[self.main_chess_asset.white_pieces.index('king')] \
                        in black_attack_list: # The king is unsafe

                        piece_attacks_to_remove.append(attack)

                    # Now lets redo or board for the next move, and white attacks
                    if len(self.main_chess_asset.black_pieces) != black_pieces_count:
                        removed_bool = True
                    else:   removed_bool = False


                    self.undo_check(piece_pos, piece_index,'white', removed_bool)
                    self.main_chess_asset.black_options = self.check_all_options(self.main_chess_asset.black_pieces,
                                                                                 self.main_chess_asset.black_pieces_locations,
                                                                                 'black')


                self.main_chess_asset.white_options[piece_index] = [
                attack for attack in piece_attack_list if attack not in piece_attacks_to_remove]
            print('new ones    ', self.main_chess_asset.white_options)

