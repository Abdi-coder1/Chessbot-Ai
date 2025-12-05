import pygame

class GameGraphic:
    """
    This class contains all the visual methods for this program,
    That includes drawing the screen and board, pieces and moves.
    What Exactly it should draw, is decided by the chess engine
    """
    def __init__(self,game_asset,chess_asset, board):
        # Create reference to the same asset object as elsewhere in the code.
        self.game_asset = game_asset
        self.chess_asset = chess_asset
        self.board = board

        #extra Attributes for drawing capability
        self.draw_king = False


    def draw_screen(self):
        """
        A function that draw the screen by filling the window in game asset
        with a chosen color
        :return: draws the screen
        """
        self.game_asset.window.fill(self.game_asset.window_color)
        pygame.display.set_caption('Chess_Bot')

    def draw_board(self):
        """
        A function that at every frame draw the board, with a brown/white color.
        The Board itself is a 8x8 square grid, with dimension specified in game_config.
        Additionally, it draws the prompt text and the closed of sections.
        :return: draws the board
         """
        sd = self.chess_asset.board_appearance['square_dimension']
        # Draw board logic
        for i in range(0, 64):
            column = i % 8
            row = i // 8
            location = (row, column)
            if (location[0] + location[1]) % 2 == 0:
                pygame.draw.rect(self.game_asset.window,
                                 self.chess_asset.board_appearance['light_color_rgb'],
                                 [column * sd, row * sd, sd, sd])
            else:
                pygame.draw.rect(self.game_asset.window,
                                 self.chess_asset.board_appearance['dark_color_rgb'],
                                 [column * sd, row * sd, sd, sd])

            # Draw the background underneath
        pygame.draw.rect(self.game_asset.window, (179, 158, 106),
                         [0, sd * 8, self.game_asset.window_width,
                          self.game_asset.window_height - sd * 8])
        pygame.draw.rect(self.game_asset.window, 'gold',
                         [0, sd * 8, self.game_asset.window_width,
                          self.game_asset.window_height - sd * 8], 5)
        # Draw the background to right side
        pygame.draw.rect(self.game_asset.window, (179, 158, 106),
                         [sd * 8, 0, self.game_asset.window_width - sd * 8,
                          self.game_asset.window_height])
        pygame.draw.rect(self.game_asset.window, 'silver',
                         [sd * 8, 0, self.game_asset.window_width - sd * 8,
                          self.game_asset.window_height],
                         5)

        # Draw instruction text
        turn_step_text_surface = self.game_asset.text_font_1.render(
            self.chess_asset.turn_step_text_list[
                self.chess_asset.turn_step % 4],
            True, 'black')
        turn_step_text_rect = turn_step_text_surface.get_rect(center=[200, 680])
        self.game_asset.window.blit(turn_step_text_surface, turn_step_text_rect)

    def draw_pieces(self):
        """
        This function draws all the current pieces in their exact location,
        to achieve this, it utilizes the board object.
        :return: the drawing of pieces on screen
        """
        for row in self.board.board_grid:
            for item in row:
                if item is not None:
                    if item.alive:
                        self.game_asset.window.blit(item.images['big'], item.images_rect['big'])

    def draw_piece_highlight(self):
        """
        When a piece is selected, we shall outline it, red or blue
        :return: a highlighted box around selected piece
        """
        sd = self.chess_asset.board_appearance['square_dimension']
        all_piece = [item for row in self.board.board_grid for item in row if item is not None]
        for piece in all_piece:
            if piece.selected and piece.alive:
                pygame.draw.rect(self.game_asset.window, piece.highlight_color,
                               [ piece.position[1] * sd, piece.position[0] * sd,sd, sd],
                             5)

    def draw_capture(self):
        """
        During the game, players, capture pieces,
        This function shows all the pieces that have been captured on the screen in agrid pattern
        :return:
        """
        black_pieces = [item for item in self.board.board_capture if item.color == 'white']
        white_pieces = [item for item in self.board.board_capture if item.color == 'black']
        sd = self.chess_asset.board_appearance['square_dimension']
        self.game_asset.window.blit(self.game_asset.captured_surface, self.game_asset.captured_surface_rect)
        for i in range(len(white_pieces)):
            white_pieces[i].images_rect['small'].topleft =  [
               sd *8 + i%3 * 40, i//3 * 50 + 60]
            self.game_asset.window.blit(white_pieces[i].images['small'], white_pieces[i].images_rect['small'])
        for i in range(len(black_pieces)):
            black_pieces[i].images_rect['small'].topleft =  [
               sd *8 + i%3 * 40 + 4*40, i//3 * 50 + 60]
            self.game_asset.window.blit(black_pieces[i].images['small'], black_pieces[i].images_rect['small'])



    def draw_valid_moves(self):
        """
        When a human presses a valid  piece, this function will be drawing its valid moves
        :return: circle dots along valid squares for that piece
        """
        all_piece = [item for row in self.board.board_grid for item in row if item is not None]
        sd = self.chess_asset.board_appearance['square_dimension']
        for game_piece in all_piece:
            if game_piece.selected and game_piece.alive:
                for attack_pos in game_piece.valid_moves:
                    if isinstance(game_piece, self.board.piece_classes['king']) \
                            and abs(attack_pos[1]-game_piece.position[1]) >1:
                        pass
                    else:
                        pygame.draw.circle(self.game_asset.window, game_piece.highlight_color,
                                           [attack_pos[1] * sd + sd / 2,
                                                   attack_pos[0] * sd + sd / 2],
                                            5)

    def draw_pawn_promotion(self,color):
        """
        When the game is in pawn_promotion state, we will draw the promotion screen that
        allows the player to interacte with the pieces and chose on of them
        :param color: wich side is going to promote
        :return:  Draws the promotion screen
        """
        sd = self.chess_asset.board_appearance['square_dimension']
        turn_step_text_surface = self.game_asset.text_font_2.render(
            '{key}: promote a piece'.format(key=color), True, 'black')
        turn_step_text_rect = turn_step_text_surface.get_rect(center=[250, 680])

        lines = ['{key}, you may now '.format(key=color),
                 'select on of these ',
                 'following pieces to',
                 'upgrade the',
                 'highlighted pawn to']
        promotion_instruction_surface = [self.game_asset.text_font_1.render(line, True, 'Black')
                                         for line in lines]
        promotion_instruction_rect = [surface.get_rect(center=[820, i * 40 + 40]) for i, surface in
                                      enumerate(promotion_instruction_surface)]
        for i in range(len(promotion_instruction_surface)):
            self.game_asset.window.blit(promotion_instruction_surface[i], promotion_instruction_rect[i])


        pygame.draw.rect(self.game_asset.window, (179, 158, 106),
                         [0, sd * 8, self.game_asset.window_width,
                          self.game_asset.window_height - sd* 8])
        pygame.draw.rect(self.game_asset.window, 'gold',
                         [0, sd * 8, self.game_asset.window_width,
                          self.game_asset.window_height - sd * 8], 5)
        self.game_asset.window.blit(turn_step_text_surface, turn_step_text_rect)

        #Drawing the pieces
        mouse_pos = pygame.mouse.get_pos()
        for i,image_list in enumerate(self.chess_asset.pictures[color].values()):
            if i<4: # not pawn or king
                relevant_image = image_list[0]
                relevant_image_rect = relevant_image.get_rect(topleft = (sd*8 + i%4 * 60,250))
                self.game_asset.window.blit(image_list[0],relevant_image_rect)
                if relevant_image_rect.collidepoint(mouse_pos):
                    pygame.draw.rect(self.game_asset.window, 'gold', relevant_image_rect, 3)

    def draw_castle(self):
        """
        If a castle options is avialble for the king that was just selected,
        we will draw it, so that the player may choose it.
        :return: draws the castle on screen
        """
        sq = self.chess_asset.board_appearance['square_dimension']
        king_pieces = [item for row in self.board.board_grid for item in row \
            if item is not None and isinstance(item, self.board.piece_classes['king'])]
        for king in king_pieces:
            if king.castling_state['queen_side'] and king.selected:
                pygame.draw.circle(self.game_asset.window, king.castling_color,
                                   [king.position[1] * sq + sq / 2,
                                    king.position[0] * sq + sq / 2], 5)
                pygame.draw.circle(self.game_asset.window, king.castling_color,
                                   [(king.position[1] - 2) * sq + sq / 2,
                                    king.position[0] * sq + sq / 2], 5)
                pygame.draw.line(self.game_asset.window, (0, 0, 0),
                                 [king.position[1] * sq + sq / 2,
                                  king.position[0] * sq + sq / 2],
                                 [(king.position[1] - 2) * sq + sq / 2,
                                  king.position[0] * sq + sq / 2], 3)
            elif king.castling_state['king_side'] and king.selected:
                pygame.draw.circle(self.game_asset.window, king.castling_color,
                                   [king.position[1] * sq + sq / 2,
                                    king.position[0] * sq + sq / 2], 5)
                pygame.draw.circle(self.game_asset.window, king.castling_color,
                                   [(king.position[1] + 2) * sq + sq / 2,
                                    king.position[0] * sq + sq / 2], 5)
                pygame.draw.line(self.game_asset.window, (0, 0, 0),
                                 [king.position[1] * sq + sq / 2,
                                  king.position[0] * sq + sq / 2],
                                 [(king.position[1] + 2) * sq + sq / 2,
                                  king.position[0] * sq + sq / 2], 3)

    def draw_game_over(self, winning, click = None):
        """
        When the game ends, the end game screen wil be draw, with information of
        who won. If human is involved then there is a possibility for restarting by
        pressing a button.
        :param winning:
        :param click: Graphical interface dictionary {'hover': bool, 'press': bool}
        :return:  True if button click, otherwise False
        """
        continue_game = False
        if winning == 'None':
            message = 'Game over, is\'s a draw'
        else:
            message = 'Game_over, congratulation {key}, you won!'.format(key = winning)
        self.game_asset.window.fill('grey')

        winner_text_surface = self.game_asset.text_font_2.render(message, True, 'black')
        winner_text_surface_rect = winner_text_surface.get_rect(center=[490, 300])
        self.game_asset.window.blit(winner_text_surface, winner_text_surface_rect)

        # The player may see and interact with restart button, or history button, for a new game,
        if click is not None:
            self.game_asset.window.blit(self.game_asset.button_surface, self.game_asset.button_surface_rect)
            self.game_asset.window.blit(self.game_asset.history_button_surface,
                                        self.game_asset.history_button_surface_rect)
            if click['hover'][0]:
                pygame.draw.rect(self.game_asset.window, self.game_asset.hover_color,
                                 [233, 418, 434, 64], 5)
            elif click['hover'][1]:
                pygame.draw.rect(self.game_asset.window, self.game_asset.hover_color,
                                 [233, 518, 470, 64], 5)

    def draw_king_danger(self,current_events):
        """
        When the king is in check, we will flash a red or blue square around the piece,
        in order to pull attention towards it. To accomplish this we utilize a timer set
        int the game assets, that periodically draws or dont draw a border color.
        :param current_events, a list of the current events, which may hold a timer object
        :return: A flashing effect
        """
        kings_list =[ self.board.locate(7), self.board.locate(23)]
        sd = self.chess_asset.board_appearance['square_dimension']
        for king in kings_list:
            if king.check_state['check']:
                if self.game_asset.flash_timer in [event.type for event in current_events]:
                    if not self.draw_king:
                        self.draw_king = True
                    elif self.draw_king:
                        self.draw_king = False
                if self.draw_king:
                    pygame.draw.rect(self.game_asset.window, king.highlight_color, [
                            king.position[1] * sd, king.position[0] * sd, sd, sd], 5)
    def draw_history(self,current_events,history_board):
        """

        :param index: which board state was this
        :param history_board: The specific board with the pieces included.
        :return: an interactive visual element to replay past histories.
        """
        self.draw_screen()
        self.draw_board()
        self.draw_pieces()
        self.draw_piece_highlight()
        self.draw_valid_moves()
        self.draw_castle()
        self.draw_king_danger(current_events)
        if history_board.pawn_promotion['white']['bool']:
            self.draw_pawn_promotion('white')
        elif history_board.pawn_promotion['black']['bool']:
            self.draw_pawn_promotion('black')
        else:
            self.draw_capture()

    def draw_repetition(self):
        rectangle = pygame.Rect(650,570,200,70,)
        mouse_pos =  pygame.mouse.get_pos()
        if self.game_asset.button_repetition_surface_rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.game_asset.window, "gold", rectangle,5)

        self.game_asset.window.blit(self.game_asset.button_repetition_surface,
                                    self.game_asset.button_repetition_surface_rect)





