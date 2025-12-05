import pygame
pygame.font.init()

class GameAssets:
    """
    This class contains all the assets to initialize and start the game screen. This includes
    color, surfaces, windows etc. Changing these parameters changes how the game looks
    """
    def __init__(self):
        # Definition of the window
        self.window_height = 720
        self.window_width = 1000
        self.clock = pygame.time.Clock()
        self.tick_rate = 60
        self.window = pygame.display.set_mode((self.window_width,self.window_height))
        self.window_color = (160,160,160)

        # For the texts thar are displayed, we use the following fonts
        self.text_font_2 = pygame.font.Font(r'C:\Users\Abdi\PycharmProjects\bilder\Mom.ttf', 35)
        self.text_font_1 = pygame.font.Font(r'C:\Users\Abdi\PycharmProjects\bilder\punk_typewriter.otf',60)
        self.text_font_promotion = pygame.font.Font(r'C:\Users\Abdi\PycharmProjects\bilder\punk_typewriter.otf',40)

        # For the buttons inside showed in the end game screen
        self.button_message = 'Click here to play again'
        self.button_color = (101, 67, 33)
        self.button_surface = self.text_font_1.render(self.button_message, True, self.button_color)
        self.button_surface_rect = self.button_surface.get_rect(center=[450, 450])
        self.hover_color = 'green'
        self.history_button_message = 'Click here to show history'
        self.history_button_color = (136, 8, 8)
        self.history_button_surface = self.text_font_1.render(self.history_button_message,
                                                              True,
                                                              self.history_button_color)
        self.history_button_surface_rect = self.history_button_surface.get_rect(center=[450, 550])

        # For the button regarding the three move repetition draw.
        self.repetition_button_message = "Call Draw?"
        self.button_repetition_color = (101, 56, 19)
        self.button_repetition_surface = self.text_font_1.render(self.repetition_button_message, True,
                                                                 self.button_repetition_color)
        self.button_repetition_surface_rect = self.button_repetition_surface.get_rect(center=[750, 600])


        # for the captured screen. we will have some text.
        self.captured_surface = self.text_font_1.render('Captured pieces', True, 'Black')
        self.captured_surface_rect = self.captured_surface.get_rect(topleft = [8 * 80, 0])

        # For flashing graphical elements, and triggering start_over in end game state with two AI,
        self.flash_timer =  pygame.USEREVENT + 1  # start and stop
        pygame.time.set_timer(self.flash_timer,500)
        self.restart_timer = pygame.USEREVENT + 2  # start and sto
        pygame.time.set_timer(self.restart_timer, 5000) # wont be exact 5 seconds intervalls!
        self.history_timer = pygame.USEREVENT + 3
        pygame.time.set_timer(self.history_timer, 500)