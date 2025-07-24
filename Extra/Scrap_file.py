import pygame.image

class ChessAssets:
    """
    This Class contains all the assets needed to start and play the chess game, that includes pictures,
    starting positions, board configurations, and starting turn.
    """
    def __init__(self):
        # The setup starts with defining the pieces and their starting location for respective player
        self.white_start_pieces =  {'rook':[[0,7], [7,7]] , 'knight':[[1,7], [6,7]], 'bishop':[[2,7], [5,7]],
                                    'queen':[3,7], 'king':[4,7],
                                    'pawn': [[0,6], [1,6], [2,6], [3,6], [4,6], [5,6], [6,6], [7,6]],
                                    }
        self.black_start_pieces = {'rook':[[0,0], [7,0]] , 'knight':[[1,0], [6,0]], 'bishop':[[2,0], [5,0]],
                                    'queen':[3,0], 'king':[4,0],
                                    'pawn': [[0,1], [1,1], [2,1], [3,1], [4,1], [5,1], [6,1], [7,1]],
                                    }

        # This dictates the text that will get displayed.
        self.turn_step = 0
        self.turn_step_text_list = {0:'White: Select a piece', 1:'White: Move that piece',
                                    2:'Black: select a piece', 3:'Black: Move that piece'}

        # Now we will import all the relevant pictures. The big is for the game, and the small for the captured.
        # Black
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

        #--------------------
        # white
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
        #--------------------------------------
        # Now lets attach the pictures to the piece types

        self.white_pictures = {'rook': [self.white_rook, self.white_rook_small],
                               'knight': [self.white_knight, self.white_knight_small],
                               'bishop': [self.white_bishop, self.white_bishop_small],
                               'queen': [self.white_queen, self.white_queen_small],
                               'king': [self.white_king,self.white_king_small],
                               'pawn': [self.white_pawn, self.white_pawn_small]}
        self.black_pictures = {'rook': [self.black_rook, self.black_rook_small],
                               'knight': [self.black_knight, self.black_knight_small],
                               'bishop': [self.black_bishop, self.black_bishop_small],
                               'queen': [self.black_queen, self.black_queen_small],
                               'king': [self.black_king, self.black_king_small],
                               'pawn': [self.black_pawn, self.black_pawn_small]}

        # these will dictate the appearance of the board.
        self.dark_board_color_rgb = (181, 136, 99)
        self.light_board_color_rgb = (245, 217, 181)
        self.square_dimension = 80




import pygame

pygame.font.init()

class GameAssets:
    """
    This class contains all the assets to initialize and start the game screen.
    """
    def __init__(self):
        self.window_height = 720
        self.window_width = 900
        self.clock = pygame.time.Clock()
        self.tick_rate = 60
        self.window = pygame.display.set_mode((self.window_width,self.window_height))

        # For the texts thar are displayed, we ude the following fonts
        self.text_font_2 = pygame.font.Font(r'C:\Users\Abdi\PycharmProjects\bilder\Mom.ttf', 35)
        self.text_font_1 = pygame.font.Font(r'C:\Users\Abdi\PycharmProjects\bilder\punk_typewriter.otf',60)
        self.text_font_promotion = pygame.font.Font(r'C:\Users\Abdi\PycharmProjects\bilder\punk_typewriter.otf',40)

from Config.chess_config import ChessAssets
from Config.game_config import GameAssets
