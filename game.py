from PlayingCard import PlayingCard
from PlayingCard import Card
from PlayingCard import Suit
from random import randint
import operator

card_value = 0
full_deck  = []
partial_deck = []
play_deck = []
Players = {1 : [], 2: [], 3: [], 4: []}
Players_bid = {1: 0, 2: 0, 3: 0, 4: 0}
card_round = {}

 
#Function for deal a full deck of cards  
def create_deck():
    for suit in Suit:
        for card in Card:
                full_deck.append(PlayingCard(Card(card),Suit(suit)))

    return full_deck
 
def getRangeforGame(n):
    rangeOut = ""
    for i in range(n,29):
          rangeOut = rangeOut + str(i) + ","
    return rangeOut

def keywithmaxval(d):
     """ a) create a list of the dict's keys and values; 
         b) return the key with the max value"""  
     v = list(d.values())
     k = list(d.keys())
     return k[v.index(max(v))]

def draw_card (deck):
    rand_card = randint(0, len(deck)-1)
    return deck.pop(rand_card)

def draw_players_card(players_deck,card_number):
     return players_deck.pop(card_number)
     

def card_value(card):
    card_value = 0
    if (str(card) == "Card.SEVEN" or str(card) == "Card.EIGHT" or str(card) == "Card.KING" or str(card) == "Card.QUEEN"):
        card_value = 0
    elif(str(card) == "Card.TEN" or str(card) == "Card.ACE"):
            card_value = 1
    elif(str(card) == "Card.NINE"):
            card_value = 2
    elif(str(card) == "Card.JACK"):
            card_value = 3
    return card_value

def first_deal_28(partial_deck):
    while(len(partial_deck) > 16):
        for player in Players:
            Players[player].append(draw_card(partial_deck))      

def second_deal_28(partial_deck):
    while(len(partial_deck) > 0):
        for player in Players:
            Players[player].append(draw_card(partial_deck))  

def first_round_card_bidding(Players_bid):
    for key in Players_bid.keys():
            if ( key == 1):
                  Players_bid[key] = int(input("Please Select Bid Amount for Player" + str(key) + " : " + getRangeforGame(14) + "\n") or 0)
                  Players_bid[key] = Players_bid[key] if Players_bid[key] != 0 else 14
            if ( key == 2):
                Players_bid[key] = int(input("Please Select Bid Amount for Player" + str(key) + " : " + getRangeforGame(Players_bid[1] + 1) + "\n") or 0)
            if ( key == 3):
                if ( Players_bid[2] == 0):
                    Players_bid[key] = Players_bid[key] = int(input("Please Select Bid Amount for Player" + str(key) + " : " + getRangeforGame(20) + "\n") or 0)
                elif (Players_bid[2] > 0):
                    Players_bid[key] = Players_bid[key] = int(input("Please Select Bid Amount for Player" + str(key) + " : " + getRangeforGame(Players_bid[2] + 1) + "\n") or 0)
            if ( key == 4):
                if ( Players_bid[2] == 0 and Players_bid[3] == 0):
                      Players_bid[key] = int(input("Please Select Bid Amount for Player" + str(key) + " : " + getRangeforGame(15) + "\n") or 0)
                elif (Players_bid[2] > 0 and Players_bid[3] == 0):
                    Players_bid[key] = Players_bid[key] = int(input("Please Select Bid Amount for Player" + str(key) + " : " + getRangeforGame(Players_bid[2] + 1) + "\n") or 0)
                elif (Players_bid[2] > 0 and Players_bid[3] > 0):
                    Players_bid[key] = Players_bid[key] = int(input("Please Select Bid Amount for Player" + str(key) + " : " + getRangeforGame(Players_bid[3] + 1) + "\n") or 0)
                elif (Players_bid[2] == 0 and Players_bid[3] > 0):
                    Players_bid[key] = Players_bid[key] = int(input("Please Select Bid Amount for Player" + str(key) + " : " + getRangeforGame(Players_bid[3] + 1) + "\n") or 0)
                
                

def First_round_trump_card(Players_bid, Players):
    trump_Key = keywithmaxval(Players_bid)
    print("Player ",trump_Key," : ", Players_bid[trump_Key])
    print("Select your trump Card from your Cards \n")
    for i in range(0, len(Players[trump_Key])):
             print("Player ",trump_Key," : ", Players[trump_Key][i].card , Players[trump_Key][i].suit)
    trump_card_key = int(input("Select your trump Card from your Cards 1,2,3,4 \n"))
    trump_card_key = trump_card_key - 1
    trump_card = Players[trump_Key][trump_card_key].card
    trump_suit = Players[trump_Key][trump_card_key].suit
    print("Player ",trump_Key," Trump : ",trump_card , trump_suit )
    return trump_card,trump_suit,trump_Key

def get_range_of_suits(Players,player,round_suit):
     card_range_stats = []
     if not round_suit:
        for i in range(0, len(Players[player])):
               card_range_stats.append(i)
        return card_range_stats
     for i in range(0, len(Players[player])):
          if (Players[player][i].suit == round_suit):
               j = i + 1
               card_range_stats.append(j)
     return card_range_stats

