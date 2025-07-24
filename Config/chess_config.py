import pygame.image
import pygame.draw

class Chessassets:
    """
    This Class contains all the assets needed to start and play the chess game.
    """
    def __init__(self):
        self.white_pieces = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook',
                        'pawn', 'pawn',    'pawn',   'pawn','pawn',   'pawn',   'pawn',   'pawn', ]
        self.white_pieces_locations = [[0,7], [1,7], [2,7], [3,7], [4,7], [5,7], [6,7], [7,7],
                                  [0,6], [1,6], [2,6], [3,6], [4,6], [5,6], [6,6], [7,6]]    #[column, rad]
        self.captured_pieces_white = []   # what have white captured?

        self.black_pieces = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook',
                        'pawn', 'pawn',    'pawn',   'pawn','pawn',   'pawn',   'pawn',   'pawn', ]
        self.black_pieces_locations = [[0,0], [1,0], [2,0], [3,0], [4,0], [5,0], [6,0], [7,0],
                                  [0,1], [1,1], [2,1], [3,1], [4,1], [5,1], [6,1], [7,1]]
        self.captured_pieces_black = []

        # 0: White turn --> no selected. 1: white turn --> piece selected. 2: Black turn --> no selected. 3: Black turn --> piece selected
        self.turn_step = 0
        self.turn_step_text_list = ['White: Select a piece', 'White: Move that piece',
                          'Black: select a piece', 'Black: Move that piece' ]

        self.selected_piece_index = None  # Which piece has been chosen?, arbitrary large value when none are selected
        self.valid_moves = [] # The current valid moves I am looking at for a piece

        self.white_options = []  # What are all of whites options?
        self.black_options = []  # what are all of blacks options.

        self.white_history = [[[0,7]], [[1,7]], [[2,7]], [[3,7]], [[4,7]], [[5,7]], [[6,7]], [[7,7]],
                              [[0,6]], [[1,6]], [[2,6]], [[3,6]], [[4,6]], [[5,6]], [[6,6]], [[7,6]]]

        self.black_history = [[[0,0]], [[1,0]], [[2,0]], [[3,0]], [[4,0]], [[5,0]], [[6,0]], [[7,0]],
                              [[0,1]], [[1,1]], [[2,1]], [[3,1]], [[4,1]], [[5,1]], [[6,1]], [[7,1]]]

        self.black_history_captured= []  # the history that blakc captured frm white
        self.white_history_captured = [] # the hisotry that white captured form black




        self.black_queen = pygame.image.load(r'C:\Users\Abdi\PycharmProjects\bilder\chess_pieces\black queen.png')
        self.black_queen = pygame.transform.scale(self.black_queen,(60,60))
        self.black_queen_small = pygame.transform.scale(self.black_queen,(45,45))

        self.black_king = pygame.image.load(r'C:\Users\Abdi\PycharmProjects\bilder\chess_pieces\black king.png')
        self.black_king = pygame.transform.scale(self.black_king,(60,60))
        self.black_king_small = pygame.transform.scale(self.black_king,(45,45))

        self.black_rook = pygame.image.load(r'C:\Users\Abdi\PycharmProjects\bilder\chess_pieces\black rook.png')
        self.black_rook = pygame.transform.scale(self.black_rook,(60,60))
        self.black_rook_small = pygame.transform.scale(self.black_rook,(45,45))

        self.black_bishop = pygame.image.load(r'C:\Users\Abdi\PycharmProjects\bilder\chess_pieces\black bishop.png')
        self.black_bishop = pygame.transform.scale(self.black_bishop,(60,60))
        self.black_bishop_small = pygame.transform.scale(self.black_bishop,(45,45))

        self.black_knight = pygame.image.load(r'C:\Users\Abdi\PycharmProjects\bilder\chess_pieces\black knight.png')
        self.black_knight = pygame.transform.scale(self.black_knight,(60,60))
        self.black_knight_small = pygame.transform.scale(self.black_knight,(45,45))

        self.black_pawn = pygame.image.load(r'C:\Users\Abdi\PycharmProjects\bilder\chess_pieces\black pawn.png')
        self.black_pawn = pygame.transform.scale(self.black_pawn,(60,60))
        self.black_pawn_small = pygame.transform.scale(self.black_pawn,(45,45))

        self.black_pieces_images = [self.black_pawn, self.black_king, self.black_queen, self.black_knight,
                                    self.black_rook, self.black_bishop]
        self.black_pieces_images_small = [self.black_pawn_small, self.black_king_small, self.black_queen_small,
                                          self.black_knight_small, self.black_rook_small, self.black_bishop_small]

         #--------------------
        self.white_queen = pygame.image.load(r'C:\Users\Abdi\PycharmProjects\bilder\chess_pieces\white queen.png')
        self.white_queen = pygame.transform.scale(self.white_queen,(60,60))
        self.white_queen_small = pygame.transform.scale(self.white_queen,(45,45))

        self. white_king = pygame.image.load(r'C:\Users\Abdi\PycharmProjects\bilder\chess_pieces\white king.png')
        self.white_king = pygame.transform.scale(self.white_king,(60,60))
        self.white_king_small = pygame.transform.scale(self.white_king,(45,45))

        self.white_rook = pygame.image.load(r'C:\Users\Abdi\PycharmProjects\bilder\chess_pieces\white rook.png')
        self.white_rook = pygame.transform.scale(self.white_rook,(60,60))
        self.white_rook_small = pygame.transform.scale(self.white_rook,(45,45))

        self.white_bishop = pygame.image.load(r'C:\Users\Abdi\PycharmProjects\bilder\chess_pieces\white bishop.png')
        self.white_bishop = pygame.transform.scale(self.white_bishop,(60,60))
        self.white_bishop_small = pygame.transform.scale(self.white_bishop,(45,45))

        self.white_knight = pygame.image.load(r'C:\Users\Abdi\PycharmProjects\bilder\chess_pieces\white knight.png')
        self.white_knight = pygame.transform.scale(self.white_knight,(60,60))
        self.white_knight_small = pygame.transform.scale(self.white_knight,(45,45))

        self.white_pawn = pygame.image.load(r'C:\Users\Abdi\PycharmProjects\bilder\chess_pieces\white pawn.png')
        self.white_pawn = pygame.transform.scale(self.white_pawn,(60,60))
        self.white_pawn_small = pygame.transform.scale(self.white_pawn,(45,45))

        self.white_pieces_images = [self.white_pawn,  self.white_king, self.white_queen,  self.white_knight,
                                    self.white_rook, self.white_bishop]
        self.white_pieces_images_small = [self.white_pawn_small,self.white_king_small, self.white_queen_small,
                                          self.white_knight_small,
                                          self.white_rook_small,
                                          self.white_bishop_small]


        self.pieces_list_image = ['pawn', 'king', 'queen', 'knight', 'rook', 'bishop']  # Correlate al the pieces to index

        self.dark_color_rgb = (181, 136, 99)
        self.light_color_rgb = (245, 217, 181)
        self.square_dimension = 80