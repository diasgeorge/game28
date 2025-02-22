from enum import Enum
from enum import IntEnum


#card enum for Playing Cards
class Card(Enum):
    SEVEN = 7
    EIGHT = 8
    QUEEN = 9
    KING = 10
    TEN = 11
    ACE = 12
    NINE = 13
    JACK = 14

#suit enum for Playing Cards
class Suit(Enum):
    SPADES = 'spades'
    CLUBS = 'clubs'
    HEARTS = 'hearts'
    DIAMONDS = 'diamonds'

#class to hold information for Playing cards
class PlayingCard:
    def __init__(self,card_type,card_suit):
        self.card = card_type
        self.suit = card_suit




