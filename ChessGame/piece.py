

class BasePiece:
    """
    This class contains all the commons attributes and methods for every type of piece,
    rook, pawn, bishop, king, queen, and knight. In this way, all the pieces will have access
    to the same methods, but still keep their individually
    """
    def __init__(self, piece_color, piece_state, piece_location, piece_history, piece_valid_move,
                 piece_image_list, piece_selected, piece_id, chess_asset, game_asset):

        # we start by defining common attributes
        self.alive = piece_state                 # Has it been captured? Bool
        self.position = piece_location           # What is its location? [int,int]
        self.history = piece_history             # The history of moves [[int,int], [int,int], ...]
        self.valid_moves = piece_valid_move      # At the current time, what moves can it make? [[int,int], [int,int]..]
        self.color = piece_color                  # White or black? str
        self.images = {'big': piece_image_list[0],# what image has it? pygame.Surface
                       'small': piece_image_list[1]}
        self.selected = piece_selected              # True or false,has it been selected for an action? Bool
        self.id = piece_id                          # What is the piece id?:  int

        # Apart from above attributes, the pieces need access to the different assets of the game
        self.chess_asset = chess_asset
        self.game_asset =  game_asset


    def coopy(self):
        """
        For different simulations, it is useful to copy the piece instead of manipulating it directly
        :return: A perfect copy of the relevant object
        """
        copy_piece = self.__class__(
            self.color,self.alive, self.position,
            self.history,self.valid_moves,
            self.images, self.selected, self.id,
            self.chess_asset, self.game_asset)
        return copy_piece

    def record_history(self, recent_move):
        """
        Given the move that was just made, we need to update the piece history
        :param recent_move: type = [int,int]
        :return: updates the history list though appending.
        """
        self.history.append(recent_move)

    def apply_move(self, new_pos):
        """
        Given the position that the piece will move to, lets apply the change
        :param new_pos: type = [int,int]
        :return: Updates this piece position
        """
        self.position = new_pos

    def undo_move(self):
        """
        For simulations, pieces need to redo their recent moves.
        This function takes the most recent move, erases it and reset
        the previous state
        :return: The previous states of all attributes
        """
        recent_move = self.history[-1]
        self.position = recent_move
        self.history.pop(-1)

    def draw_piece(self):
        """
        Based ont the piece position, can we draw the piece?
        :return: draws the piece on thw window
        """
        self.game_asset.window.blit(self.images['big'], [self.position[0] * self.chess_asset.square_dimension + 10,
                                         self.position[1] * self.chess_asset.square_dimension + 10])







class Pawn(BasePiece):
    """
    This class contains the pawn, of which there are 8,
    Its special thing is the valid moves, an_passant,and promotion
    """
    def __init__(self, piece_color, piece_state, piece_location, piece_history, piece_valid_move,
                 piece_image_list, piece_selected, piece_id, chess_asset, game_asset, 
                 piece_enpassant, piece_promotion):
        super().__init__(piece_color, piece_state, piece_location, piece_history, piece_valid_move,
                 piece_image_list, piece_selected, piece_id, chess_asset, game_asset,)
        
        # Since the pawn has access to an_passant and promotion it will get two more attributes
        self.enpassant = piece_enpassant
        self.promotion = piece_promotion

    def get_valid_move(self, board):
        """
        Based on the current board and the pawn location and its state, what moves can it make?
        Remember, it has an_passant and promotion available to it.
        :param board: The current board state, a copy, type = Board
        :return updates the pawn valid moves
        """
        pass

class Rook(BasePiece):
    """
    This class contains the Rook, of which there are two, Its special thing is
    he valid moves, and castling. So it has more functionality.
    """
    def __init__(self, piece_color, piece_state, piece_location, piece_history, piece_valid_move,
                 piece_image_list, piece_selected, piece_id, chess_asset, game_asset):
        super().__init__(piece_color, piece_state, piece_location, piece_history, piece_valid_move,
                 piece_image_list, piece_selected, piece_id, chess_asset, game_asset)

    def get_valid_move(self, board):
        """
         Based on the current board and the bishop location, what moves can it make?
        :param board: The current board state, a copy, type = Board
        :return updates the Rook valid moves
        """
        pass

class Knight(BasePiece):
    """
    This class contains the Knight, of which there are two,
    Its special thing is the valid moves
   """
    def __init__(self, piece_color, piece_state, piece_location, piece_history, piece_valid_move,
                 piece_image_list, piece_selected, piece_id, chess_asset, game_asset):
        super().__init__(piece_color, piece_state, piece_location, piece_history, piece_valid_move,
                 piece_image_list, piece_selected, piece_id, chess_asset, game_asset)

    def get_valid_move(self, board):
        """
        Based on the current board and the Knight location, what moves can it make?
        :param board: The current board state, a copy, type = Board
        :return updates the Knight valid moves
        """
        pass

class Queen(BasePiece):
    """
    This class contains the queen, of which there are 1,
    Its special thing is the valid moves
    """
    def __init__(self, piece_color, piece_state, piece_location, piece_history, piece_valid_move,
                 piece_image_list, piece_selected, piece_id, chess_asset, game_asset):
        super().__init__(piece_color, piece_state, piece_location, piece_history, piece_valid_move,
                 piece_image_list, piece_selected, piece_id, chess_asset, game_asset)


    def get_valid_move(self, board):
        """
        Based on the current board and the queen location, what moves can it make?
        :param board: The current board state, a copy, type = Board
        :return updates the queen valid moves
        """
        pass

class King(BasePiece):
    """
    This class contains the King, of which there are 1,
    Its special thing is the valid moves, and check and Check_mate
    """
    def __init__(self, piece_color, piece_state, piece_location, piece_history, piece_valid_move,
                 piece_image_list, piece_selected, piece_id, chess_asset, game_asset,
                 check_state_list, castling_state_list):

        # since the game state is tied to the kings state, we will defined following check attributes
        super().__init__(piece_color, piece_state, piece_location, piece_history, piece_valid_move,
                 piece_image_list, piece_selected, piece_id, chess_asset, game_asset)
        self.check_state = {'check': check_state_list[0], 'check_mate': check_state_list[1]}
        
        # And since the king can castle, we define and castling state
        self.castling_state = {'queen_side':castling_state_list[0],  'king_side': castling_state_list[1]}




    def get_valid_move(self, board):
        """
        Based on the current board and the king location, and its threat level,
        what moves can it make? Remember, moves that endangers it are not allowed
        :param board: The current board state, a copy, type = Board
        :return updates the King valid moves
        """
        pass

class Bishop(BasePiece):
    """
    This class contains the Bishop, of which there are two,
    Its special thing is the valid moves
    """
    def get_valid_move(self, board):
        """
        Based on the current board and the bishop location, what moves can it make?
        :param board: The current board state, a copy, type = Board
        :return updates the Bishop valid moves
        """
        pass

