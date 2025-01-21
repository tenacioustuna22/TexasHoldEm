import cards as pt_cards
import re
from collections import Counter
from operator import itemgetter
from itertools import groupby

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
    print('Your hand is:\n' + str(hand))
    print('The flop is:\n' + str(flop))
    print('The Turn comes:\n' + str(turn))
    print('The River shows:\n' + str(river) + '\n\nFor a table '
                                              'of:\n\n' + str(community))

    return total_cards.append(hand + community)


def detect_flush():
    flush = ''.join(total_cards[hand_count])

    if len(re.findall('Hearts', flush)) > 4:
        return True
    elif len(re.findall('Diamonds', flush)) > 4:
        return True
    elif len(re.findall('Spades', flush)) > 4:
        return True
    elif len(re.findall('Clubs', flush)) > 4:
        return True
    else:
        return False


def detect_multiple():
    ranks = []
    for i in range(len(total_cards[hand_count])):
        card = total_cards[hand_count][i].split('-')
        ranks.append(card[0])

    c = Counter(ranks)
    multiples = c.most_common(2)

    if multiples[0][1] == 2:
        return str('Pair of ' + multiples[0][0] + "'s ")
    elif multiples[0][1] == 2 and multiples[1][1] == 2:
        return str('Two Pair of ' + multiples[0][0] + "'s and " +
                   multiples[1][0] + "'s ")
    elif multiples[0][1] == 3:
        return str('Three of a kind ' + multiples[0][0] + "'s ")
    elif multiples[0][1] == 4:
        return str('Four of a kind ' + multiples[0][0] + "'s ")
    elif multiples[0][1] == 3 and multiples[1][1] == 2:
        return str('Full House, ' + multiples[0][0] + "'s over " +
                   multiples[1][0] + "'s ")
    else:
        return False


def detect_straight():
    # Create dictionary linking each card to its ranking
    rank_values = {'2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7,
                   '9': 8, '10': 9, 'Jack': 10, 'Queen': 11, 'King': 12,
                   'Ace': 13}
    reverse_values = {y: x for x, y in rank_values.items()}
    hand_values = []
    no_dup_values = []
    runs = []
    high_card_value = []
    straight = False

    # Iterate through total_cards and add the card ranks to hand_values
    for i in range(len(total_cards[hand_count])):
        card = total_cards[hand_count][i].split('-')
        hand_values.append(rank_values.get(card[0]))
    # Get rid of any duplicates, they interrupt our run search
    for value in hand_values:
        if value not in no_dup_values:
            no_dup_values.append(value)
    # If any Aces, add the unlisted value 0 to account for low straight
    if max(no_dup_values) == 13:
        no_dup_values.append(0)
    # Sort low to high
    no_dup_values.sort()
    # Create runs a list of lists with consecutive values together as a list
    # and non consecutive values the only list item
    for k, g in groupby(list(enumerate(no_dup_values)), lambda x: x[0] - x[1]):
        runs.append(list(map(itemgetter(1), g)))
    # See if any of the lists have 5 cards in them (a poker straight)
    # If they do, set indicator to True and get the high card
    for i in range(len(runs)):
        if len(runs[i]) > 4:
            straight = True
            high_card_value.append(runs[i][-1])
            high_card.append(reverse_values.get(high_card_value[0]))

    if detect_flush() is True and straight is True:
        if high_card[hand_count] == 'Ace':
            return str("Royal Flush !")
        else:
            return str("Straight Flush " + str(high_card[hand_count]) +
                       " high.")
    elif straight is True:
        return str("Straight " + str(high_card[hand_count]) + " high.")

    else:
        return False

start_new_hand()
print("\n" + str(total_cards))
print(detect_multiple())
print(detect_flush())
print(detect_straight())
print(total_cards)
