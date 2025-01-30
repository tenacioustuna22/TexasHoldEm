import random
from typing import List, Tuple



class Deck:
    def __init__(self):
        suits = ['S', 'C', 'H', 'D']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
  
        self.cards = [(rank, suit) for suit in suits for rank in ranks]
        random.shuffle(self.cards)
        self.community = []  

    def deal_card(self) -> Tuple[str, str]:
        # Deal a single card from the deck
        return self.cards.pop() if self.cards else None
    
    def deal_flop(self) -> None:
        for _ in range(3):
            self.community.append(self.deal_card())
       
    
    def deal_turn(self) -> None:
        for _ in range(1):
            self.community.append(self.deal_card())
       
    
    def deal_river(self) -> None:
        for _ in range(2):
            self.community.append(self.deal_card())
    
    def get_community_cards(self) -> str:
        
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



    def bet(self, player: Player):
        
        if player.is_folded:
            return
        
        while True:
            try:
                amount = float(input(f'{player.name}: {player.show_hand()}, pot: {self.pot}, current bet: {self.current_bet} '))
            except ValueError:
                print("Invalid input! Please enter a number.")
                continue

            # Validation checks
            if amount == 0 and player.last_bet == self.current_bet:
                player.check()
                break
            elif amount - player.last_bet == 0:
                player.fold()
                print(f"{player.name} folds")
                return
            elif amount > player.money:
                print(f"You do not have enough money to bet {amount}, your available money is {player.money}")
            elif amount < self.current_bet and amount > 0:
                print(f"{player.name}: Not enough to match current bet ({self.current_bet}), type 0 to fold")
            elif amount > self.current_bet and amount < 2 * self.current_bet:
                print("Raise must be at least double the current bet")
            else:
                # Process valid bet
                player.update_money(-amount)
                self.pot += amount
                player.last_bet = amount
                self.current_bet = max(self.current_bet, amount)
                player.total_bet += amount
                break
    


    def additional_bet_required(self, player: Player):
        if player.is_folded:
            return
        
        if self.current_bet > player.last_bet:
            additional_amount = self.current_bet - player.last_bet
            while True:
                try:
                    amount = float(input(f'{player.name}: {player.show_hand()}, pot: {self.pot}, current bet: {self.current_bet} '))
                except ValueError:
                    print("Invalid input! Please enter a number.")
                    continue

                # Validation checks
                if amount == 0 and player.last_bet == self.current_bet:
                    player.check()
                    break
                elif amount - player.last_bet == 0:
                    player.fold()
                    print(f"{player.name} folds")
                    return
                elif amount > player.money:
                    print(f"You do not have enough money to bet {amount}, your available money is {player.money}")
                elif amount + player.last_bet < self.current_bet and amount > 0:
                    print(f"{player.name}: Not enough to match current bet ({self.current_bet}), type 0 to fold")
                elif amount + player.last_bet > self.current_bet and amount < 2 * self.current_bet:
                    print("Raise must be at least double the current bet")
                else:
                    # Process valid bet
                    player.update_money(-amount)
                    self.pot += amount
                    player.last_bet = amount
                    self.current_bet = max(self.current_bet, amount)
                    player.total_bet += amount
                    break
            if player.total_bet > self.current_bet:
                self.raise_protocol()

    


    def use_small_blind(self):
        small_blind_player = self.players[0]
        self.current_bet = self.small_blind
        # Force small blind without input prompt
        amount = min(self.small_blind, small_blind_player.money)
        small_blind_player.update_money(-amount)
        self.pot += amount
        small_blind_player.last_bet = amount
        small_blind_player.total_bet += amount

    def use_big_blind(self):
        big_blind_player = self.players[1]
        self.current_bet = self.big_blind
        # Force big blind without input prompt
        amount = min(self.big_blind, big_blind_player.money)
        big_blind_player.update_money(-amount)
        self.pot += amount
        big_blind_player.last_bet = amount
        big_blind_player.total_bet += amount

    def reset_current_bet(self):
        self.current_bet = 0.00



    def initial_betting_sequence(self):
        for player in self.players[2:]:  
            if not player.is_folded:  
                self.bet(player)
         
        for i in range(num_players):
                game.additional_bet_required(game.players[i])
        
    def post_betting_sequence(self):
        for player in self.players:
            if not player.is_folded: 
                self.bet(player)
        for i in range(num_players):
                game.additional_bet_required(game.players[i])
    


    def raise_protocol(self):
        num_players = len(self.players)

        
        last_raiser_index = None
        for i, player in enumerate(self.players):
            if player.last_bet == self.current_bet and player.last_bet != 0 and not player.is_folded: 
                last_raiser_index = i

        if last_raiser_index is None:
            return  

        
        start_index = (last_raiser_index + 1) % num_players

        for i in range(start_index, start_index + num_players - 1):  
            player = self.players[i % num_players]  

            if player.last_bet < self.current_bet and not player.is_folded:  
                self.additional_bet_required(player)

    def reset_all_players_last_bets(self):
        for player in self.players:
            player.last_bet = 0





#START 


num_players = int(input("Enter number of players: "))
game = Game(num_players)
deck = Deck()


game.use_small_blind()
game.use_big_blind()


for players in game.players:
    game.deal_cards_to_player(players, 2)


game.initial_betting_sequence()
for player in game.players:
    if not player.is_folded:
        if player.last_bet < game.current_bet:
            game.additional_bet_required(player)


if game.current_bet == game.players[1].last_bet and game.current_bet == game.big_blind:
        bet_amount = float(input(f'{game.players[1].name}: {game.players[1].show_hand()}, pot: {game.pot}, current bet: {game.current_bet}, 0 to check '))
        if bet_amount == 0:
            game.players[1].check()
        else:
            game.bet(game.players[1], bet_amount + game.players[1].last_bet)
            game.raise_protocol()   
                


deck.deal_flop()
print("Flop:", deck.get_community_cards()) 
game.reset_all_players_last_bets()
game.reset_current_bet()


game.post_betting_sequence() 
for player in game.players:
    if not player.is_folded:
        if player.last_bet < game.current_bet:
            game.additional_bet_required(player)


deck.deal_turn()
print("Community Cards:", deck.get_community_cards())
game.reset_all_players_last_bets()
game.reset_current_bet()


game.post_betting_sequence() 
for player in game.players:
    if not player.is_folded:
        if player.last_bet < game.current_bet:
            game.additional_bet_required(player)


deck.deal_river()
print("Community Cards:", deck.get_community_cards())
game.reset_all_players_last_bets()
game.reset_current_bet()


game.post_betting_sequence() 
for player in game.players:
    if not player.is_folded:
        if player.last_bet < game.current_bet:
            game.additional_bet_required(player)


