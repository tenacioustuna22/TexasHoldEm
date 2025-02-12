import random
from typing import List, Tuple
from itertools import combinations
from collections import Counter



def main():
    # 1) Ask how many players
        num_players = int(input("Enter number of players: "))
        game = Game(num_players)

        while True:
            
            # 3) Play that round
            game.play_one_round()
            
            # 4) Optional: If you want to remove busted players (money <= 0)
            #    or end game if only 1 remains:
            busted = [p for p in game.players if p.money <= 0]
            for p in busted:
                print(f"{p.name} is out of money and removed from the game.")
            game.players = [p for p in game.players if p.money > 0]
            
            if len(game.players) < 2:
                print("Not enough players to continue. Game over.")
                break

            # 5) Ask if the table wants another round
            cont = input("Would you like to keep playing? (y/n): ")
            if cont.lower() != 'y':
                print("Thanks for playing!")
                break


RANK_VALUE = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
    '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14
}

def evaluate_5card_hand_detailed(cards: List[Tuple[str, str]]) -> Tuple[int, List[int]]:
    """
    Evaluate exactly 5 cards. Return (category, tiebreakers).
    
    category is an int in [1..9], where lower is better:
        1 = Straight Flush
        2 = Four of a Kind
        3 = Full House
        4 = Flush
        5 = Straight
        6 = Three of a Kind
        7 = Two Pair
        8 = One Pair
        9 = High Card
    
    tiebreakers is a list of integers (descending significance),
    e.g. for a Full House: [rank_of_trips, rank_of_pair].
    For a Flush or High Card: sorted ranks descending, etc.
    
    We compare two hands by:
      1. category ascending (1 is best)
      2. if category ties, compare tiebreakers lexicographically, where bigger is better.
    """
    rank_vals = [RANK_VALUE[r] for (r, s) in cards]
    suits = [s for (r, s) in cards]

    rank_vals.sort(reverse=True)
    freq = Counter(rank_vals)  # e.g. {14:4, 9:1} for four Aces
    counts_desc = sorted(freq.values(), reverse=True)
    
    # Check for flush
    is_flush = (len(set(suits)) == 1)

    # Check for straight (including special A-2-3-4-5)
    def is_consecutive(vals: List[int]) -> bool:
        return all(vals[i] == vals[i+1] + 1 for i in range(len(vals)-1))
    is_straight = is_consecutive(rank_vals)
    
    # Special case: A-2-3-4-5 => treat top card as 5
    if not is_straight and set(rank_vals) == {14, 5, 4, 3, 2}:
        is_straight = True
    
    if is_straight:
        # The "top" card in a normal straight is rank_vals[0].
        # But for A-2-3-4-5, we treat top_straight=5
        if set(rank_vals) == {14, 5, 4, 3, 2}:
            top_straight = 5
        else:
            top_straight = rank_vals[0]

    # Sort freq by (count DESC, rank_val DESC)
    freq_sorted = sorted(freq.items(), key=lambda x: (x[1], x[0]), reverse=True)
    
    # 1) Straight Flush
    if is_straight and is_flush:
        return (1, [top_straight])
    
    # 2) Four of a Kind
    if counts_desc[0] == 4:
        # freq_sorted[0] => (rank_of_quads, 4)
        # freq_sorted[1] => (kicker, 1)
        rank_of_quads = freq_sorted[0][0]
        kicker = freq_sorted[1][0]
        return (2, [rank_of_quads, kicker])
    
    # 3) Full House (3 + 2)
    if counts_desc == [3, 2]:
        rank_of_trips = freq_sorted[0][0]
        rank_of_pair = freq_sorted[1][0]
        return (3, [rank_of_trips, rank_of_pair])
    
    # 4) Flush
    if is_flush:
        # Just compare the five ranks in descending order
        return (4, rank_vals)
    
    # 5) Straight
    if is_straight:
        return (5, [top_straight])
    
    # 6) Three of a Kind
    if counts_desc[0] == 3:
        # freq_sorted[0] => (trip_rank, 3)
        trip_rank = freq_sorted[0][0]
        # The other two are kickers
        kickers = sorted((r for (r, c) in freq_sorted[1:] for _ in range(c)), reverse=True)
        return (6, [trip_rank] + kickers)
    
    # 7) Two Pair
    if len(counts_desc) >= 2 and counts_desc[0] == 2 and counts_desc[1] == 2:
        # freq_sorted[0] => (highPair, 2)
        # freq_sorted[1] => (lowPair, 2)
        # freq_sorted[2] => (kicker, 1)
        high_pair = freq_sorted[0][0]
        low_pair = freq_sorted[1][0]
        kicker = freq_sorted[2][0]
        return (7, [high_pair, low_pair, kicker])
    
    # 8) One Pair
    if counts_desc[0] == 2:
        pair_rank = freq_sorted[0][0]
        # The rest are kickers
        kickers = sorted((r for (r, c) in freq_sorted[1:] for _ in range(c)), reverse=True)
        return (8, [pair_rank] + kickers)
    
    # 9) High Card
    return (9, rank_vals)


