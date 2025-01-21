from collections import namedtuple
from settings import *
import pygame, random

CardTuple = namedtuple('Card', ['value', 'suit'])
#testing
cardvalues = [2, 3, 4, 5, 6, 7, 8, 9, "T",
  "J", # Jack
  "Q", # Queen
  "K", # King
  "A"] # Ace

cardsuits = ['C', 'D', 'H', 'S']

class Card:
    def __init__(self, input_value, input_suit):
        self.animation_start_time = pygame.time.get_ticks()
        self.animation_complete = False
        self.uuid = None
        self.position = None
        self.start_position = (0, 1080)
        self.orig_position = self.start_position
        self.data = CardTuple(value=input_value, suit=input_suit)
        self.id = f"{self.data.value}{self.data.suit}"
        self.img = f"graphics/cards/{self.id}.png"

        # Load and scale the image
        self.card_img = pygame.image.load(self.img)
        self.card_img = pygame.transform.scale(self.card_img, (200, 300))  # Resize to 100x150 pixels

        # Apply rotation (if needed)
        self.card_rotation_angle = random.uniform(-3, 3)
        self.card_img = pygame.transform.rotate(self.card_img, self.card_rotation_angle)

        # Get the bounding rectangle
        self.card_bounding_rect = self.card_img.get_bounding_rect()

        # Create a surface for the card
        self.card_surf = pygame.Surface(self.card_bounding_rect.size, pygame.SRCALPHA)

    
      # Calculate the position to blit the rotated image onto the surface
        blit_pos = (0, 0)
        self.card_surf.blit(self.card_img, blit_pos)

    # Random y value for card
        self.card_y = (P1_C1[1] - self.card_surf.get_height() // 2) + random.randint(-20, 20)

class Player:
  def __init__(self):
    self.cards = []
    
class Flop:
  def __init__(self):
    self.cards = []