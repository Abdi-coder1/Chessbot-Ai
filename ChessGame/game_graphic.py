import pygame

class Gamegraphic:
    """
    This class contains all the visual methods for this program,
    that includes drawing the screen and board.
    """

    def __init__(self,main_chess_asset,main_game_asset):
        self.main_chess_asset = main_chess_asset
        self.main_game_asset = main_game_asset
        self.king_in_check = False

        self.timer = 0


        self.button_message = 'Click here to play again'
        self.button_color = 'grey'
        self.button_surface = self.main_game_asset.text_font_big.render(self.button_message, True, self.button_color)
        self.button_surface_rect = self.button_surface.get_rect(center = [450,450])
        self.hover_color = 'green'

    def draw_screen(self):
        self.main_game_asset.window.fill('grey')
        pygame.display.set_caption('Chess_Bot')

    def draw_board(self):
        # Draw the board
        sd = self.main_chess_asset.square_dimension
        for i in range(0,64):
            column = i%8
            row = i//8
            location = (row,column)
            if (location[0] + location[1]) % 2 == 0:
                pygame.draw.rect(self.main_game_asset.window,self.main_chess_asset.light_color_rgb, 
                                 [column * sd, row * sd, sd, sd ])
            else:
                pygame.draw.rect(self.main_game_asset.window,self.main_chess_asset.dark_color_rgb,
                                 [column* sd, row* sd, sd, sd ])
                                                                            
            # Draw the background outside the board
        pygame.draw.rect(self.main_game_asset.window, (179,158,106),
                         [0, sd*8, self.main_game_asset.window_width,self.main_game_asset.window_height-sd*8])
        pygame.draw.rect(self.main_game_asset.window, 'gold',
                         [0, sd * 8, self.main_game_asset.window_width,
                          self.main_game_asset.window_height - sd * 8],5)
    
    
        pygame.draw.rect(self.main_game_asset.window, (179,158,106),
                    [sd * 8, 0, self.main_game_asset.window_width - sd * 8, self.main_game_asset.window_height])
        pygame.draw.rect(self.main_game_asset.window, 'silver',
                         [sd * 8, 0,  self.main_game_asset.window_width - sd * 8,self.main_game_asset.window_height],
                         5)



        #Draw instruction text
        turn_step_text_surface = self.main_game_asset.text_font_big.render(self.main_chess_asset.turn_step_text_list[
                                                          self.main_chess_asset.turn_step%4], True, 'black')
        turn_step_text_rect = turn_step_text_surface.get_rect(center=[200,680])
        self.main_game_asset.window.blit(turn_step_text_surface,turn_step_text_rect)

    def draw_pieces(self):
        sd = self.main_chess_asset.square_dimension
        for i in range(len(self.main_chess_asset.white_pieces)):
            image_index = self.main_chess_asset.pieces_list_image.index(
                self.main_chess_asset.white_pieces[i]
            )
            relevant_image = self.main_chess_asset.white_pieces_images[image_index]
            self.main_game_asset.window.blit(relevant_image,
                                    [self.main_chess_asset.white_pieces_locations[i][0]*sd + 10,
                                    self.main_chess_asset.white_pieces_locations[i][1]*sd +10]
                                    )
            if (self.main_chess_asset.turn_step == 1
                    and self.main_chess_asset.selected_piece_index == i):
                pygame.draw.rect(self.main_game_asset.window, 'red', [
                        self.main_chess_asset.white_pieces_locations[i][0]*sd,
                        self.main_chess_asset.white_pieces_locations[i][1]*sd,
                        sd,sd], 5
                                 )
        for i in range(len(self.main_chess_asset.black_pieces)):
            image_index = self.main_chess_asset.pieces_list_image.index(
                self.main_chess_asset.black_pieces[i]
            )
            relevant_image = self.main_chess_asset.black_pieces_images[image_index]
            self.main_game_asset.window.blit(relevant_image,
                                    (self.main_chess_asset.black_pieces_locations[i][0]*sd + 10,
                                    self.main_chess_asset.black_pieces_locations[i][1]*sd +10)
                                    )
            if self.main_chess_asset.turn_step == 3 and self.main_chess_asset.selected_piece_index == i:
                pygame.draw.rect(self.main_game_asset.window, 'blue', [
                    self.main_chess_asset.black_pieces_locations[i][0] * sd,
                    self.main_chess_asset.black_pieces_locations[i][1] * sd,
                    sd, sd], 5
                    )

    def draw_valid_move(self):
        if self.main_chess_asset.turn_step == 1:
            for grid_pos in self.main_chess_asset.valid_moves:
                pygame.draw.circle(self.main_game_asset.window,'red',
                                   [grid_pos[0]*self.main_chess_asset.square_dimension +\
                                    self.main_chess_asset.square_dimension/2,
                                   grid_pos[1]*self.main_chess_asset.square_dimension +\
                                    self.main_chess_asset.square_dimension/2],
                                   5)
        if self.main_chess_asset.turn_step == 3:
            for grid_pos in self.main_chess_asset.valid_moves:
                pygame.draw.circle(self.main_game_asset.window,'blue',
                                   [grid_pos[0]*self.main_chess_asset.square_dimension +\
                                       self.main_chess_asset.square_dimension/2,
                                   grid_pos[1]*self.main_chess_asset.square_dimension +\
                                    self.main_chess_asset.square_dimension/2],
                                   5)

    def draw_captured_pieces(self):
        for i in range(len(self.main_chess_asset.captured_pieces_white)):
            piece_image = self.main_chess_asset.black_pieces_images_small[self.main_chess_asset.pieces_list_image.index(
                self.main_chess_asset.captured_pieces_white[i]) ]
            self.main_game_asset.window.blit(piece_image, [
                self.main_chess_asset.square_dimension*8 + i%3 * 40, i//3 *50+10])
        for i in range(len(self.main_chess_asset.captured_pieces_black)):
            piece_image = self.main_chess_asset.white_pieces_images_small[self.main_chess_asset.pieces_list_image.index(
                self.main_chess_asset.captured_pieces_black[i]) ]
            self.main_game_asset.window.blit(piece_image,
                                             [3*40 + self.main_chess_asset.square_dimension*8 + i%3 * 40, i//3 * 50+10])

    def draw_check(self, check_state):
        white_king_index = self.main_chess_asset.white_pieces.index('king')
        black_king_index = self.main_chess_asset.black_pieces.index('king')
        sd = self.main_chess_asset.square_dimension


        if check_state[0][1] == True and check_state[0][2] == True:
            pygame.draw.rect(self.main_game_asset.window, 'black', [
                self.main_chess_asset.white_pieces_locations[white_king_index][0] * sd,
                self.main_chess_asset.white_pieces_locations[white_king_index][1] * sd,
                sd, sd], 5)
        elif check_state[0][1] == True:
            if 30< self.timer < 40:
                pygame.draw.rect(self.main_game_asset.window, 'dark red', [
                    self.main_chess_asset.white_pieces_locations[white_king_index][0] * sd,
                    self.main_chess_asset.white_pieces_locations[white_king_index][1] * sd,
                    sd, sd], 5)

                if self.timer == 39:    self.timer = 0
                else: self.timer += 1
            else:
                self.timer += 1

        if check_state[1][1] == True and check_state[1][2] == True:
            pygame.draw.rect(self.main_game_asset.window, 'black', [
                self.main_chess_asset.black_pieces_locations[black_king_index][0] * sd,
                self.main_chess_asset.black_pieces_locations[black_king_index][1] * sd,
                sd, sd], 5)

        elif check_state[1][1] == True:
            if 30 < self.timer < 40:
                pygame.draw.rect(self.main_game_asset.window, 'dark blue', [
                    self.main_chess_asset.black_pieces_locations[black_king_index][0] * sd,
                    self.main_chess_asset.black_pieces_locations[black_king_index][1] * sd,
                    sd, sd], 5)
                if self.timer == 39:    self.timer = 0
                else:   self.timer += 1
            else:
                self.timer += 1

    def draw_game_over(self,winner,click,mouse_pos):

        self.main_game_asset.window.fill((165,99,60))
        message = 'Congratualtion ' +  winner  + ' , You have won!'

        winner_text_surface = self.main_game_asset.text_font_2.render(message,True, 'black')
        winner_text_surface_rect = winner_text_surface.get_rect(center = [450,300])
        self.main_game_asset.window.blit(winner_text_surface, winner_text_surface_rect)


        self.main_game_asset.window.blit(self.button_surface,self.button_surface_rect)
        if self.button_surface_rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.main_game_asset.window,self.hover_color,[233, 418, 434, 64], 5)
            if click:
                return True
            else:
                return False
        else:
            return False

    def draw_pawn_promotion(self, promotion_state,color):
        turn_step_text_surface = self.main_game_asset.text_font_big.render(
            '{key}: promote a piece'.format(key = color), True, 'black')
        turn_step_text_rect = turn_step_text_surface.get_rect(center=[200, 680])
        lines = ['{key}, you may now '.format(key=color),
                 'select on of these ',
                 'following pieces to',
                 'upgrade the',
                 'highlighted pawn to']
        promotion_instruction_surface = [self.main_game_asset.text_font_promotion.render(line, True, 'Black')
                                         for line in lines]
        promotion_instruction_rect = [surface.get_rect(center=[770, i * 40 + 40]) for i, surface in
                                      enumerate(promotion_instruction_surface)]
        for i in range(len(promotion_instruction_surface)):
            self.main_game_asset.window.blit(promotion_instruction_surface[i], promotion_instruction_rect[i])
        pygame.draw.rect(self.main_game_asset.window, (179, 158, 106),
                         [0, self.main_chess_asset.square_dimension * 8, self.main_game_asset.window_width,
                          self.main_game_asset.window_height - self.main_chess_asset.square_dimension * 8])
        pygame.draw.rect(self.main_game_asset.window, 'gold',
                         [0, self.main_chess_asset.square_dimension * 8, self.main_game_asset.window_width,
                          self.main_game_asset.window_height - self.main_chess_asset.square_dimension * 8], 5)

        self.main_game_asset.window.blit(turn_step_text_surface, turn_step_text_rect)
        mouse_pos = pygame.mouse.get_pos()


        for i in range(2,len(self.main_chess_asset.pieces_list_image)):
            if promotion_state[2] == 'white':
                piece_image =  self.main_chess_asset.white_pieces_images_small[i]
            else: piece_image =  self.main_chess_asset.black_pieces_images_small[i]

            piece_image = pygame.transform.rotozoom(piece_image,0,1.5)
            piece_image_rect = piece_image.get_rect(topleft =  [self.main_chess_asset.square_dimension*8 + i%3 * 80,
                                                                i//3 *80+250])
            self.main_game_asset.window.blit(piece_image, piece_image_rect)
            if piece_image_rect.collidepoint(mouse_pos):
                pygame.draw.rect(self.main_game_asset.window,'gold', piece_image_rect,4)

    def draw_castling(self, selected_index,relevant_castling_state):
        """
        This functions draws a castling options when commanded, from king side or queen side
        :return:
        """
        sq = self.main_chess_asset.square_dimension
        if relevant_castling_state[0] == 'white':
            piece_position = self.main_chess_asset.white_pieces_locations[selected_index]
            if piece_position == [4,7]: # king
                if relevant_castling_state[1]:
                    pygame.draw.circle(self.main_game_asset.window, (100, 0, 0), [piece_position[0] * sq + sq / 2,
                                                                            piece_position[1] * sq + sq / 2], 5)
                    pygame.draw.circle(self.main_game_asset.window, (100, 0, 0), [(piece_position[0] - 2) * sq + sq / 2,
                                                                            piece_position[1] * sq + sq / 2], 5)
                    pygame.draw.line(self.main_game_asset.window, (100, 0, 0), [piece_position[0] * sq + sq / 2,
                                                                          piece_position[1] * sq + sq / 2],
                                     [(piece_position[0] - 2) * sq + sq / 2,
                                      piece_position[1] * sq + sq / 2], 3)

                if relevant_castling_state[2]:
                    pygame.draw.circle(self.main_game_asset.window, (100, 0, 0), [piece_position[0] * sq + sq / 2,
                                                                            piece_position[1] * sq + sq / 2], 5)
                    pygame.draw.circle(self.main_game_asset.window, (100, 0, 0), [(piece_position[0] + 2) * sq + sq / 2,
                                                                            piece_position[1] * sq + sq / 2], 5)
                    pygame.draw.line(self.main_game_asset.window, (100, 0, 0), [piece_position[0] * sq + sq / 2,
                                                                          piece_position[1] * sq + sq / 2],
                                     [(piece_position[0] + 2) * sq + sq / 2,
                                      piece_position[1] * sq + sq / 2], 3)

        if relevant_castling_state[0] == 'black':
            piece_position = self.main_chess_asset.black_pieces_locations[selected_index]
            if piece_position == [4, 0]:  # king
                if relevant_castling_state[1]:
                    pygame.draw.circle(self.main_game_asset.window, (0, 0, 100), [piece_position[0] * sq + sq / 2,
                                                                                  piece_position[1] * sq + sq / 2], 5)
                    pygame.draw.circle(self.main_game_asset.window, (0, 0, 100), [(piece_position[0] - 2) * sq + sq / 2,
                                                                                  piece_position[1] * sq + sq / 2], 5)
                    pygame.draw.line(self.main_game_asset.window, (0, 0, 100), [piece_position[0] * sq + sq / 2,
                                                                                piece_position[1] * sq + sq / 2],
                                     [(piece_position[0] - 2) * sq + sq / 2,
                                      piece_position[1] * sq + sq / 2], 3)

                if relevant_castling_state[2]:
                    pygame.draw.circle(self.main_game_asset.window, (0, 0, 100), [piece_position[0] * sq + sq / 2,
                                                                                  piece_position[1] * sq + sq / 2], 5)
                    pygame.draw.circle(self.main_game_asset.window, (0, 0, 100), [(piece_position[0] + 2) * sq + sq / 2,
                                                                                  piece_position[1] * sq + sq / 2], 5)
                    pygame.draw.line(self.main_game_asset.window, (0, 0, 100), [piece_position[0] * sq + sq / 2,
                                                                                piece_position[1] * sq + sq / 2],
                                     [(piece_position[0] + 2) * sq + sq / 2,
                                      piece_position[1] * sq + sq / 2], 3)










