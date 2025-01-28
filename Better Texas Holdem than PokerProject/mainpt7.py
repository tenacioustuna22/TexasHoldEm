import random
from typing import List, Tuple

class Deck:
    def __init__(self):
        suits = ['S', 'C', 'H', 'D']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
  
        self.cards = [(rank, suit) for suit in suits for rank in ranks]
        random.shuffle(self.cards)
        self.community = []  # Renamed from community_cards

    def deal_card(self) -> Tuple[str, str]:
        # Deal a single card from the deck
        return self.cards.pop() if self.cards else None
    
    def deal_flop(self) -> None:
        # Deal three cards for the flop and add them to the community
        for _ in range(3):
            self.community.append(self.deal_card())
    
    def deal_turn(self) -> None:
        # Deal one card for the turn and add it to the community
        self.community.append(self.deal_card())
    
    def deal_river(self) -> None:
        # Deal one card for the river and add it to the community
        self.community.append(self.deal_card())
    
    def get_community_cards(self) -> str:
        # Return a string representation of the community cards
        return ', '.join([f"{rank}{suit}" for rank, suit in self.community])

class Player: 
    def __init__ (self, name: str, money: float = 10.0, last_bet: float = 0.0, total_bet: float = 0.0):
        self.name = name
        self.money = money
        self.hand = []
        self.is_folded = False
        self.last_bet = last_bet
        self.total_bet = total_bet

    def receive_card(self, card: Tuple[str,str]):
        self.hand.append(card)

    def show_hand(self):
        return ', '.join([f"{rank}{suit}" for rank, suit in self.hand])

    def update_money(self, amount: float):
        self.money += amount
    
    def fold(self):
        self.is_folded = True
    
    def check(self):
        pass

class Game: 
    def __init__(self, num_players: int):
        self.deck = Deck()
        self.players = []
        self.pot = 0.00
        self.current_bet = 0.00
        self.small_blind = 0.10
        self.big_blind = 0.25

        for i in range(num_players):
            name = input(f"Enter name for Player {i + 1}: ")
            self.players.append(Player(name))

    def deal_cards_to_player(self, player: Player, num_cards: int):
        for _ in range(num_cards):
            card = self.deck.deal_card()
            if card:
                player.receive_card(card)

    def bet(self, player: Player, amount: float):
        while True:
            if player.is_folded:
                return
            if amount == 0 and player.last_bet == self.current_bet:
                player.check()
                return
            if amount > player.money:
                print(f"You do not have enough money to bet {amount}, your available money is {player.money}")
            elif amount < self.current_bet and amount > 0:
                print(f"{player.name} not enough to match the current bet, type 0 to fold")
            elif amount > self.current_bet and amount < 2 * self.current_bet:
                print(f"raise must be at least double the current bet")
            elif amount == 0:
                player.fold()
                return
            else:
                player.update_money(-amount) 
                self.pot += amount - player.last_bet
                player.last_bet = amount
                self.current_bet = max(self.current_bet, amount)
                player.last_bet + amount == player.total_bet
                return
            try:
                amount = float(input(f'{player.name}, please enter a valid amount: '))
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    def reset_current_bet(self):
        self.current_bet = 0.00
    
    def use_small_blind(self):
        small_blind_player = self.players[0]
        self.current_bet = self.small_blind
        self.bet(small_blind_player, self.small_blind)
    
    def use_big_blind(self):
        big_blind_player = self.players[1]
        self.current_bet = self.big_blind
        self.bet(big_blind_player, self.big_blind)
    
    def additional_bet_required(self, player: Player):
        if self.current_bet > player.last_bet:
            additional_amount = self.current_bet - player.last_bet
            total_bet = float(input(f'{player.name}: {player.show_hand()}, pot: {self.pot}, current bet: {self.current_bet}, {additional_amount} more to play '))
            bet_amount = total_bet + player.last_bet
            self.bet(player, bet_amount)
    


num_players = int(input("Enter number of players: "))
game = Game(num_players)
deck = Deck()
game.use_small_blind()
game.use_big_blind()


for players in game.players:
    game.deal_cards_to_player(players, 2)


for i in range(2, num_players):
        bet_amount = float(input(f'{game.players[i].name}: {game.players[i].show_hand()}, pot: {game.pot}, current bet: {game.current_bet}, how much would you like to bet? '))
        game.bet(game.players[i], bet_amount)
        
    
for i in range(num_players):
        game.additional_bet_required(game.players[i])
        game.bet(game.players[i], bet_amount - game.players[i].last_bet)


if game.current_bet == game.players[1].last_bet and game.current_bet == game.big_blind:
        bet_amount = float(input(f'{game.players[1].name}: {game.players[1].show_hand()}, pot: {game.pot}, current bet: {game.current_bet}, 0 to check '))
        game.bet(game.players[i], bet_amount - game.players[i].last_bet)


deck.deal_flop()
print("Flop:", deck.get_community_cards()) 




###issue right now i think is that last_bet is being updated before the bet_amount is being changed. 

### this makes it so when updating the game.bet it is using the bet_amount - (amount - last_bet)

### in the bet class last_bet = amount, as to update it to their last bet, but because it is not the last action 
### last_bet is being updated to their current bet before the action's done



#####bet -> .25
## small blind raises to .5
##pot loses 35 cents
## raises to 50 cents, amount to cover the call 15 cents, thus 15 - 50 = -35