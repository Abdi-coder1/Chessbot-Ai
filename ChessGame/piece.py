import copy
class BasePiece:
    """
    This class contains all the commons attributes and methods for every type of piece,
    rook, pawn, bishop, king, queen, and knight. In this way, all the pieces will have access
    to the same methods, but still keep their individuality. Notice! That this programme never actually
     creates a Base peace but rather uses it as an ABC (Abstract base class).
    """
    def __init__(self, piece_color, piece_location, piece_image_list,
                piece_id, chess_asset, game_asset):
        """
        When creating a Base_piece we pass in the above attributes, and the rest is filled in,
        in short, this functions as an ABC (Abstract class)
        """
        # we start by defining common attributes
        self.alive = True                           # Has it been captured? Bool
        self.position = piece_location              # What is its location? [int,int] [y,x]
        self.history = [self.position]              # The history of moves [[int,int], [int,int], ...]
        self.valid_moves = []                       # At the current time, what moves can it make? [[int,int], [int,int]..]
        self.color = piece_color                    # White or black? str
        if self.color == 'white':
            self.highlight_color = 'red'
            self.castling_color = (139,0,0)
        else:
            self.highlight_color = 'blue'
            self.castling_color = (0,0,139)
        self.images = {'big': piece_image_list[0],   # what image has it? pygame.Surface
                       'small': piece_image_list[1]}
        self.dimension = chess_asset.board_appearance['square_dimension']     # How big is the occupying space? Int
        self.images_rect = {'big': piece_image_list[0].get_rect(topleft = (self.position[1] * self.dimension + 10,
                                                                           self.position[0] * self.dimension + 10)),
                            'small': piece_image_list[1].get_rect(topleft =(0,0))
                            }
        self.selected = False                       # True or false,has it been selected for an action? Bool
        self.id = piece_id                          # What is the piece id?:  int
        self.has_moved = False                      # since that games inception, have this pieve moved? Bool

        # Apart from above attributes, the pieces need access to the different assets of the game
        self.chess_asset = chess_asset
        self.game_asset =  game_asset

    def copy(self):
        """
        For different simulations, it is useful to copy the piece instead of manipulating it directly
        :return: A perfect copy of the relevant object, type = type(self)
        """
        copy_piece = self.__class__(
            self.color, self.position,
            [self.images['big'], self.images['small']],
             self.id, self.chess_asset, self.game_asset)
        copy_piece.alive = self.alive
        copy_piece.history = copy.deepcopy(self.history)
        copy_piece.valid_moves = copy.deepcopy(self.valid_moves)
        copy_piece.selected = self.selected
        copy_piece.has_moved = self.has_moved



        return copy_piece

    def record_history(self, recent_move):
        """
        Given the move that was just made, we need to update the piece history
        :param recent_move: type = [y,x]
        :return: updates the history list though appending.
        """
        self.history.append(recent_move)
        self.has_moved = True

    def apply_move(self, new_pos):
        """
        Given the position that the piece will move to, lets apply the change
        :param new_pos: type = [int,int]
        :return: Updates this piece position
        """
        self.position = new_pos

    def update_rectangle(self):
        """
        When the position of the piece on the board moves, we will need to update the rectangel
        to reflect this change
        """
        self.images_rect['big'].topleft = (self.position[1] * self.dimension + 10,
                                                     self.position[0] * self.dimension + 10)
    @staticmethod
    def all_piece(board_grid, color = None):
        """
        When generating the valid moves for a game piece, it often needs a list of all the current
        pieces. This functions handels this. Although sometimes, we also need a list of all the enemy  pieces,
        so this function handles this.
        :param color,  what color should the pieces in the returned list have, default is irrelevant
        :param board_grid, What is the current board grid like.
        :return: A list of all the current board pieces with that specified color.
        """
        return_list = []
        all_piece = [item for row in board_grid for item in row if item is not None]
        if color is not None:
            subset = [item for item in all_piece if item.color == color]
            return_list = subset
        else:
            return_list = all_piece
        return return_list

