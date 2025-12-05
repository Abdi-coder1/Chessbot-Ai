from . import piece
import copy

# noinspection PyTypeChecker,PyUnresolvedReferences
class Board:
    """
     The board is the main game object, since it holds the information
     regarding the game state. More specifically, the pieces location, histories, and captured.
     It also has the ability to modify itself, but that decision is made by the chess engine.
     Additionally , it contains functions to read the game state.
    """
    piece_classes = {
        'rook': piece.Rook,
        'knight': piece.Knight,
        'bishop': piece.Bishop,
        'queen': piece.Queen,
        'king': piece.King,
        'pawn': piece.Pawn
    }
    # creation of board
    def __init__(self, chess_asset, game_asset,board_id,initial,iterative_construction = True): # remember to put in chess and game asset!
        """
        Creation and initialization of the board consist of assigning different pieces classes
        to different spots, based on location. And creating the structure for history, captured
        and additional lists
        """
        # The Board have access to two unique and consistent assets, along with possible alternate setup
        self.chess_asset = chess_asset
        self.game_asset = game_asset
        self.piece_id =  0
        self.board_id = board_id
        self.initial = initial

        # Crate the board
        self.board_grid =  self.create_board_grid(self.chess_asset,self.game_asset)
        self.board_options = self.check_board_options(self.board_grid)
        self.board_capture = []

        #Game flow altering parameters
        self.board_end_state = {'white': False,
                                  'black': False,
                                'patt': False}
        self.pawn_promotion = {
                        'white': {'bool': False,
                                    'change_piece': None},
                        'black': {'bool': False,
                                    'change_piece': None,}
                                }
        if iterative_construction: # Parameters that itself includes boards
            self.board_history = {0:Board(self.chess_asset, self.game_asset,
                                        self.board_id,self.initial,False)}
            self.repetition_key = [[Board(self.chess_asset, self.game_asset,
                                          self.board_id, self.initial, False), 1]] # [board, amount]
        self.board_history_timer = -1
        self.repetition_bool = False
        if self.initial.change:
            self.board_setup(self.game_asset,self.chess_asset,self.initial) # Change the board state configurations

    # Creation of the board
    def create_board_grid(self, chess_asset, game_asset):
        """
        This function is responsible for creating the board, based on the starting configurations in
        chess_asset and game_asset. returns the board grid
        :return: a dictionary describing the board state and locations
        """
        board_grid = [
            [ None for _ in range(0, 8)]
            for _ in range(0, 8)
        ]
        # Fill the grid by iterating over the starting configuration in chess_asset
        for color in ['white', 'black']:
            for piece_type, pos_list in chess_asset.start_pieces[color].items():
                piece_class = Board.piece_classes[piece_type]
                if not any(isinstance(item, list) for item in pos_list):  # if the piece is unique (IE king/queen)
                    piece_object = piece_class(piece_color = color, piece_location = pos_list,
                                               piece_image_list = chess_asset.pictures[color][piece_type],
                                               piece_id = self.piece_id, chess_asset= chess_asset,
                                               game_asset = game_asset)
                    board_grid[pos_list[0]][pos_list[1]] = piece_object
                    self.piece_id += 1
                else:
                    for pos in pos_list:  # Iterate over the multiple versions of that piece
                        piece_object = piece_class(piece_color = color, piece_location = pos,
                                                   piece_image_list = chess_asset.pictures[color][piece_type],
                                                   piece_id = self.piece_id, chess_asset = chess_asset,
                                                   game_asset = game_asset)
                        board_grid[pos[0]][pos[1]] = piece_object
                        self.piece_id += 1
        return board_grid
    def board_setup(self, game_asset, chess_asset, initial):
        """
        Giving the preferred starting configuration,
        lets modfy the board using the board using the initial objets
        """
        pass

    # Functions to read game state
    def check_grid_safety(self,color, grid):
        """
        In certain application it is useful to se if a specific grid is safe,
        is used in casting.
        param color: which color is seeking safty?
        param grid: [y,x] the position
        :return: true or false
        """

        if color == 'white':
           enemy_attacks = [attack for piece_attack in self.board_options['black']\
                for attack in piece_attack]
        elif color == 'black':
            enemy_attacks = [attack for piece_attack in self.board_options['white'] \
                             for attack in piece_attack]
        # noinspection PyUnboundLocalVariable
        if grid in enemy_attacks:
            safty_bool = False
        else:
            safty_bool = True

        return safty_bool
    def check_grid_freedom(self, grid):
        """
        In certain application it is useful to se if a specific grid is free,
        is used in castling.
        param grid, [y,x] the position
        :return: true or false
        """
        all_piece_pos = [item.position for item in self.all_piece()]


        if grid in all_piece_pos:
            safty_bool = False
        else:
            safty_bool = True

        return safty_bool
    def check_board_options(self,board_grid):
        """
        By checking all the pieces valid moves, IE those on the board, we get
        a picture of all the avialbe moves for white or black.
        :param board_grid: the locations of every piece in the board
        :return: A dictionary of all options for respective color.
        """
        board_options = {'white': [], 'black': []} # ex [[[3,2], [4,5]], [[7,1], [6,2]], []]
        all_piece = self.all_piece()
        for game_piece in all_piece:
            game_piece.get_valid_move(board_grid)
            board_options[game_piece.color].append(game_piece.valid_moves)
        return board_options
    def check_capture(self, click_cord, selected_piece):
        """
        Based on the coordinates that a player wants to move a piece to,
        does that move entail a piece capture?
        :param click_cord: [y,x]
        :param selected_piece: who is moving?
        :return: A bool expression, and a potential piece
        """
        captured_piece = None
        capture = False
        enemy_piece_list = [item for row in self.board_grid for item in row
                            if item is not None and item.color != selected_piece.color]

        # regular capturing
        for enemy_piece in enemy_piece_list:
            if enemy_piece.position == click_cord:
                capture = True
                captured_piece = enemy_piece
        # some captures happen through an enpassant, lets see if that was used
        if selected_piece.__class__.__name__ == 'Pawn' and selected_piece.enpassant: # enpassant was viable, but was it used?
            color_pos_change = {'white': [-1, 1],
                                'black': [1,1]}
            if click_cord[0] - selected_piece.position[0] == color_pos_change[selected_piece.color][0] and \
                abs(click_cord[1] - selected_piece.position[1]) == 1: # is it moving diagonally
               for enemy_piece in enemy_piece_list: # is there  a piece under/above it?
                   if enemy_piece.position ==  [click_cord[0] + -1 * color_pos_change[selected_piece.color][0],
                                                click_cord[1]]:
                       capture = True
                       captured_piece = enemy_piece

        return capture, captured_piece
    def check_enpassant(self,maneuver_piece):
        """
        Based on the current board, is a passant avialbe for the other side?
        If white moves, we check black, and vice versa
        :param maneuver_piece, the piece that just moved
        :return: Change the an-passant value and modify valid moves
        """

        all_piece = self.all_piece()
        for item in all_piece: # enpassant is only avialbe one round
            if isinstance(item, piece.Pawn) :
                item.enpassant = False # # enp enp
        color_valid_pos = {'white': 4,
                           'black': 3 }  # positions of pawn that enables enpassant fo the other side
        color_y_change = {'white': 1,
                              'black': -1 }

        if isinstance(maneuver_piece,Board.piece_classes['pawn']):
            if maneuver_piece.position[0] == color_valid_pos[maneuver_piece.color]: # in position to be overtaken
                enemy_pawn_pieces = [game_piece for game_piece in all_piece \
                                     if isinstance(game_piece, Board.piece_classes['pawn']) \
                                     and game_piece.color != maneuver_piece.color]
                for enemy_pawn in enemy_pawn_pieces:
                    if enemy_pawn.position[0] == maneuver_piece.position[0] and \
                        abs(enemy_pawn.position[1] - maneuver_piece.position[1]) == 1 : # to the regular side, on the same row
                        enemy_pawn.enpassant = True
                        index = self.board_options_piece_match(enemy_pawn) # synchronize the board options
                        self.board_options[enemy_pawn.color][index].append([maneuver_piece.position[0] +  \
                                                                            color_y_change[maneuver_piece.color],
                                                                            maneuver_piece.position[1]])
                        enemy_pawn.valid_moves.append([maneuver_piece.position[0] + color_y_change[maneuver_piece.color],
                                                       maneuver_piece.position[1]])
    def check_pawn_promotion(self):
        """
        When a piece moves, the game could go into pawn_promotion state,
        this functions checks for it. Note that this function also works if there are multiple
        promotions in waiting by working though the quen in reverse position order,
        :return: The pawn-promotion state of a pawn and board can be changed
        """
        pawn_pieces = [item for row in self.board_grid for item in row \
            if item is not None and isinstance(item, Board.piece_classes['pawn'])]
        for pawn in pawn_pieces:
            if pawn.color == 'white' and pawn.position[0] == 0 or \
                    pawn.color == 'black' and pawn.position[0] == 7:
                pawn.promotion = True
                self.pawn_promotion[pawn.color]['bool'] = True
                self.pawn_promotion[pawn.color]['change_piece'] = pawn
    def check_castling(self):
        """
        Given the games current board, is it possible to perform a
        castle for either black or white? Remember we may have 0,1,2 rooks!
        :return change the castling attribute fo the king and board
        """
        castling_info ={
            'white': {'history': [False,False,False], # l_rook, king, r_rook
                         'safety': [False,False],        # l_side, r_side
                         'freedom': [False,False]},       # l_side, r_side
            'black': {'history': [False, False, False],  # l_rook, king, r_rook
                                   'safety': [False, False],  # l_side, r_side
                                   'freedom': [False, False]},      # l_side, r_side
                         }
        castling_y_pos = {'white':  7 ,
                          'black': 0}
        all_piece = self.all_piece()
        for color in ['white', 'black']:
            rook_pieces = [item for item in all_piece if isinstance(item, Board.piece_classes['rook']) and \
                           item.color == color] # len(rook_pieces) = 0  1 or  2
            king_piece = [item for item in all_piece if isinstance(item, Board.piece_classes['king']) and \
                           item.color == color][0]

            king_piece.castling_state['king_side'] = False
            king_piece.castling_state['queen_side'] = False

            if rook_pieces: # if we have rooks left:
                # first, check history
                rook_valid_pos = {'white': [[7,0],[7,7]],
                                  'black': [[0,0],[0, 7]]}
                king_valid_pos = {'white':[7,4],
                                  'black': [0,4]}
                for rook_piece in rook_pieces:
                    if not rook_piece.has_moved and rook_piece.position == rook_valid_pos[rook_piece.color][0]:
                        castling_info[color]['history'][0] = True
                    if not rook_piece.has_moved and rook_piece.position == rook_valid_pos[rook_piece.color][1]:
                        castling_info[color]['history'][2] = True
                if not king_piece.has_moved and king_piece.position == king_valid_pos[king_piece.color]:
                    castling_info[color]['history'][1] = True

                # second we watch safety, between and including king / rook squares
                pos_range_x_list = [[0,king_piece.position[1] + 1], [king_piece.position[1],8]]
                for pos_range in pos_range_x_list: # left or right
                    grid_safty_list = []
                    for i in range(pos_range[0], pos_range[1]):
                        grid_pos = [castling_y_pos[color],i]
                        safty_bool = self.check_grid_safety(color,grid_pos)
                        grid_safty_list.append(safty_bool)
                    if False not in grid_safty_list: # all the grids are safe.
                        castling_info[color]['safety'][pos_range_x_list.index(pos_range)] = True

                # third we watch freedom,
                pos_range_x_list = [[1, 4], [5, 7]]
                for pos_range in pos_range_x_list:
                    grid_freedom_list = []
                    for i in range(pos_range[0], pos_range[1]):
                        grid_pos = [castling_y_pos[color], i]
                        freedom_bool = self.check_grid_freedom(grid_pos)
                        grid_freedom_list.append(freedom_bool)
                    if False not in grid_freedom_list:
                        castling_info[color]['freedom'][pos_range_x_list.index(pos_range)] = True

                # with the information gathered, we update the king castling options, left then right
                if castling_info[color]['history'][1] and castling_info[color]['history'][2]: # history ok
                    if castling_info[color]['safety'][1]:   # safty ok
                        if castling_info[color]['freedom'][1]:  # freedom
                            king_piece.castling_state['king_side'] = True

                            # appending the move and synchronizing the board options
                            index = self.board_options_piece_match(king_piece)
                            self.board_options[king_piece.color][index].append([king_piece.position[0], king_piece.position[1] + 2])
                            king_piece.valid_moves.append([king_piece.position[0], king_piece.position[1] + 2])

                if castling_info[color]['history'][0] and castling_info[color]['history'][1]:  # history ok
                    if castling_info[color]['safety'][0]:  # safty ok
                        if castling_info[color]['freedom'][0]:  # freedom
                            king_piece.castling_state['queen_side'] = True

                            # appending the move and synchronizing the board options
                            index = self.board_options_piece_match(king_piece)
                            self.board_options[king_piece.color][index].append([king_piece.position[0], king_piece.position[1] - 2])
                            king_piece.valid_moves.append([king_piece.position[0], king_piece.position[1] - 2])

    # functions that change the board state
    def apply_piece_select(self, selected_piece):
        """
        On the board, there may only be one selected piece at a time,
        used for graphical interface. This functions handels this select attribute
        :param selected_piece, a piece object on the ture Board
        :return: Changed the selected attribute of selected piece
        """
        all_piece = self.all_piece()
        for game_piece in all_piece:
            game_piece.selected = False
        selected_piece.selected = True
    def apply_move(self,relevant_piece, end_pos):
        """
        Based on the chess_engine, lets apply the change in position. The object will be referenced
        in the new position, and behind it will leave a None object.
        :param relevant_piece:  The piece object
        :param end_pos: the end coordinates [y,x]
        :return:
        """
        self.board_grid[relevant_piece.position[0]][relevant_piece.position[1]] = None
        relevant_piece.apply_move(end_pos)
        self.board_grid[relevant_piece.position[0]][relevant_piece.position[1]] = relevant_piece
        relevant_piece.update_rectangle()
    def apply_capture(self,captured_piece):
        """
        Some moves capture pieces, if this happens we remove the piece from the grid
        :param captured_piece:
        :return: updates the board grid and capture list
        """
        captured_piece.alive = False
        self.board_capture.append(captured_piece)
        self.board_grid[captured_piece.position[0]][captured_piece.position[1]] = None
    def apply_castling(self, king, side):
        """
        When the maneuver robject includes castling we will perform it,
        This is done by updtaing the position of the king and the rook, acoridng to the rules.
        :param king, the king piece.
        :param side, is castling on queen or king side, left or right
        :return: updates the position of rook and king
         """

        if side == 'king_side':
            rook_current_pos =[king.position[0], 7 ]
            rook_new_pos = [king.position[0], king.position[1] + 1]
            king_new_pos = [king.position[0], king.position[1] + 2]
        else:
            rook_current_pos = [king.position[0], 0]
            rook_new_pos = [king.position[0], king.position[1] - 1]
            king_new_pos = [king.position[0], king.position[1] - 2]
        rook_piece = self.locate_piece_pos(rook_current_pos)

        # with the rook  and position in hand, lets apply the change.
        self.apply_move(rook_piece, rook_new_pos)
        self.apply_move(king,king_new_pos)

    # Check mate functions
    def check_mate(self,impending = False):
        """
        The game ends when either one of the pieces is in check_ mate or when a patt have
        been reach, this functions both takes away dangeorus move that exposes the king,
        and is unhelpfully when the king is in heck. In addition, it records the game state booth in the pieces, and board
        """

        all_piece = self.all_piece()
        filter_list = {'piece': [],
                       'moves': []}
        king_list = [self.locate(7), self.locate(23)]

        for king in king_list:
            # Reset from last time
            king.check_state['check'] = False
            king.check_state['check_mate'] = False
            king_in_check = not king.check_safety(self.board_options) # if danger -- True
            if  king_in_check:
                king.check_state['check'] = True
            if king_in_check or impending: # The king is under attack, or impending
                defence_bool = False # Is there any move that guarantees the safty of the king?
                for same_color_piece in [item for item in all_piece if item.color == king.color]:
                    for defence_move in same_color_piece.valid_moves:
                        # copy the board,and piece
                        copy_board = self.copy_board()
                        # noinspection PyNoneFunctionAssignment
                        copy_piece = copy_board.sync_board_match_piece(same_color_piece)
                        # apply move and check capture
                        captured_bool,captured_piece = copy_board.check_capture(defence_move,king)
                        if captured_bool:
                            copy_board.apply_capture(captured_piece)
                        copy_board.apply_move(copy_piece,defence_move)

                        #check king safety
                        copy_board.board_options = copy_board.check_board_options(copy_board.board_grid)
                        king_safety = copy_board.locate(king.id).check_safety(copy_board.board_options)
                        if king_safety:
                            defence_bool = True
                        if not king_safety: # The move did not make the king safe.
                            filter_list['piece'].append(same_color_piece)
                            filter_list['moves'].append(defence_move)

                # With the check_value and defence_bool, lets see if we have a check_mate or patt
                if not defence_bool and king.check_state['check']:
                    king.check_state['check_mate'] = True
                    self.board_end_state[king.color] = True
                elif not defence_bool and not king.check_state['check']:
                    self.board_end_state['patt'] = True

        if filter_list:
            self.filter_moves(filter_list)
    def impending_check(self):
        """
        Since, the king is never captured, those valid moves that as just predicted
        need to be filtered for moves that exposes the king to safety
        :return: updates the valid moves list
        """
        self.check_mate(impending=True)

    # Copy related functions
    # noinspection PyNoneFunctionAssignment
    def copy_board(self):
        """
        A function that copies the current board and returns that copy,
        the shared states are the game and chess config objects
        :return: a board object that is a copy
        """
        new_board = Board(self.chess_asset, self.game_asset, self.board_id + 1,self.initial)
        for i in range(len(new_board.board_grid)):
            for j in range(len(new_board.board_grid[i])):
                if self.board_grid[i][j] is None:
                    new_board.board_grid[i][j] = None
                elif self.board_grid[i][j] is not None:
                    # noinspection PyUnresolvedReferences
                    new_board.board_grid[i][j] = self.board_grid[i][j].copy()
        new_board.board_options = copy.deepcopy(self.board_options)
        for captured_piece in self.board_capture:
            copy_piece = captured_piece.copy()
            new_board.board_capture.append(copy_piece)
        new_board.board_end_state = copy.deepcopy(self.board_end_state)

        if self.pawn_promotion['white']['bool']:
            new_board.pawn_promotion['white']['bool'] = True
            new_board.pawn_promotion['white']['change_piece'] = new_board.sync_board_match_piece(
                                                                self.pawn_promotion['white']['change_piece'])
        if self.pawn_promotion['black']['bool']:
            new_board.pawn_promotion['black']['bool'] = True
            new_board.pawn_promotion['black']['change_piece'] = new_board.sync_board_match_piece(
                self.pawn_promotion['black']['change_piece'])

        return  new_board

    # Comparing  between boards
    def sync_board_match_piece(self, sync_piece):
        """
        Since the sync Board and the actual boards are identical, we somtimes need to match
        the sync board pieces to teh true board pieces. Self, refers to the true board
        and the sync piece is from the current board
        :param sync_piece: A piece from the other board,
        :return: that corrosponding piece in the board that called the function
        """
        all_board_pieces = [item for row in self.board_grid for item in row if item is not None]
        for board_piece in all_board_pieces:
            if sync_piece.position == board_piece.position and type(sync_piece) == type(board_piece):
                true_piece = board_piece
                return true_piece
    def board_options_piece_match(self, board_piece):
        """
        When the boards options have been established, this function can
        take in a piece, and find the index of its valid moves in the options list
        :param board_piece, the piece on the board we are concerned about
        :return: the index in the option list
        """
        index = None
        for i in range(len(self.board_options[board_piece.color])):
            if board_piece.valid_moves == self.board_options[board_piece.color][i]:
                index = i
        return index
    @staticmethod
    def board_compare(board_1, board_2):
        """
        In many aspects of the game, it is useful to know whether two boards are similar
        and if so, in what way. Checks position, attack patterns, and special rights
        :param board_1: The first board object
        :param board_2: The second Board object
        :return: True or false boolean
        """
        similarity = {'position': True, 'move_pattern': True, 'final':False}
        for row in range(len(board_1.board_grid)):
            for column in range(len(board_1.board_grid)):
                object_1 = board_1.board_grid[row][column]
                object_2 = board_2.board_grid[row][column]
                if object_1 is not None and object_2 is not None:
                    similarity['position'] = similarity['position'] and \
                                             type(object_1) == type(object_2)

                    similarity['move_pattern'] = similarity['move_pattern'] and \
                                                 object_1.valid_moves == object_2.valid_moves
        # obs! by checking for valid moves we don't need to check enpassant / Castle / promotion
        if similarity['position'] and similarity['move_pattern']: similarity['final'] = True
        return similarity['final']

    # useful side functions
    def locate_piece_pos(self, grid_pos):
        """
        Somtimes, we may need to find a piece, based on its position,
        this will accomplish that.
        :param grid_pos:
        :param self
        :return: a piece that has that position
        """
        return self.board_grid[grid_pos[0]][grid_pos[1]]
    def locate(self,locate_id):
        """
        BAse don't the id of the piece that iwant to find in the relevant board grid,
        return that piece
        :param locate_id: A special number for every piece, int
        :return: that piece wit the id
        """
        located_piece = None
        all_piece = self.all_piece()
        for game_piece in all_piece:
            if game_piece.id == locate_id:
                located_piece = game_piece
        return located_piece
    def filter_moves(self,filter_list):
        """
        Based on the valid moves for all pieces, and the moves that I want to remove,
        for instance through check och impeding check, remove them.
        :param filter_list: a lis with piece, and the move that will be filtered from red that piece
        [[piece, move], [piece, move], ...]
        :return: and updates options list for the board list.
        """
        for i in range(len(filter_list['piece'])):
            filter_list['piece'][i].valid_moves.remove(filter_list['moves'][i])

        # when the moves of the pieces are filtered, we now redo the board options
        board_options = {'white': [], 'black': []}  # ex [[[3,2], [4,5]], [[7,1], [6,2]], []]
        all_piece = self.all_piece()
        for game_piece in all_piece:
            board_options[game_piece.color].append(game_piece.valid_moves)

        self.board_options = board_options
    def all_piece(self, color=None):
        """
        When generating the valid moves for a game piece, it often needs a list of all the current
        pieces. This functions handels this. Although sometimes, we also need a list of all the enemy  pieces,
        so this function handles this.
        :param color,  what color should the pieces in the returned list have, default is irrelevant
        :return: A list of all the current board pieces with that specified color.
        """
        all_piece = [item for row in self.board_grid for item in row if item is not None]
        if color is not None:
            subset = [item for item in all_piece if item.color == color]
            return_list = subset
        else:
            return_list = all_piece
        return return_list

    #History functions
    def record_board_history(self):
        """
        Whenever a change to the boards state is made, no matter what kind,
        this function will take a snapshot of the boards and its pieces as a copy
        and save it
        :return: Updates the board_history list
        """

        self.board_history.update(
            {len(self.board_history) : self.copy_board()}
        )
    def repetition_eval(self):
        """
        After a move is made, we check the current board state,
        against all previous ones, in order to determine if the same state
        has occurred three times. If so, return true. Assumes that the current board has history
        :return:
        """
        repetition = [False,False]
        new_board = next(iter(
            reversed(list(self.board_history.values()))
        ))
        for compare in self.repetition_key:
            compare_board = compare[0]
            compare_bool = self.board_compare(new_board,compare_board)

            if compare_bool:
                compare[1] += 1
                repetition[1] = True
                break
            else:   continue
        if not repetition[1]:
            self.repetition_key.append([new_board,1])
        if 3 in [compare[1] for compare in self.repetition_key ]:
                repetition[0] = True
        self.repetition_bool = repetition[0]
