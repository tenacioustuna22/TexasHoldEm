import sys
import pygame
import cards as pt_cards
import stats as st

import re
from collections import Counter
from operator import itemgetter
from itertools import groupby

# Create an instance of the game stat counters
stat = st.GameStats()

# Define the pygame functions for display and interaction

def check_events(deal_button):
    """ Check for events in the game"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_deal_button(deal_button, mouse_x, mouse_y)

def check_deal_button(deal_button, mouse_x, mouse_y):
    """ Checks to see if the deal button is being pressed """
    if deal_button.rect.collidepoint(mouse_x, mouse_y):
            deal_cards()
            stat.phase += 1


def deal_cards():
    """ Assigns card images based on values and step in the deal """
    value_list = start_new_hand()
    if stat.phase == 0:
        stat.card_0_val = value_list[0]
        stat.card_1_val = value_list[1]
    elif stat.phase == 1:
        stat.card_2_val = value_list[2]
        stat.card_3_val = value_list[3]
        stat.card_4_val = value_list[4]
    elif stat.phase == 2:
        stat.card_5_val = value_list[5]
    elif stat.phase == 3:
        stat.card_6_val = value_list[6]
    else:
        stat.stats_reset()
        print(value_list)





def update_screen(pt_set, screen, deal_button, deck_image):
    """ For every iteration of main loop draw the screen """
    # Draw screen at every iteration of main loop
    screen.fill(pt_set.bg_color)
    # Draw Button
    deal_button.draw_button()
    # Draw Deck image (static back of deck)
    deck_image.blitme()
    # Create new instances of the card images
    card_1 = pt_cards.CardImage(screen, 1, "{}".format(stat.card_2_val))
    card_2 = pt_cards.CardImage(screen, 2, "{}".format(stat.card_3_val))
    card_3 = pt_cards.CardImage(screen, 3, "{}".format(stat.card_4_val))
    card_4 = pt_cards.CardImage(screen, 4, "{}".format(stat.card_5_val))
    card_5 = pt_cards.CardImage(screen, 5, "{}".format(stat.card_6_val))
    hand_1 = pt_cards.Hand(screen, 1, "{}".format(stat.card_0_val))
    hand_2 = pt_cards.Hand(screen, 2, "{}".format(stat.card_1_val))

    # Draw the community cards
    card_1.blitme()
    card_2.blitme()
    card_3.blitme()
    card_4.blitme()
    card_5.blitme()
    # Draw the players hand
    hand_1.blitme()
    hand_2.blitme()

    # Refresh the display
    pygame.display.flip()


# Define the card functions for manipulating the deck and hand

# local variables for card functions
total_cards = []
hand_count = 0
high_card = []

def start_new_hand():
    new_hand = pt_cards.Deck()
    new_hand.shuffle()
    hand = new_hand.deal_hand()
    new_hand.burn_card()
    flop = new_hand.deal_flop()
    new_hand.burn_card()
    turn = new_hand.deal_turn()
    new_hand.burn_card()
    river = new_hand.deal_river()
    community = new_hand.community_cards
    total_cards.append(hand + community)

    return total_cards[0]