class Pawn(BasePiece):
    """
    This class contains the pawn, of which there are 8,
    Its special thing is the valid moves, an_passant,and promotion
    """
    def __init__(self, piece_color, piece_location, piece_image_list,
                piece_id, chess_asset, game_asset):

        super().__init__(piece_color, piece_location, piece_image_list,
                piece_id, chess_asset, game_asset)
        # Since the pawn has access to an_passant and promotion it will get two more attributes
        self.enpassant = False  # Bool
        self.promotion = False   # Bool

    def get_valid_move(self, board_grid):
        """
        Based on the current board_grid and the pawn location and its state, what moves can it make?
        :param board_grid: The current board_grid state, type = Board_grid
        :return updates the pawn valid moves
        """
        valid_moves = []
        all_piece = Pawn.all_piece(board_grid)
        all_piece_position = [item.position for item in  Pawn.all_piece(board_grid)]
        enemy_positions_list = [item.position for item in all_piece if item.color != self.color]
        # Since the moves are symmetrical across colors, lets use a reverse factor.
        if self.color == 'black':
            color_factor = 1
            color_pos = 1
        else:
            color_factor = -1
            color_pos = 6

        # Moving forward
        if [self.position[0] + color_factor, self.position[1]] not in all_piece_position:
            if 0 <= self.position[0] + color_factor < 8 and\
                    0 <= self.position[1] < 8:
                valid_moves.append([self.position[0] + color_factor, self.position[1]])

        # Moving two steps forward
        if [self.position[0] + (2*color_factor), self.position[1]] not in all_piece_position and \
                [self.position[0] + color_factor, self.position[1]] not in all_piece_position and \
                self.position[0] == color_pos:
            if 0 <= self.position[0] + (2 * color_factor) <8 \
                    and 0 <= self.position[1] < 8:
                valid_moves.append([self.position[0] + (2*color_factor), self.position[1]])

        # Checking capture left
        if [self.position[0] + color_factor, self.position[1] - 1] in enemy_positions_list and \
                0 <= self.position[0] + color_factor < 8 and \
                 0 <= self.position[1] -1 < 8 :
            valid_moves.append([self.position[0] + color_factor, self.position[1]-1])

        # Checking capture right
        if [self.position[0] + color_factor, self.position[1] + 1] in enemy_positions_list and \
                0 <= self.position[0] + color_factor < 8 and \
                0 <= self.position[1] + 1 < 8 :
            valid_moves.append([self.position[0] + color_factor, self.position[1] + 1])
        self.valid_moves = valid_moves

    def copy(self):
        """
        This function creates an identical piece to the current pawn.
        :return: A perfect copy of the relevant object, type = type(self)
        """
        copy_piece = super().copy()
        copy_piece.enpassant = self.enpassant
        copy_piece.promotion = self.promotion
        return copy_piece

class Rook(BasePiece):
    """
    This class contains the Rook, of which there are two, Its special thing is
    the valid moves, and castling.
    """
    def get_valid_move(self, board_grid):
        """
         Based on the current board_grid and the rook location, what moves can it make?
        :param board_grid: The current board_grid state, a copy, type = Board_grid
        :return updates the Rook valid moves
        """

        valid_moves = []
        ally_position_list = [item.position for item in Rook.all_piece(board_grid, color = self.color)]
        if self.color == 'white':
            enemy_positions_list = [item.position for item in Rook.all_piece(board_grid,color = 'black')]
        else:
            enemy_positions_list = [item.position for item in Rook.all_piece(board_grid,color = 'white')]
        direction_mod = [[-1,0],[1,0],[0,1],[0,-1]] # For the four different directions [y,x]

        # The rooks moves are made in chains
        for y_mod,x_mod in direction_mod:
            path = True    # is the path still valid?
            chain_mod = 1  # squares of movement
            while path:
                possible_new_pos = [self.position[0] + y_mod * chain_mod, self.position[1] + x_mod * chain_mod]
                if possible_new_pos not in ally_position_list and \
                        0 <= possible_new_pos[1] < 8\
                        and 0 <= possible_new_pos[0] <8:  # square is valid
                    valid_moves.append(possible_new_pos)
                    chain_mod += 1
                    if possible_new_pos in enemy_positions_list:
                        path = False
                else: # was an empty square
                    path = False
        self.valid_moves = valid_moves

class Knight(BasePiece):
    """
    This class contains the Knight, of which there are two,
    Its special thing is the valid moves
   """
    def get_valid_move(self, board_grid):
        """
        Based on the current board_grid and the Knight location, what moves can it make?
        :param board_grid: The current board_grid state, type = Board_grid
        :return updates the Knight valid moves
        """
        valid_moves = []
        ally_position_list = [item.position for item in Knight.all_piece(board_grid,color=self.color)]
        # Relative to starting location, where can the piece go? [y,x]
        relative_pos = [[1, 2], [-1, 2], [1, -2], [-1, -2], [2, 1], [2, -1], [-2, 1], [-2, -1]]

        for pos_transformer in relative_pos:
            new_pos = [self.position[0] + pos_transformer[0], self.position[1] + pos_transformer[1]]
            if new_pos not in ally_position_list and \
                    0 <= new_pos[0] < 8 and \
                    0 <= new_pos[1] < 8 :  # viable/withing bounds
                valid_moves.append(new_pos)
        self.valid_moves = valid_moves

