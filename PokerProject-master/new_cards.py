import random
import itertools


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

class Deck:
    def __init__(self):
        suits = ['Spades', 'Clubs', 'Hearts', 'Diamonds']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack',
                 'Queen', 'King', 'Ace']
        self.cards = list(''.join(card) for card in itertools.product(ranks,
                                                                      suits))

    def __str__(self):
        return str(self.cards)


newdeck = Deck()

print(newdeck)