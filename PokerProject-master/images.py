import pygame

class DeckImage():

    def __init__(self, screen):
        """ Initialize deck image attributes """
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.image = pygame.image.load('images/deck.bmp')
        self.rect = self.image.get_rect()

        # Place the deck at the top right
        self.rect.right = self.screen_rect.right - 55
        self.rect.top = self.screen_rect.top + 10


    def blitme(self):
        """ Draw the deck  """
        self.screen.blit(self.image, self.rect)


class CardBack():


    def __init__(self, screen, card_num, card):
        """ Initialize card back attributes """
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.image = pygame.image.load('images/{}.bmp'.format(str(card)))
        self.rect = self.image.get_rect()

        # Place 1st card of the table at the top left
        self.rect.left = self.rect.width * card_num
        self.rect.top = self.rect.width

        # Store the cards position
        self.x = float(self.rect.x)


    def blitme(self):
        """ Draw the card """
        self.screen.blit(self.image, self.rect)


class Hand():


    def __init__(self, screen, card_num, card):
        """ Initialize card back attributes """
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.image = pygame.image.load('images/{}.bmp'.format(str(card)))
        self.rect = self.image.get_rect()

        # Place 1st card of the table at the top left
        self.rect.left = self.rect.width * card_num
        self.rect.bottom = self.screen_rect.bottom - 10

        # Store the cards position
        self.x = float(self.rect.x)


    def blitme(self):
        """ Draw the card """
        self.screen.blit(self.image, self.rect)



