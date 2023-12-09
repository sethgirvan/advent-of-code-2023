from collections import Counter

import fileinput
import functools
import operator

def hand_type(hand: str) -> int:
    """
    Returns hand type value in range [0, 6]
    """

    count_dict = Counter(hand)
    j_count = count_dict["J"]
    print(f"hand: {hand} j_count {j_count}")
    count_dict["J"] = 0
    counts = [x[1] for x in count_dict.items()]
    counts.sort(reverse=True)
    print(f"hand {hand} counts {counts}")

    if j_count == 5:
        return 6

    best_count = j_count + counts[0]
    print(f"best count {best_count}")

    if best_count >= 4:
        return best_count + 1
    elif best_count == 3:
        if counts[1] == 2:
            return 4
        else:
            return 3
    elif best_count == 2:
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
        "J": 0,
        "T": 9,
        }

def card_to_val(card: str) -> int:
    """
    Return card value in range [0,12]
    """
    if card.isdigit():
        return int(card) - 1
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
