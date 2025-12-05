import pygame
class HumanPlayer:
    """
    This is the main Human class. It handels the graphical interface,
    that allows a human to interact with the world. Its main purpose is to
     create a valid move object. To its help, it has boars registration methods
    """
    def __init__(self,chess_asset,game_asset):
        self.chess_asset = chess_asset
        self.game_asset = game_asset
        # No boards since that is frame-wise and unique over different moves.

    def board_click(self,current_events):
        """
        In order to create the graphical interface, the click function
        observes the events, and based on it determines if the user made a valid click,
        either for movement or promotion
        :param current_events; A list of the current actions since last frame
        :return A none object or the positions
        """
        for event in current_events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                coordinates = [event.pos[1], event.pos[0]] #[y,x]
                if all(c < self.chess_asset.board_appearance['square_dimension'] * 8 for c in coordinates):  # inside the board?
                    grid_coordinates =  [coordinates[0] // self.chess_asset.board_appearance['square_dimension'],
                             coordinates[1] // self.chess_asset.board_appearance['square_dimension']]
                    return grid_coordinates
        return None




    def select_piece(self,board,user_click,maneuver):
        """
        A user interface function that lets the player choose the appropriate piece for the current color.
        By pressing on a piece, we record the piece move specific data on the maneuver object
        :param board: The board object
        :param user_click: A [y,x] coordinate
        :param maneuver: the current maneuver object
        :return: Changes the maneuver object to reflect the selected piece
        """
        all_piece = [item for row in board.board_grid for item in row if item is not None]
        all_piece_positions = [piece.position for piece in all_piece]

        if user_click in all_piece_positions:

            chosen_piece = all_piece[all_piece_positions.index(user_click)]
            if (chosen_piece.color == 'white' and self.chess_asset.turn_step < 2) or \
                    (chosen_piece.color == 'black' and self.chess_asset.turn_step >= 2):
                # The user have clicked a valid piece, now we record it
                maneuver.state['color'] = chosen_piece.color
                maneuver.state['piece'] = chosen_piece
                maneuver.state['start_pos'] = chosen_piece.position
                maneuver.state['human_type'] = 'selected'
                maneuver.state['updated'] = True

    def select_move(self,board,user_click, maneuver):
        """
        A user interface function that lets the player, after having selected
        a piece, move that piece by pressing on one of their valid moves.
        param board, the sync board
        :param user_click, the coordinates [y,x]
        :param maneuver, the current maneuver robject
        :param board, the current sync_board
        :return: an updated maneuver robject, if possible
        """
        if self.chess_asset.turn_step % 2 == 1: # piece have been selected
            selected_piece = maneuver.state['piece']
            if user_click in selected_piece.valid_moves:
                capture_bool,capture_piece = board.check_capture(user_click,selected_piece) #Capture?

                # Now we update the maneuver robject with the relevant information
                maneuver.state['capture']['bool'] = capture_bool
                maneuver.state['capture']['piece'] = capture_piece
                maneuver.state['end_pos'] = user_click
                maneuver.state['human_type'] = 'moved'

                # The selected move may trigger a castling, so we account for it
                if selected_piece.__class__.__name__ == 'King':
                    if selected_piece.castling_state['queen_side'] and \
                        maneuver.state['end_pos'][1] - selected_piece.position[1] <0:

                        maneuver.state['castling']['bool'] = True
                        maneuver.state['castling']['side'] = 'queen_side'
                        maneuver.state['castling']['color'] = selected_piece.color

                    elif selected_piece.castling_state['king_side'] and \
                        maneuver.state['end_pos'][1] - selected_piece.position[1] > 0:

                        maneuver.state['castling']['bool'] = True
                        maneuver.state['castling']['side'] = 'king_side'
                        maneuver.state['castling']['color'] = selected_piece.color



    def generate_move(self,board, current_events, maneuver):
        """
        This is the main user interface for deciding on a move, however it is not
        always used. That get based on the user interaction. Its main purpose
        is to modify the Maneuver object according to the player interaction.
        :param board: The consistent board class
        :param current_events: a list of current events
        :param maneuver: a New maneuver object to be updated
        :return: A new potentially updated move object.
        """
        user_click = self.board_click(current_events)
        if user_click is not None:
            self.select_piece(board,user_click,maneuver) # User may select and record a new piece.
            self.select_move(board,user_click,maneuver)

        return maneuver

    def generate_promotion(self,current_events):
        """
        When the game ins in pawn_promotion state,
         this function is responsible for choosing a piece
        on the screen, though the user interactivity, with the mouse.
        :param current_events:  All the events happening
        :return:  Letting the player choose a piece and returning its name type
        """
        for event in current_events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                sd = self.chess_asset.board_appearance['square_dimension']
                pieces_rect_list = []
                mouse_pos = pygame.mouse.get_pos()
                pieces_name_list = ['rook', 'knight', 'bishop', 'queen']
                for i in range(0,4):
                    pieces_rect_list.append(pygame.Rect(sd*8 + i%4 * 60,250, 60, 60))

                for i in range(len(pieces_rect_list)):
                    if pieces_rect_list[i].collidepoint(mouse_pos):

                        return pieces_name_list[i]
        return None

    def restart_click(self):
        """
        When the game_over screen is activated, then this function allows interactivity with the screen.
        By recording if the player, presses the restart button or hovers over it
        :return: [bool, bool], first for hover, second press
        """
        click_info = {'hover': [False, False], 'press': False}
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        if self.game_asset.button_surface_rect.collidepoint(mouse_pos): # Hovering over button --> Highlight
            click_info['hover'][0] = True
        elif self.game_asset.history_button_surface_rect.collidepoint(mouse_pos):
            click_info['hover'][1] = True
        if mouse_pressed[0]:
            click_info['press'] = True

        return click_info

    def generate_repetition(self, current_events):
        if pygame.MOUSEBUTTONDOWN in [event.type for event in current_events]:
            mouse_pos = pygame.mouse.get_pos()
            if self.game_asset.button_repetition_surface_rect.collidepoint(mouse_pos):
                return True
        return None

