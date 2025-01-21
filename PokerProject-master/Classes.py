import random
import itertools


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + ' of ' + self.suit

class Deck:
    def __init__(self):
        suits = ['Spades', 'Clubs', 'Hearts', 'Diamonds']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack',
                 'Queen', 'King', 'Ace']
        self.cards = list('-'.join(card) for card in itertools.product(ranks,
                                                                      suits))
        self.hand = []
        self.burn_pile = []
        self.flop = []
        self.turn = []
        self.river = []
        self.community_cards = []

    def __str__(self):
        return str(self.cards)

    def shuffle(self):
        return random.shuffle(self.cards)

    def pop_card(self):
        """" i is the index of the card you wish to remove """
        return self.cards.pop()

    def update_community_cards(self):
        self.community_cards = self.flop[:] + self.turn[:] + self.river[:]

    def cards_remaining(self):
        return len(self.cards)

    def deal_hand(self):
        """ num is the number of cards to deal """

        for n in range(2):
            self.hand.append(self.pop_card())
        return self.hand

    def burn_card(self):
        self.burn_pile.append(self.pop_card())
        return self.burn_pile

    def deal_flop(self):
        for i in range(3):
            self.flop.append(self.pop_card())
            self.update_community_cards()
        return self.flop

    def deal_turn(self):
        self.turn.append(self.pop_card())
        self.update_community_cards()
        return self.turn

    def deal_river(self):
        self.river.append(self.pop_card())
        self.update_community_cards()
        return self.river



