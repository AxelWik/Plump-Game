import constants
import random

#Functions to determine valid inputs
def get_valid_input(prompt, validation_function, *args):
  while True:
    user_input = input(prompt)
    if validation_function(user_input, *args):
      return user_input
    else:
      print(constants.invalidinput)

def is_valid_nr_players(nr_players):
  if nr_players.isdigit():
    return int(nr_players) > 1 and int(nr_players) <= 5
  return False

def is_valid_name(name, names):
  if name == "" or name in names:
    return False
  return True

def is_valid_nr_rounds(nr_cards, nr_players):
  if nr_cards.isdigit():
    return int(nr_cards) > 0 and 52 / nr_players >= int(nr_cards)
  return False
  
def is_valid_bid(bid, nr_cards, bids, is_last_player):
  if not bid.isdigit():
    return False
    
  if int(bid) > nr_cards or int(bid) < 0:
    return False

  if int(bid)+bids == nr_cards and is_last_player:
    return False
  return True

#Print functions
def print_bidding_order(players, bidding_order):
  bidding_order_string = ", ".join([players[name].name for name in bidding_order])
  print(bidding_order_string, "is the bidding order.")
  print(players[bidding_order[-1]].name, "is the last player.")
  return

def print_cards(players, player):
  cards_held = [str(card) for card in players[player].cards]
  cards_string = f"\nCards held by {players[player].name}:\n" + ", ".join(cards_held)
  print(cards_string)
  return

def print_stack(stack):
  cards_on_stack = [str(card) for card in stack]
  stack_string = "Cards on the stack:\n" + ", ".join(cards_on_stack)
  print(stack_string)
  return

#Gameplay
def deal_cards(players, deck, nr_cards):
  for _ in range(int(nr_cards)):
    for player in players:
      dealt_card = deck.deal()
      if dealt_card:
        players[player].cards.append(dealt_card)
      else:
        print(constants.emptydeck)
  return players, deck

def bidding_order(players, bidding_order):
  if bidding_order == []:
    bidding_order = list(players.keys())
    random.shuffle(bidding_order)
    print_bidding_order(players, bidding_order)
    return bidding_order
  bidding_order = bidding_order[1:] + bidding_order[:1]
  print_bidding_order(players, bidding_order)
  return bidding_order

def bidding(players, names, nr_cards):
  bids = 0
  for player in names:
    print(f"\nIt is {players[player].name}'s turn.")
    is_last_player = False
    if player == names[-1]:
      print("This is the last player to bid!")
      is_last_player = True
    print_cards(players, player)
    bid = int(get_valid_input("What is your bid? ", is_valid_bid, nr_cards, bids, is_last_player))
    bids += bid
    players[player].bid = bid
    print(f"{players[player].name} has bid {players[player].bid} tricks. Total bid: {bids}.")
  return players

def initial_play_order(players, names):
  player_bids = [[players[player].bid, player] for player in names]
  max_bid = max(player_bids, key = lambda x: x[0])
  max_bid_index = player_bids.index(max_bid)
  player_order = [x[1] for x in player_bids]
  playing_order_vars = player_order[max_bid_index:] + player_order[:max_bid_index]
  playing_order_names = ", ".join([players[name].name for name in playing_order_vars])
  print("Playing order: ", playing_order_names)
  return playing_order_vars

def is_valid_selection(selection, players, player, suit_to_follow):
  if not selection.isdigit():
    return False
  
  selection = int(selection)
  if selection < 1 or selection > len(players[player].cards):
    return False
  
  legal_cards = get_legal_selections(players, player, suit_to_follow)
  if not any(legal_cards):
    return True
  return legal_cards[selection-1]
  
def get_legal_selections(players, player, suit_to_follow):
  return [str(card.suit) == suit_to_follow for card in players[player].cards]

def set_suit_to_follow(stack, suit_to_follow):
  suit_to_follow = stack[0].suit
  print(f"Suit to follow: {suit_to_follow}\n")
  return stack, suit_to_follow

def select_card(players, player, stack, suit_to_follow):
  print(f"{players[player].name} has bid {players[player].bid}, and has taken {players[player].tricks} tricks so far.")
  selection = get_valid_input("What card do you wish to play? Enter its position in your hand. ", is_valid_selection, players, player, suit_to_follow)
  selection = int(selection)-1
  card_to_play = players[player].cards[selection]
  players[player].card_played = card_to_play
  print(f"{players[player].name} plays {players[player].card_played}.\n")
  stack.append(card_to_play)
  if len(stack) == 1:
    stack, suit_to_follow = set_suit_to_follow(stack, suit_to_follow)
  players[player].cards.remove(card_to_play)
  return players, stack, suit_to_follow

def playing_sequence(players, player, stack, suit_to_follow):
  print(f"\nIt is {players[player].name}'s turn.\n")
  print_cards(players, player)
  players, stack, suit_to_follow = select_card(players, player, stack, suit_to_follow)
  print_stack(stack)
  return players, stack, suit_to_follow

def end_of_round(players):
  print("\nThe round has concluded!")
  for player in players:
    round_points = 0
    print(f"{players[player].name} has {players[player].tricks} tricks and bid {players[player].bid}.")
    if players[player].tricks == players[player].bid:
      round_points += 10+players[player].bid
      if players[player].tricks == 0:
        round_points -= 5
      players[player].points += round_points
      print(f"{players[player].name} has earned {round_points} points.")
    print(f"{players[player].name} has {players[player].points} points.\n")
  return players

def reset_stack():
  stack = []
  suit_to_follow = ""
  return stack, suit_to_follow

def reset_tricks(players):
  for player in players:
    players[player].tricks = 0
  return players

def end_of_game(players):
  print("The game has ended!")
  top_score = -1
  top_score_player = ""
  for player in players:
    print(f"{players[player].name} has {players[player].points} points.")
    if players[player].points == top_score:
      top_score_player = top_score_player + " and " + players[player].name
    if players[player].points > top_score:
      top_score = players[player].points
      top_score_player = players[player].name
  print(f"The winner is {top_score_player} with {top_score} points!")
  return