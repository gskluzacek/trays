"""
What this script does (game.py)
It’s a small card-dealing demo that:
Builds a standard 52‑card deck
Suits: ♠ ♡ ♢ ♣
Ranks: 2 through 10, J, Q, K, A
Each card is represented as a tuple like ("♠", "A").
Shuffles the deck
When play() runs, it creates the deck with shuffle=True, so the order is randomized.
Deals the deck into 4 hands
It deals cards “round-robin” style (like real dealing): the 1st card to player 1, 2nd to player 2, 3rd to player 3, 4th to player 4, then repeats.
Each player ends up with 13 cards (because 52 / 4 = 13).
Prints each player’s hand
It labels players as P1, P2, P3, P4.
For each player it prints a line like:
P1: ♠2 ♣K ♡10 ... (format is suit+rank)
Runs when executed as a script
If you run python game.py, it calls play() and prints the dealt hands.
If you import it from another module, it won’t auto-run (because of the if __name__ == "__main__": guard).
"""
# game.py

import random

SUITS = "♠ ♡ ♢ ♣".split()
RANKS = "2 3 4 5 6 7 8 9 10 J Q K A".split()


def create_deck(shuffle=False):
    """Create a new deck of 52 cards"""
    deck = [(s, r) for r in RANKS for s in SUITS]
    if shuffle:
        random.shuffle(deck)
    return deck


def deal_hands(deck):
    """Deal the cards in the deck into four hands"""
    return (deck[0::4], deck[1::4], deck[2::4], deck[3::4])


def play():
    """Play a 4-player card game"""
    deck = create_deck(shuffle=True)
    names = "P1 P2 P3 P4".split()
    hands = {n: h for n, h in zip(names, deal_hands(deck))}

    for name, cards in hands.items():
        card_str = " ".join(f"{s}{r}" for (s, r) in cards)
        print(f"{name}: {card_str}")


if __name__ == "__main__":
    play()