def evaluate_7card_hand_detailed(seven_cards: List[Tuple[str, str]]) -> Tuple[int, List[int]]:
    """
    Evaluate 7 cards (2 hole + 5 community) by picking the best 5-card subset.
    Returns (category, tiebreakers).
    """
    best = (9, [-1, -1, -1, -1, -1])  # something "worst" by default
    for combo in combinations(seven_cards, 5):
        cat, tie = evaluate_5card_hand_detailed(list(combo))
        # Compare to current best:
        #  - cat ascending
        #  - if cat ties, tiebreak descending
        if cat < best[0]:
            best = (cat, tie)
        elif cat == best[0] and tie > best[1]:
            best = (cat, tie)
    return best


# -----------------------------------------
# 2) Deck, Player, and Game classes
# -----------------------------------------

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
        self.community.append(self.deal_card())
    
    def deal_river(self) -> None:
        self.community.append(self.deal_card())
    
    def get_community_cards(self) -> str:
        return ', '.join([f"{rank}{suit}" for rank, suit in self.community])


class Player: 
    def __init__(self, name: str, money: float = 10.0, last_bet: float = 0.0,
                 beginning_money: float = 0.0, all_in_pot_amount: float = 0.0, all_in_difference: float = 0.0):
        self.name = name
        self.money = money
        self.hand = []
        self.is_folded = False
        self.last_bet = last_bet
        self.is_all_in = False
        self.beginning_money = beginning_money
        self.winner = []
        self.all_in_pot_amount = all_in_pot_amount
        self.all_in_difference = all_in_difference
        

    def receive_card(self, card: Tuple[str, str]):
        self.hand.append(card)

    def show_hand(self):
        return ', '.join([f"{rank}{suit}" for rank, suit in self.hand])

    def update_money(self, amount: float):
        self.money += amount
        self.money = round(self.money, 2)
    
    def fold(self):
        self.is_folded = True
    
    def check(self):
        pass

    def all_in(self):
        self.is_all_in = True
        self.is_folded = True
      # locks them out of betting actions
        
    


        
    def update_beginning_money(self):
        self.beginning_money = self.money


