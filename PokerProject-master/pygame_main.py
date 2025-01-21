import pygame
from settings import Settings
from button import Button
import cards as pt_cards
import game_functions as gf



def run_game():
    # Import the settings from the Settings class
    pt_set = Settings()
    screen_width = pt_set.screen_width
    screen_height = pt_set.screen_height
    caption = pt_set.caption

    # Initialize the game and draw the game window
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption(caption)

    # Initialize the objects within the window
    deal_button = Button(screen, "Deal")
    deck_image = pt_cards.DeckImage(screen)


    # Start main game loop
    while True:
        gf.check_events(deal_button)
        gf.update_screen(pt_set, screen, deal_button, deck_image)



run_game()