def get_range_of_Trumps(Players,player,trump_suit):
     card_range_stats = []
     for i in range(0, len(Players[player])):
          if (Players[player][i].suit != trump_suit):
               j = i + 1
               card_range_stats.append(j)
     return card_range_stats
     
def intialize_card_round(roundplayer,card_round):
     card_round.clear()
     roundp = roundplayer
     while(roundp < 5):
          card_round[roundp] = []
          roundp = roundp + 1
     i = 1
     while(len(card_round) < 5 and i < roundplayer):
          card_round[i] = []
          i = i + 1
     return card_round
     
def show_Cards(Players):
    for player in Players:
        for i in range(0, len(Players[player])):
             print("Player ",player," : ", Players[player][i].card , Players[player][i].suit, card_value(Players[player][i].card))

def show_card_round(card_round):
     for player in card_round:
           for i in range(0, len(card_round[player])):
             print("Player ",player," : ", card_round[player][i].card , card_round[player][i].suit, card_value(card_round[player][i].card))


def gameround(Players,card_round,trump_suit,trump_player,cardsOpen):
     print("Let us start the game \n")
     card_round_number = 0
     no_suit = ""
     round_suit = ""
     list_iterator = iter(card_round)
     first_item = next(list_iterator)
     print(first_item)
     if ( first_item == trump_player and cardsOpen == 0):
        card_range = get_range_of_Trumps(Players,first_item,trump_suit)
     else:
        card_range = get_range_of_suits(Players,first_item,round_suit)
     card_round_number = int(input("1Player " + str(first_item) + " Play from your Cards "+ str(card_range)+ " \n"))
     while (card_round_number not in card_range ):
        card_round_number = int(input("2Player " + str(first_item) + " Play from your Cards "+ str(card_range)+ " \n"))
     card_round_number = card_round_number - 1
     round_suit = Players[first_item][card_round_number].suit
     card_round[first_item].append(draw_players_card(Players[first_item],card_round_number))
     
     for item in list_iterator:
        card_range = get_range_of_suits(Players,item,round_suit)
        if not card_range:
            card_range = get_range_of_suits(Players,item,trump_suit)
        if not card_range:
            card_range = get_range_of_suits(Players,item,no_suit)
        card_round_number = int(input("1Player " + str(item) + " Play from your Cards "+ str(card_range)+ " \n"))
        while (card_round_number not in card_range ):
            card_round_number = int(input("2Player " + str(item) + " Play from your Cards "+ str(card_range)+ " \n"))
        card_round_number = card_round_number - 1
        card_round[item].append(draw_players_card(Players[item],card_round_number))
     return card_round,round_suit

def roundgame(card_round,main_suit,trump_suit,cardsOpen):
     card_values = {}
     winningPlayer = 0
     sumofCardValues = 0
     for player in card_round:
           for i in range(0, len(card_round[player])):
                if (card_round[player][i].suit == trump_suit):
                     if (winningPlayer != 0):
                          if ( card_round[player][i].card.value > card_round[winningPlayer][i].card.value):
                               winningPlayer = player
                     else:
                          winningPlayer = player
                          cardsOpen = 1
                if (card_round[player][i].suit == main_suit):
                     card_values[player] = card_round[player][i].card.value
                sumofCardValues = sumofCardValues + card_value(card_round[player][i].card)
     if (winningPlayer):
          return winningPlayer,sumofCardValues,cardsOpen
     lplayer = max(card_values.items(), key=operator.itemgetter(1))[0]
     return lplayer,sumofCardValues,cardsOpen

def gamePlay(Players,trump_player,trump_suit):
     #Intitalize the Card Round for Round 1
     sumGame1 = 0
     sumGame2 = 0
     cardsOpen = 0
     card_round = {}
     for player in Players:
          card_round[player] = []
          card_round[player] = []
          card_round[player] = []
          card_round[player] = []

     for i in range(0, 8):
          card_round,round_suit = gameround(Players,card_round,trump_suit,trump_player,cardsOpen)
          show_card_round(card_round)
          roundplayer,sumofCardValues,cardsOpen = roundgame(card_round,round_suit,trump_suit,cardsOpen)
          if (roundplayer == 1 or roundplayer == 3):
               print("Winner is : ", roundplayer)
               sumGame1 = sumGame1 + sumofCardValues
          if (roundplayer == 2 or roundplayer == 4):
               print("Winner is : ", roundplayer)
               sumGame2 = sumGame2 + sumofCardValues
          card_round = intialize_card_round(roundplayer,card_round)
    
     print( "Total Points for Team A : ", sumGame1 )
     print( "Total Points for Team B : ", sumGame2 )
          
               
# Driver program to test above functions.
full_deck = create_deck()
partial_deck = list(full_deck)
first_deal_28(partial_deck) 
show_Cards(Players)
first_round_card_bidding(Players_bid)
trump_card,trump_suit,trump_player = First_round_trump_card(Players_bid, Players)
x = input("Do you want to continue : Y/N \n")
if x == 'Y':
    second_deal_28(partial_deck)

show_Cards(Players)
gamePlay(Players,trump_player,trump_suit)
show_Cards(Players)