class Queen(BasePiece):
    """
    This class contains the queen, of which there are 1,
    Its special thing is the valid moves
    """
    def get_valid_move(self, board_grid):
        """
        Based on the current board_grid and the queen location, what moves can it make?
        :param board_grid: The current board_grid state, type = Board_grid
        :return updates the queen valid moves
        """
        valid_moves = []
        ally_position_list = [item.position for item in Queen.all_piece(board_grid) if item.color == self.color]
        if self.color == 'white':
            enemy_positions_list = [item.position for item in Queen.all_piece(board_grid, color = 'black')]
        else:
            enemy_positions_list = [item.position for item in Queen.all_piece(board_grid, color = 'white')]
        direction_mod_1 = [[-1, 0], [1, 0], [0, 1], [0, -1]]  # For the four different directions [y,x]
        # up_left, up_right, down_left, down_right
        direction_mod_2 = [[-1, -1], [-1, 1], [1, -1], [1, 1]]  # For the four different directions [y,x]
        for y_mod, x_mod in direction_mod_1 + direction_mod_2:
            path = True  # is the path still valid?
            chain_mod = 1  # squares f movement
            while path:
                possible_new_pos = [self.position[0] + y_mod * chain_mod, self.position[1] + x_mod * chain_mod]
                if possible_new_pos not in ally_position_list and \
                        0 <= possible_new_pos[1] < 8  and \
                        0 <= possible_new_pos[0] < 8: # square is valid
                    valid_moves.append(possible_new_pos)
                    chain_mod += 1
                    if possible_new_pos in enemy_positions_list:
                        path = False
                else:
                    path = False
        self.valid_moves = valid_moves

class King(BasePiece):
    """
    This class contains the King, of which there are 1,
    Its special thing is the valid moves, and check and Check_mate
    """
    def __init__(self, piece_color, piece_location, piece_image_list,
                 piece_id, chess_asset, game_asset):
        super().__init__(piece_color, piece_location, piece_image_list,
                         piece_id, chess_asset, game_asset)
        # Its own parameters
        self.check_state = {'check': False, 'check_mate': False} # dic
        self.castling_state = {'queen_side': False,  'king_side': False} # dic

    def get_valid_move(self, board_grid):
        """
        Based on the current board_grid and the king location, what moves can it make?
        :param board_grid: The current board_grid state, type = Board_grid
        :return updates the King valid moves
        """
        valid_moves = []
        ally_position_list = [item.position for item in King.all_piece(board_grid, color = self.color)]
        # Relative to starting location, where can the piece go? [y,x]
        relative_pos = [[-1, 0], [-1, 1], [-1, -1], [0, 1], [0, -1], [1, 0], [1, 1], [1, -1]]

        for pos_transformer in relative_pos:
            new_pos = [self.position[0] + pos_transformer[0], self.position[1] + pos_transformer[1]]
            if new_pos not in ally_position_list and \
                    0 <= new_pos[0] < 8 and \
                    0 <= new_pos[1] < 8:  # empty and withing bounds
                valid_moves.append(new_pos)
        self.valid_moves = valid_moves

    def check_safety(self, board_options):
        """
        Based on the updated board with the new options, is the king in safety?
        :param board_options: The board options, containing all the current attacks
        :return: True or false Bool
        """
        colors = ['white', 'black']
        safe = True
        enemy_attacks = board_options[colors[(colors.index(self.color) + 1) % 2 ]]
        for piece_attack in enemy_attacks:
            for attack in piece_attack:
                if self.position == attack:
                    safe = False
        return safe

    def copy(self):
        """
        this functions creates and modifies a piece so that copy is returned.
        :return: A perfect copy of the relevant object, type = type(self)
        """
        copy_piece = super().copy()
        copy_piece.check_state = copy.deepcopy(self.check_state)
        copy_piece.castling_state = copy.deepcopy(self.castling_state)
        return copy_piece

class Bishop(BasePiece):
    """
    This class contains the Bishop, of which there are two,
    Its special thing is the valid moves
    """
    def get_valid_move(self, board_grid):
        """
        Based on the current board_grid and the bishop location, what moves can it make?
        :param board_grid: The current board_grid state, a copy, type = Board_grid
        :return updates the Bishop valid moves
        """
        valid_moves = []
        all_piece = [item for row in board_grid for item in row if item is not None]
        ally_position_list = [item.position for item in Bishop.all_piece(board_grid,color = self.color)]
        if self.color == 'white':
            enemy_positions_list = [item.position for item in Queen.all_piece(board_grid, color = 'black')]
        else:
            enemy_positions_list = [item.position for item in Queen.all_piece(board_grid, color = 'white')]
        # up_left, up_right, down_left, down_right
        direction_mod = [[-1, -1], [-1, 1], [1, -1], [1, 1]]  # For the four different directions [y,x]

        # The prospering of the rooks moves are made in chains
        for y_mod, x_mod in direction_mod:
            path = True  # is the path still valid?
            chain_mod = 1  # squares f movement
            while path:
                possible_new_pos = [self.position[0] + y_mod * chain_mod, self.position[1] + x_mod * chain_mod]
                if possible_new_pos not in ally_position_list and \
                        0 <= possible_new_pos[1] < 8  and \
                        0 <= possible_new_pos[0] < 8 :  # square is valid
                    valid_moves.append(possible_new_pos)
                    chain_mod += 1
                    if possible_new_pos in enemy_positions_list:
                        path = False
                else:
                    path = False
        self.valid_moves = valid_moves