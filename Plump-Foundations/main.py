import random

from classes import Card, Player, Deck
import func

if __name__ == "__main__":
  print("Welcome to the game of Plump!")
  #Set up a dictionary which we will fill with the players and their cards
  players = {}
  
  #Create players
  nr_players = int(func.get_valid_input("How many players are there? ", func.is_valid_nr_players))

  #Get player names
  names = []
  for i in range(nr_players):
    name = func.get_valid_input("What is the name of player " + str(i + 1) + "? ", func.is_valid_name, names)
    names.append(name)
    players[f"player{i+1}"] = Player(name, [], 0, 0, 0, "")

  #Determine nr of rounds
  nr_rounds = func.get_valid_input("\nHow many rounds should be played? \n", func.is_valid_nr_rounds, nr_players)
  nr_rounds = int(nr_rounds)
  
  #Play the game until we've played all the rounds
  round_counter = 1
  while round_counter <= nr_rounds:
    
    #Create deck and shuffle it at the start of each round
    deck = Deck()
    deck.shuffle()

    #Deal cards
    nr_starting_cards = round_counter
    players, deck = func.deal_cards(players, deck, nr_starting_cards)

    #Determine bidding order
    if round_counter == 1:
      bidding_order = []
    bidding_order = func.bidding_order(players, bidding_order)

    #Players take turn bidding
    players = func.bidding(players, bidding_order, nr_starting_cards)

    #Determine playing order
    playing_order = func.initial_play_order(players, bidding_order)

    #The players play a certain amount of rounds
    for _ in range(nr_starting_cards):

      #Reset the stack between each turn
      stack, suit_to_follow = func.reset_stack()

      #Each player takes their turn and plays a card
      for player in playing_order:
        players, stack, suit_to_follow = func.playing_sequence(players, player, stack, suit_to_follow)

      #Determine what card won
      highest_card = max((card for card in stack if card.suit == suit_to_follow), key = lambda card: int(card.value))
      print(f"\nThe highest card is: {highest_card}.\n")

      #Determine winner of trick
      for player in players:
        if players[player].card_played == highest_card:
          print(f"{players[player].name} takes home the trick.")
          players[player].tricks += 1

      #Print scores
      for player in players:
        print(f"{players[player].name} has {players[player].tricks} tricks.")
      
    #End of round
    players = func.end_of_round(players)
  
    #Reset tricks taken
    players = func.reset_tricks(players)

    #Increase round counter by 1 at end of loop
    round_counter += 1

  #Print out the end scores and the winner
  func.end_of_game(players)