class Game: 
    def __init__(self, num_players: int):
        self.deck = Deck()
        self.players = []
        self.pot = 0.00
        self.current_bet = 0.00
        self.small_blind = 0.10
        self.big_blind = 0.25
        self.winner_determined = False
        

        for i in range(num_players):
            name = input(f"Enter name for Player {i + 1}: ")
            self.players.append(Player(name))

    def deal_cards_to_player(self, player: Player, num_cards: int):
        for _ in range(num_cards):
            card = self.deck.deal_card()
            if card:
                player.receive_card(card)

    def bet(self, player: Player, amount: float) -> bool:
        """
        Attempts to place a bet for 'player' in the amount 'amount'.
        Returns True if bet was successful (or fold/check/all-in).
        Returns False if invalid and we should re-prompt.
        """
        try:
            amount = float(amount)
        except ValueError:
            print("Invalid input! Please enter a valid numeric amount.")
            return False
        
        while True:
            if player.is_folded:
                return True  # no action if already folded
            
            # Checking
            if amount == player.last_bet and player.last_bet == self.current_bet:
                player.check()
                print(f"{player.name} checks")
                return True
            
            # Folding (entering 0 when you owe something)
            elif amount - player.last_bet == 0:
                player.fold()
                print(f"{player.name} folds")
                return True
            
            # All-in
            elif amount - player.last_bet == player.money:
                print(f'{player.name} is all in!')
                player.update_money(-amount + player.last_bet)
                self.pot += (amount - player.last_bet)
                self.pot = round(self.pot, 2)
                player.last_bet = round(amount, 2)
                self.current_bet = max(self.current_bet, amount)
                self.current_bet = round(self.current_bet, 2)
                player.all_in()
                return True
            
            # Invalid negative
            elif amount < 0:
                print (f'{player.name}, negative amounts not allowed')
                return False
            
            # Not enough money
            elif amount - player.last_bet > player.money:
                print(f"You do not have enough money to bet {round(amount, 2)}, your available money is {player.money}")
                return False
            
            # If bet < current bet (but > 0), not matching
            elif amount < self.current_bet and amount > 0:
                print(f"{player.name}, not enough to match the current bet. Type 0 to fold.")
                return False
            
            # Must raise at least double the current bet
            elif amount > self.current_bet and amount < 2 * self.current_bet:
                print("Raise must be at least double the current bet.")
                return False

            # Otherwise, a valid bet or valid raise
            player.update_money(-amount + player.last_bet) 
            self.pot += (amount - player.last_bet)
            self.pot = round(self.pot, 2)
            player.last_bet = amount
            self.current_bet = max(self.current_bet, amount)
            return True
    
    def calculate_all_in_amounts(self):
        for player in self.players:
            if player.is_all_in:
                player.all_in_pot_amount = self.pot
                for p in self.players:
                    if player.last_bet < p.last_bet:
                        if player is p:
                            continue
                        player.all_in_difference += p.last_bet - player.last_bet 
                player.all_in_pot_amount -= player.all_in_difference

    def betting_sequence(self, player: Player):
        """
        Prompt 'player' for a bet/call/fold/check action when needed.
        """
        additional_amount = self.current_bet - player.last_bet
        old_current_bet = self.current_bet
        
        # If they already matched the bet, don't ask again
        if player.last_bet == self.current_bet and self.current_bet != 0:
            return
        
        while True:
            try:
                prompt_msg = (f'{player.name}: {player.show_hand()}, money: {round(player.money, 2)}, '
                              f'pot: {round(self.pot, 2)}, current bet: {round(self.current_bet, 2)}, '
                              f'{round(additional_amount, 2)} more to call -> ')
                total_bet_input = float(input(prompt_msg))
            except ValueError:
                print("Invalid input. Please enter a valid number.")
                continue
            
            bet_amount = total_bet_input + player.last_bet
            bet_success = self.bet(player, bet_amount)
            if bet_success:
                # If someone raised above old_current_bet, we do raise_protocol
                if old_current_bet < self.current_bet:
                    self.raise_protocol()
                break
            else:
                continue

    def reset_current_bet(self):
        self.current_bet = 0.00

    def use_small_blind(self):
        # Player[0] => small blind
        small_blind_player = self.players[0]
        self.current_bet = self.small_blind
        self.bet(small_blind_player, self.small_blind)
    
    def use_big_blind(self):
        # Player[1] => big blind
        big_blind_player = self.players[1]
        self.current_bet = self.big_blind
        self.bet(big_blind_player, self.big_blind)

    def initial_betting_sequence(self):
        # Each player after the blinds
        for player in self.players[2:]:
            while True:
                try:
                    msg = (f'{player.name}: {player.show_hand()}, money: {round(player.money, 2)}, '
                           f'pot: {round(self.pot, 2)}, current bet: {round(self.current_bet, 2)}, '
                           f'how much would you like to bet? ')
                    bet_amount = float(input(msg))
                except ValueError:
                    print("Invalid input. Please enter a valid number.")
                    continue
                bet_success = self.bet(player, bet_amount)
                if bet_success:
                    break
                else:
                    continue
        
        # Force each player to match or fold if the bet changed
        for i in range(len(self.players)):
            self.additional_bet_required(self.players[i])
        
        # Now specifically let the big blind (player[1]) act again if everyone else is done
        if (self.current_bet == self.players[1].last_bet == self.big_blind):
            old_current_bet = self.current_bet
            while True:
                try:
                    msg = (f'{self.players[1].name}: {self.players[1].show_hand()}, money: {round(self.players[1].money, 2)}, '
                           f'pot: {round(self.pot, 2)}, current bet: {round(self.current_bet, 2)}, 0 to check -> ')
                    total_bet = float(input(msg))
                except ValueError:
                    print("Invalid input. Please enter a valid number.")
                    continue
                bet_amount = total_bet + self.players[1].last_bet
                bet_success = self.bet(self.players[1], bet_amount)
                if bet_success:
                    if old_current_bet < self.current_bet:
                        self.raise_protocol()
                    break
                else:
                    continue

    def post_betting_sequence(self):
        # Another round of betting for each non-folded player
        for player in self.players:
            if not player.is_folded:
                self.betting_sequence(player)

    def additional_bet_required(self, player: Player):
        # If player hasn't matched current_bet yet, ask them
        if player.is_folded:
            return
        if self.current_bet > player.last_bet:
            self.betting_sequence(player)

    def raise_protocol(self):
    #After a raise, each player (except the raiser) must have the chance to call or raise again.
        num_players = len(self.players)

        
        last_raiser_index = None
        for i, player in enumerate(self.players):
            if player.last_bet == self.current_bet and player.last_bet != 0:
                last_raiser_index = i

        if last_raiser_index is None:
            return  

        
        start_index = (last_raiser_index + 1) % num_players

        for i in range(start_index, start_index + num_players - 1):  
            player = self.players[i % num_players]  

            if player.last_bet < self.current_bet: 
                self.additional_bet_required(player)

    def reset_all_players_last_bets(self):
        for player in self.players:
            player.last_bet = 0

    def start_new_round(self):
        self.deck = Deck()
        self.reset_all_players_last_bets()
        self.reset_current_bet()
        self.pot = 0
        self.winner = []
        self.winner_determined = False
        
        for player in self.players:
            player.hand.clear()
            player.is_folded = False
            player.is_all_in = False
            player.last_bet = 0
            player.update_beginning_money()
            player.all_in_pot_amount = 0
            player.all_in_difference = 0
        

    def sort_players_all_in(self):
        """
        A utility to handle your custom logic: making all-in players no longer folded, etc.
        Then sort them by their beginning stack if needed.
        """
        for player in self.players:
            if player.is_all_in:
                print(player.all_in_pot_amount)
                player.is_folded = False
        all_in_players = [player for player in self.players if player.is_all_in]
        all_in_players.sort(key=lambda player: player.beginning_money)
        for player in all_in_players: 
            self.determine_winner(self.deck)
            if self.winner[0] == player and len(self.winner) == 1:
                winning_amount = player.all_in_pot_amount
                
                player.update_money(player.all_in_pot_amount)
                
                for p in self.players:
                    p.all_in_pot_amount -= winning_amount
                self.pot -= winning_amount
                
                for i, current_player in enumerate(all_in_players):
                    if i < len(all_in_players) - 1:
                        next_player = all_in_players[i+1]
                        next_player.all_in_pot_amount -= player.all_in_pot_amount
                    elif self.pot == current_player.all_in_pot_amount:
                        break
                    else:
                        self.pot -= player.all_in_pot_amount
            elif len(self.winner) != 1 and player in self.winner:
                num_winners = len(self.winner)
                share = player.all_in_pot_amount / num_winners
                player.update_money(share)
                self.pot -= share
                for p in self.players:
                    p.all_in_amount -= share
            player.fold()
    

    def rotate_players(self):
        last_player = self.players.pop(-1)
        self.players.insert(0, last_player)
            
    
    def check_for_all_ins(self):
        if len([player for player in self.players if not player.is_all_in]) == 1:
            return True
        else:
            return False
            
        
    
