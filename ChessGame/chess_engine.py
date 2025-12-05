import pygame
from sys import exit
import copy
from Config import AiAssets,ChessAssets,GameAssets
from Player import HumanPlayer,AiPlayer
from .game_graphic import GameGraphic
from .board import Board
from .maneuver import Maneuver
from .initial import Initial



class ChessEngine:
    """
    The chess engine is the main driver of the game, by using the board and pieces
    for representation a manipulation, the player for maneuver decision and lastly
    the game_graphic for drawing, it drives the game forward.
    """
    player_class = {'human': HumanPlayer,
                       'ai': AiPlayer}

    def __init__(self,player_white, player_black):
        """
        :param player_white: a string, human och AI
        :param player_black:  A string human or AI
        """
        # The engine have access to three unique and consistent assets
        self.game_asset = GameAssets()
        self.chess_asset = ChessAssets()
        self.ai_asset = AiAssets()

        # For execution of its functions it needs a board and a graphical unit, The board have the pieces
        self.initial = Initial(random = True)
        self.board = Board(game_asset = self.game_asset,chess_asset = self.chess_asset,
                           board_id = 0,initial=self.initial)

        self.graphic = GameGraphic(self.game_asset, self.chess_asset, self.board)

        # For human players, they need consistent objects over multiple frames
        self.sync_board = self.board.copy_board()
        self.current_maneuver = Maneuver()

        # For detection and decisions of moves, it needs two player, IE Human or Ai. Each with different assets
        self.player_asset = {'human': [self.chess_asset, self.game_asset],
                        'ai': [self.chess_asset,self.ai_asset]}
        self.players = {'white': ChessEngine.player_class[player_white](*self.player_asset[player_white]),
                        'black': ChessEngine.player_class[player_black](*self.player_asset[player_black])}

    @staticmethod
    def observe_events():
        """
        Based on the current events on the screen, triggerd by the user,
        record and return them
        :return: A dictionary with relevant and useful events
        """
        current_events = pygame.event.get()
        return current_events
    @staticmethod
    def quit_game(current_events):
        """
        Based on the current events, does the user want to end the game?
        Triggers if the red cross is clicked.
        :param current_events: a list or dict of the actions since last frame.
        :return: terminates the screen fully
        """
        for event in current_events:
            if event.type == pygame.QUIT:
                exit()

    # main game functions
    def run_game(self,current_events):
        """
        This is the main game function, that starts the game process, when commanded
        by the main function. The flow has three stages; play game, play pawn promotion
        end game. This functions commands the first two, by checking the board fpr promotion.
        :return: Runs the game.
        """

        if self.board.pawn_promotion['white']['bool'] or \
                self.board.pawn_promotion['black']['bool']:  # pawn_promotion state
            self.draw_game(current_events, pawn_promotion=True)
            self.play_pawn_promotion(current_events)
        elif self.board.repetition_bool: # The moves draw possible
            self.draw_game(current_events, repetition = True)
            self.play_repetition(current_events)

        else:
            self.play_game(current_events)
            self.draw_game(current_events)
            print(self.board.repetition_bool)

    def draw_game(self, current_events, pawn_promotion = False, repetition = False):
        """
        For every frame this function will draw the screen, by commanding
        the graphic object. What will be drawn depends on the boards state
        :param pawn_promotion, is it time for a pawn_promotion?
        :param current_events: what has happened on the screen, used in king danger
        :param repetition, should a button for calling draw appear?
        :return: Draws the screen according to game and board state
        """
        self.graphic.draw_screen()
        self.graphic.draw_board()
        self.graphic.draw_pieces()
        self.graphic.draw_piece_highlight()
        self.graphic.draw_valid_moves()
        self.graphic.draw_castle()
        self.graphic.draw_king_danger(current_events)

        if pawn_promotion:
            if self.board.pawn_promotion['white']['bool']:
                self.graphic.draw_pawn_promotion('white')
            else:
                self.graphic.draw_pawn_promotion('black')
        else:
            self.graphic.draw_capture()

        if repetition: # Display the draw button for human, it's ok for AI by the way.
             self.graphic.draw_repetition()
    def play_game(self, current_events):
        if self.chess_asset.turn_step <2: # Whites turn
            current_player = self.players['white']
        else: # Black turn
            current_player = self.players['black']

        # Regardless of Ai or player, take the information and return a move
        if isinstance(current_player,HumanPlayer):
            maneuver_object = current_player.generate_move(self.sync_board, current_events, self.current_maneuver)
        else:
            maneuver_object = current_player.generate_move(self.board.copy_board(), current_events, Maneuver())

        """ 
        Since the maneuver generation for Ai and Human are fundamentally different,
        we will separate the logic in two streams
        """

        if isinstance(current_player,HumanPlayer):
            # For human player, the maneuver object have three versions, empty, selected, and moved.
            if maneuver_object.state['updated'] == True and \
                    maneuver_object.state['human_type'] == 'selected': # new piece
                selected_piece = self.board.sync_board_match_piece(maneuver_object.state['piece'])
                self.board.apply_piece_select(selected_piece)
                if self.chess_asset.turn_step == 0:
                    self.chess_asset.turn_step = 1
                elif self.chess_asset.turn_step == 2:
                    self.chess_asset.turn_step = 3

            elif maneuver_object.state['updated'] == True and \
                    maneuver_object.state['human_type'] == 'moved': # movement!
                self.apply_maneuver(maneuver_object)

                #-------------------------------------
                """Regardless of AI or human choices, a move has potentially been made and applied.
                the following cold changes the relevant parameters of the boards ans sets up for next round
                """
                self.board.board_options = self.board.check_board_options(self.board.board_grid)

                # Adding special rules
                self.board.check_enpassant(self.board.locate(locate_id = maneuver_object.state['piece'].id))
                self.board.check_pawn_promotion()
                self.board.check_castling()

                # Handling check_mate
                self.board.check_mate()
                self.board.impending_check()
                # Setting upp next game
                self.current_maneuver = Maneuver()
                self.syncing_board()
                self.chess_asset.turn_step +=1
                self.chess_asset.turn_step %= 4
                self.board.record_board_history()
                self.board.repetition_eval()

    # noinspection PyUnboundLocalVariable
    def play_pawn_promotion(self,current_events):
        """
        In addition to the regular game, the state of pawn promotion is
        also possible. This function executes this rule for AI and human.
        :param current_events: what is currently happening on screen.
        :return:
        """
        if self.chess_asset.turn_step <2: # Whites turn
            current_player = self.players['white']
            promotion_pawn = self.board.pawn_promotion['black']['change_piece']
        else: # Black turn
            current_player = self.players['black']
            promotion_pawn = self.board.pawn_promotion['white']['change_piece']
        """
       since the program flow for humans and ai are fundamentally diffrent. Realise that
       the intendent piece to be promoted to takes time to decide. 
       """
        if isinstance(current_player, HumanPlayer):
            piece_name = current_player.generate_promotion(current_events) # Humans
        elif isinstance(current_player, AiPlayer):
            piece_name = current_player.generate_promotion(self.board.copy_board(), current_events)

        if piece_name is not None: # A piece to promote to has been chosen.
            # create and replace the piece
            new_piece = Board.piece_classes[piece_name](
                piece_color=promotion_pawn.color, piece_location=promotion_pawn.position,
                piece_image_list=self.chess_asset.pictures[promotion_pawn.color][piece_name],
                piece_id=promotion_pawn.id, chess_asset=self.chess_asset,
                game_asset=self.game_asset
            )
            new_piece.history = copy.deepcopy(promotion_pawn.history)
            new_piece.selected = False
            self.board.board_grid[promotion_pawn.position[0]][promotion_pawn.position[1]] = new_piece
            self.board.board_options = self.board.check_board_options(self.board.board_grid)
            promotion_pawn.promotion = False

            self.board.check_mate()
            self.board.impending_check()
            self.current_maneuver = Maneuver()
            self.syncing_board()
            self.board.pawn_promotion = {
                        'white': {'bool': False,
                                    'change_piece': None},
                        'black': {'bool': False,
                                    'change_piece': None,}
                                }
            self.board.record_board_history()
    def run_game_over(self, winning, current_events):
        """
        When the game ends, we will display the results of the game, and an option to restart
         For humans its through interactivity, and AI is a timer
        :param winning: who just won the match, white or black, or was it a draw.
        :param current_events; a list of the current events, used for AI restart
        :return: the return screen, and the options of restarting
        """
        restart,history = False,False
        if isinstance(self.players['white'], self.player_class['ai']) and \
                isinstance(self.players['black'], self.player_class['ai']):
            self.graphic.draw_game_over(winning)
            if self.game_asset.restart_timer in [event.type for event in current_events]:
                restart = True  # Can be changed to share history

        else:   # When human involved, then graphical interface is used.
            for player in self.players.values():
                if isinstance(player, ChessEngine.player_class['human']):
                    human_player = player
            # noinspection PyUnboundLocalVariable
            click_info = human_player.restart_click()
            self.graphic.draw_game_over(winning, click = click_info)
            if click_info['press']:
                if click_info['hover'][0]:
                    restart = True
                elif click_info['hover'][1]:
                    history = True
        return restart,history

    def play_repetition(self,current_events):
        """ 
        During the games play, the same board position has occurred 3 times,
        therefore the current layer, human or AI gets a chance to call a draw
        :param current_events: What's happening on the screen currently
        :return: A modification of the Board end state
        """

        if self.chess_asset.turn_step<2:
            current_player = self.players['white']
        else:
            current_player = self.players['black']

        """
        Here it becomes a split between Ai: instant decision or human
        frame dependent decision.
        """
        if isinstance(current_player, HumanPlayer):
            repetition_bool = current_player.generate_repetition(current_events)
        else:
            repetition_bool = current_player.generate_repetition(self.board.copy_board())

        # Regardless of human or Ai, lets apply the potential change.
        if repetition_bool is not None:
            if repetition_bool:
                self.board.board_end_state['patt'] = True
            else:
                self.board.board_end_state = False
    def check_winner(self):
        """
        After the game is played, then this functions will use
        the board to determine who has won. and return that information.
        :return: run, should the game continue, bool
        :return, winner, who has won, black, white or none, str
        """
        run = True
        winner= None

        if self.board.board_end_state['patt']:
            winner = 'None'
            run = False
        elif self.board.board_end_state['white']:
            winner = 'black'
            run = False
        elif self.board.board_end_state['black']:
            winner = 'white'
            run = False

        return winner, run





   # side functions for the game
    def apply_maneuver(self,maneuver):
        """
        Regardless, if the human or AI crated the maneuver robject, lets apply it,
        :param maneuver: The maneuver object filled with move information,
        :return:  changes the game board state
        """
        selected_piece = self.board.sync_board_match_piece(maneuver.state['piece'])
        if maneuver.state['capture']['bool']: # piece was captured
            captured_piece = self.board.sync_board_match_piece(maneuver.state['capture']['piece'])
            self.board.apply_capture(captured_piece)

        #application of move may be a casting, so check for that first.
        if maneuver.state['castling']['bool']: # tome for castling
            self.board.apply_castling(selected_piece, maneuver.state['castling']['side'])
            selected_piece.record_history(selected_piece.position)

            # now record history for the rook
            if maneuver.state['castling']['side'] == 'king_side':
                rook_piece = self.board.locate_piece_pos([selected_piece.position[0],
                                                          selected_piece.position[1]-1])
                rook_piece.record_history(rook_piece.position)
            elif maneuver.state['castling']['side'] == 'queen_side':
                rook_piece = self.board.locate_piece_pos([selected_piece.position[0],
                                                          selected_piece.position[1]+1])
                rook_piece.record_history(rook_piece.position)

        else: # it is a regular move.
            self.board.apply_move(selected_piece, maneuver.state['end_pos'])
            selected_piece.record_history(selected_piece.position)
        selected_piece.selected = False
    def syncing_board(self):
        """
        When a change to the board have been made, we will copy it,
        and sync it with the players board
        :return:
        """
        self.sync_board= self.board.copy_board()


    def show_history(self,current_events):
        """
        Upon completion of the board, this function will replay the
        game just played, so that we may observe tactics
        :param current_events: includes the timer for history
        :return:
        """
        if self.game_asset.history_timer in [event.type for event in current_events]: # change the board
            if not self.board.board_history_timer == \
                len(self.board.board_history)-1: # it has  not already reached maximum
                self.board.board_history_timer +=1
                self.graphic.board = self.board.board_history[self.board.board_history_timer]
            else:
                self.board.board_history_timer +=1
        self.graphic.draw_history(current_events,history_board=self.graphic.board)

        if len(self.board.board_history) == self.board.board_history_timer:
            history=False
            self.board.board_history_timer = 0
        else:
            history = True
        return history
