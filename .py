import random

class Card:
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']

    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def __str__(self):
        return f"{self.value} of {self.suit}"

class Deck:
    def __init__(self):
        self.cards = [Card(value, suit) for suit in Card.suits for value in Card.values]
        random.shuffle(self.cards)

    def deal(self):
        return self.cards.pop() if self.cards else None

class Player:
    def __init__(self, name, chips):
        self.name = name
        self.chips = chips
        self.hand = []

    def bet(self, amount):
        if amount > self.chips:
            raise ValueError("Not enough chips!")
        self.chips -= amount
        return amount

    def __str__(self):
        return f"{self.name} ({self.chips} chips)"

def evaluate_hand(hand, community_cards):
    # Simplified evaluation logic: counts pairs only.
    values = [card.value for card in hand + community_cards]
    value_counts = {v: values.count(v) for v in values}
    pairs = sum(1 for count in value_counts.values() if count == 2)
    return pairs

# Game setup
num_players = 2
starting_chips = 1000
players = [Player(f"Player {i+1}", starting_chips) for i in range(num_players)]

# Game loop
deck = Deck()
community_cards = []
pot = 0

# Deal two cards to each player
for player in players:
    player.hand = [deck.deal(), deck.deal()]

# Betting round
for player in players:
    print(f"{player.name}'s turn:")
    print(f"Hand: {[str(card) for card in player.hand]}")
    try:
        bet_amount = int(input(f"{player.name}, place your bet: "))
        pot += player.bet(bet_amount)
    except ValueError:
        print("Invalid bet, skipping turn.")

# Deal the flop (3 community cards)
community_cards.extend([deck.deal() for _ in range(3)])
print(f"Flop: {[str(card) for card in community_cards]}")

# Another betting round
for player in players:
    print(f"{player.name}'s turn:")
    try:
        bet_amount = int(input(f"{player.name}, place your bet: "))
        pot += player.bet(bet_amount)
    except ValueError:
        print("Invalid bet, skipping turn.")

# Deal the turn (1 card)
community_cards.append(deck.deal())
print(f"Turn: {[str(card) for card in community_cards]}")

# Another betting round
for player in players:
    print(f"{player.name}'s turn:")
    try:
        bet_amount = int(input(f"{player.name}, place your bet: "))
        pot += player.bet(bet_amount)
    except ValueError:
        print("Invalid bet, skipping turn.")

# Deal the river (1 card)
community_cards.append(deck.deal())
print(f"River: {[str(card) for card in community_cards]}")

# Final betting round
for player in players:
    print(f"{player.name}'s turn:")
    try:
        bet_amount = int(input(f"{player.name}, place your bet: "))
        pot += player.bet(bet_amount)
    except ValueError:
        print("Invalid bet, skipping turn.")

# Determine winner
results = {}
for player in players:
    results[player.name] = evaluate_hand(player.hand, community_cards)

winner = max(results, key=results.get)
print(f"Winner is {winner} with {results[winner]} pairs!")
print(f"Pot of {pot} chips goes to {winner}!")