# DETERMINING THE WINNER 

    def if_everyone_folds(self):
        active_players = [player for player in self.players if not player.is_folded or player.is_all_in]
        if len(active_players) == 1:
            winner = active_players[0]
            self.winner = [winner]
            print(f"\n** The winner is {winner.name} (all other players folded) **")
            self.winner_determined = True
            self.award_money_to_winner()
            self.rotate_players()
            return True
        return False
   
    
    def award_money_to_winner(self):
        if len(self.winner) == 1:
            sole_winner = self.winner[0]
            sole_winner.update_money(self.pot)
            print(f"{sole_winner.name} wins the pot of {self.pot}!")
            
        else:
        # Tie: split pot among winners
            num_winners = len(self.winner)
            share = self.pot / num_winners
            winners_names = ', '.join(player.name for player in self.winner)
            for w in self.winner:
                w.update_money(share)
            print(f"{winners_names} split the pot of {self.pot} (each gets {share:.2f})!")

   
    def determine_winner(self, deck: Deck):
        if all(player.is_folded for player in self.players):
            pass
        else:
            """
            After all betting is done and community cards are dealt,
            figure out who wins among non-folded players using tie-break logic.
            """
            # rank_names for printing
            rank_names = {
                1: "Straight Flush",
                2: "Four of a Kind",
                3: "Full House",
                4: "Flush",
                5: "Straight",
                6: "Three of a Kind",
                7: "Two Pair",
                8: "One Pair",
                9: "High Card"
            }


            community = deck.community  # 5 community cards in deck.community

            # Evaluate each player's best 7-card hand
            results = []
            active_players = [player for player in self.players if not player.is_folded]
            for player in active_players:
                seven_cards = player.hand + community  # 7 total (2 hole, 5 community)
                cat, tie = evaluate_7card_hand_detailed(seven_cards)
                results.append((player, (cat, tie)))

            # Now pick the single best or tie
            # best_hand = min(results, key=??) but we must do custom compare:
            # We'll do a simple pass:
            best_cat, best_tie = results[0][1]
            winners = [results[0][0]]  # the player objects

            for (player, (cat, tie)) in results[1:]:
                if cat < best_cat:
                    best_cat, best_tie = cat, tie
                    winners = [player]
                elif cat == best_cat:
                    if tie > best_tie:
                        best_cat, best_tie = cat, tie
                        winners = [player]
                    elif tie == best_tie:
                        winners.append(player)

            # Show the best category + tiebreak
            if len(winners) == 1:
                winner = winners[0]
                print(f"\n** The winner is {winner.name} **")
                print(f"Winning hand category: {best_cat} ({rank_names[best_cat]})")
                print(f"Tiebreakers: {best_tie}")
            else:
                # It's a tie among multiple players
                print(f"\n** It's a tie among: {', '.join(player.name for player in winners)} **")
                print(f"Hand category: {best_cat} ({rank_names[best_cat]})")
                print(f"Tiebreakers: {best_tie}")
            self.winner = winners

            self.winner_determined = True


    
    def play_one_round(self):
        # 1) Set blinds
        self.start_new_round()
        self.use_small_blind()
        self.use_big_blind()

        # 2) Deal each player 2 hole cards
        for player in self.players:
            self.deal_cards_to_player(player, 2)
        
        # 3) Pre-Flop betting
        self.initial_betting_sequence()
        self.calculate_all_in_amounts()
        if self.check_for_all_ins():
            return
        if self.if_everyone_folds():
            return  # Round ends immediately

        # 4) Flop
        self.deck.deal_flop()
        print("Flop:", self.deck.get_community_cards())
        self.reset_all_players_last_bets()
        self.reset_current_bet()
        self.post_betting_sequence()
        self.calculate_all_in_amounts()
        if self.check_for_all_ins():
            return
        if self.if_everyone_folds():
            return

        # 5) Turn
        self.deck.deal_turn()
        print("Community Cards:", self.deck.get_community_cards())
        self.reset_all_players_last_bets()
        self.reset_current_bet()
        self.post_betting_sequence()
        self.calculate_all_in_amounts()
        if self.check_for_all_ins():
            return
        if self.if_everyone_folds():
            return

        # 6) River
        self.deck.deal_river()
        print("Community Cards:", self.deck.get_community_cards())
        self.reset_all_players_last_bets()
        self.reset_current_bet()
        self.post_betting_sequence()
        self.calculate_all_in_amounts()

        # 7) Sort all-in players if needed
        self.sort_players_all_in()

        # 8) Determine the winner (showdown) if not already folded out
        self.determine_winner(self.deck)

        # 9) Award pot
        self.award_money_to_winner()
        for player in self.players:
            print(player.money)
        self.rotate_players()







main()