from collections import Counter

import fileinput
import functools
import operator

def hand_type(hand: str) -> int:
    """
    Returns hand type value in range [0, 6]
    """

    counts = [x[1] for x in Counter(hand).items()]
    counts.sort(reverse=True)
    print(f"hand {hand} counts {counts}")
    if counts[0] >= 4:
        return counts[0] + 1
    elif counts[0] == 3:
        if counts[1] == 2:
            return 4
        else:
            return 3
    elif counts[0] == 2:
        if counts[1] == 2:
            return 2
        else:
            return 1
    else:
        return 0

card_val_dict = {
        "A": 12,
        "K": 11,
        "Q": 10,
        "J": 9,
        "T": 8,
        }

def card_to_val(card: str) -> int:
    """
    Return card value in range [0,12]
    """
    if card.isdigit():
        return int(card) - 2
    else:
        return card_val_dict[card]

def hand_to_val(hand: str) -> int:
    card_vals = [card_to_val(card) for card in hand]
    print(card_vals)
    return 13**5 * hand_type(hand) \
            + functools.reduce(lambda sum, card: 13*sum + card, card_vals)

hand_bids = (line.split() for line in fileinput.input())
hand_bid_vals = ((hand_to_val(hand_bid[0]), int(hand_bid[1])) for hand_bid in hand_bids)
hand_bids_sorted = sorted(hand_bid_vals, key=lambda x: x[0])
rank_bids = list(((i + 1, bid) for i, (_, bid) in enumerate(hand_bids_sorted)))
print(rank_bids)
total = functools.reduce(operator.add, (rank * bid for rank, bid in rank_bids))
print(total)
