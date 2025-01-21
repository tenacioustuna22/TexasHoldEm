import pygame.font
from settings import Settings

class Button():

    def __init__(self, screen, msg):
        """ Initialize button attributes """
        self.screen = screen
        self.screen_rect = screen.get_rect()
        pt_set = Settings()

        # Set the dimensions and properties of the button
        self.width, self.height = 200, 50
        self.button_color = pt_set.button_color
        self.text_color = pt_set.button_text_color
        self.font = pygame.font.SysFont(None, 48)

        # Build the buttons rect object and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.top = self.screen_rect.top + 110
        self.rect.right = self.screen_rect.right - 10

        # The button message needs to be prepped only once
        self.prep_msg(msg)


    def prep_msg(self, msg):
        """ Turn the msg into a rendered image and center on the button """
        self.msg_image = self.font.render(msg, True, self.text_color,
                                          self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center


    def draw_button(self):
        """ Draw blank button and then draw message """
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)