import pygame

pygame.font.init()

class Gameassets:
    """
    This class contains all the assets to initialize and start the screen.
    """

    def __init__(self):
        self.window_height = 720
        self.window_width = 900
        self.clock = pygame.time.Clock()
        self.tick_rate = 60
        self.window = pygame.display.set_mode((self.window_width,self.window_height))

        self.text_font_2 = pygame.font.Font(r'C:\Users\Abdi\PycharmProjects\bilder\Mom.ttf', 35)
        self.text_font_big = pygame.font.Font(r'C:\Users\Abdi\PycharmProjects\bilder\punk_typewriter.otf',60)
        self.text_font_promotion = pygame.font.Font(r'C:\Users\Abdi\PycharmProjects\bilder\punk_typewriter.otf',40)
