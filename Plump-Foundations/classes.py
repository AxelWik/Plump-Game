import random

class Player:
  def __init__(self, name, cards, points, tricks, bid, card_played):
    self.name = name
    self.cards = cards
    self.points = points
    self.tricks = tricks
    self.bid = bid
    self.card_played = card_played

class Card:
  def __init__(self, suit, rank):
    self.suit = suit
    self.rank = rank
    self.value = self.get_card_value()
  def get_card_value(self):
    if self.rank in ["J", "Q", "K", "A"]:
      return  {"J": 11, "Q": 12, "K": 13, "A": 14}[self.rank]
    else: 
      return self.rank
  def __str__(self):
    if self.suit in ["Hearts", "Diamonds"]:
      return f"\033[31m{self.suit}{self.rank}\033[0m"  # Red color for Hearts and Diamonds
    else:
      return f"{self.suit}{self.rank}"

class Deck:
  def __init__(self):
    self.cards = []
    suits = ["♥️", "♦️", "♠️", "♣️"]
    ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    for suit in suits:
      for rank in ranks:
        self.cards.append(Card(suit, rank))

  def shuffle(self):
    random.shuffle(self.cards)

  def deal(self):
    return self.cards.pop() 

  def __str__(self):
    return str(self.cards)