"""Aditya Varshney Blackjack"""

from random import *
import sys

goal_score = 21
num_decks = 1
starting_cash = 500

def set_num_decks(value):
	global num_decks
	num_decks = value

def set_starting_cash(value):
	global starting_cash
	starting_cash = value

def set_goal_score(value):
	global goal_score
	goal_score = value

# Greets users and provides options to change the game's settings
def welcome_page():
	global starting_cash

	print("\n-*-*-*-*-\tWelcome to Blackjack\t-*-*-*-*-\n")
	option = eval(input("To Play Game, Press 1. For Settings, Press 2..."))
	if(option==1):
		return
	else:
		print("\n\tSettings\t\n")
		# ndecks = eval(input("Enter the number of decks you would like to use (default is 1 deck)..."))
		# set_num_decks(ndecks)
		# scash = eval(input("Enter the default starting cash amount (default is 500)..."))
		# set_starting_cash(scash)
		gscore = eval(input("Fun Option: Enter the value of blackjack that you would like to play with (default is 21)..."))
		set_goal_score(gscore)
		return

def new_round_page():
	print("\n-*-*-*-*-\tNext Round\t-*-*-*-*-\n")

def is_new_game():
	return(cash_available[0]==starting_cash and cash_available[1]==starting_cash)

score1, score2, score_dealer = 0,0,0
player1, player2, dealer = 0,1,100
player1_list, player2_list = [], []
dealer_hand = []
bets,cash_available = [],[starting_cash,starting_cash]
Blackjack = False

# Deck is the set of cards still available in the game
# By default, deck is sequenced from 1 to 52. Call 
# shuffle() to swap the various deck values.

deck = [1,2,3,4,5,6,7,8,9,10,10,10,10]*4*num_decks
# deck = [1,1,10,10]*13*num_decks

def shuffle():
	global deck
	for i in range(52):
		swap_index = randint(1,51)
		swap_value = deck[swap_index]
		deck[swap_index] = deck[i]
		deck[i] = swap_value
	return deck

# Shuffle the deck
deck = shuffle()

# Completes the action of drawing a card
# This involves decrementing the size of the deck 
# and returning the card that was drawn from the top of the deck.
def draw_card(deck):
	next_card = deck.pop(0)
	return next_card

def get_bets(A=1):
	global bets
	if(A==1):
		bet1 = eval(input('Player 1: Place bet... '))
		if(bet1>cash_available[0]):
			print("Bet is too high! ")
			get_bets()
		elif(bet1<=0):
			print("Bet is too low! ")
			get_bets()
		A=2
	if(A==2):
		bet2= eval(input('Player 2: Place bet... '))
		if(bet2>cash_available[1]):
			print("Bet is too high! ")
			get_bets(2)
		if(bet2<=0):
			print("Bet is too low! ")
			get_bets(2)
		A=1
	bets.append(bet1)
	bets.append(bet2)
	return bets


def next_player(player):
	return 1-player


def prompt_user_move():
	choice = eval(input('See Hand, Hit, or Stay?' +'\n' + 'Enter 1 to See Hand, 2 to Hit, 3 to Stay. '))
	return choice

# Determines if the player is busted. check_busted will use
# choose ace_value to see if an ace should return 1 or 11.
def check_game_over():
	return (score1 >= goal_score or score2 >= goal_score) # is busted or game is over

def check_for_ones(player_list):
	for i in player_list:
		if(i == 1):
			return True
	return False

def reset():
	global score1
	global score2
	global player1_list
	global player2_list
	global deck
	global bets
	global cash_available
	global Blackjack

	score1,score2,player1_list,player2_list,bets,Blackjack=0,0,[],[],[],False

def double_bet(player):
	global bets
	global cash_available

	current = bets[player]
	cash_available[player] -= current
	bets[player] += current

def get_list(player):
	if(player == player1):
		return player1_list
	if(player == player2):
		return player2_list

def get_score(player):
	if(player == player1):
		return score1
	if(player == player2):
		return score2

def set_list(player,p_list):
	global player1_list
	global player2_list

	if(player == player1):
		player1_list = p_list
	if(player == player2):
		player2_list = p_list

def set_score(player,score):
	global score1
	global score2

	if(player == player1):
		score1 = score
	if(player == player2):
		score2 = score

def update_score(player,cards):
	global score1
	global score2
	global player1_list
	global player2_list
	global Blackjack

	next_card = draw_card(cards)%13 # Since the deck is numbered from 1 to 52, we need to account for suites

	if(not check_game_over()):
		if(player == player1):
			score1 += next_card
			player1_list.append(next_card)		
			if(goal_score - score1 == 10):
				if(check_for_ones(player1_list)):
					score1 += 10
					print("Hand: " + str(get_list(player)))
					print("Player 1 wins! Blackjack!")
					Blackjack = True
					return player1
			if(score1>goal_score):
				print("Hand: " + str(get_list(player)))
				print("Player 2 Wins!")
				return player2
			if(score1==goal_score):
				print("Hand: " + str(get_list(player)))
				print("Player 1 Wins!")
				return player1

		if(player==player2):
			score2 += next_card
			player2_list.append(next_card)
			if(goal_score - score2 == 10):
				if(check_for_ones(get_list(player))):
					score2 += 10
					print("Hand: " + str(get_list(player)))
					print("Player 2 wins! Blackjack!")
					Blackjack = True
					return player2
			if(score2>goal_score):
				print("Hand: " + str(get_list(player)))
				print("Player 1 Wins!")
				return player1
			if(score2==goal_score):
				print("Hand: " + str(get_list(player)))
				print("Player 2 Wins!")
				return player2
	return -1

# Alternative (more concise) implementation to update_score(). Has bugs!
def update_score2(player,cards):
	global score1
	global score2
	global player1_list
	global player2_list
	global Blackjack

	next_card = draw_card(cards)%13 # Since the deck is numbered from 1 to 52, we need to account for suites

	score = get_score(player)
	list = get_list(player)
	player_number = player+1

	score += next_card
	list.append(next_card)		
	if(score == 11):
		if(check_for_ones(player1_list)):
			score += 10
			print(list)
			set_score(player,score)
			set_list(player,list)
			Blackjack = True
			print("Player " + str(player_number) + " wins! Blackjack!")
			return player

	elif(score==goal_score):
		print("Player " + str(player_number) + " wins!")
		return player

	if(score>goal_score):
		print("Player " + str(player_number) + " wins!")
		return next_player(player)

	return -1


# Resets hands and deals out 2 cards
def start_game(player,deck,winner=-1):
	global cash_available
	global bets
	reset()
	if(is_new_game()):
		welcome_page()
	else:
		new_round_page()
	print("Player 1's money: " + str(cash_available[0]) + "\tPlayer 2's money: " + str(cash_available[1]))
	bets = get_bets()
	for i in range(0,2):
		cash_available[i]-=bets[i]
	for i in range(0,2):
		if(winner==-1):
			winner = update_score(player,deck)
		if(winner==-1):
			winner = update_score(next_player(player),deck)
	if(not check_game_over()):
		print("\nCards Dealt. Let's Play!")
	else:
		adjust_money(winner)

# Play out a game of blackjack until one of the players busts, wins, or runs out of money.
# Implements start_game and what_next for complete user interaction
def play(deck=deck,scoreA=0,scoreB=0,player=player1, goal=goal_score):
	global score1
	global score2
	global player1
	global player2
	global player1_list
	global player2_list
	
	start_game(player,deck)

	while(check_game_over()==False):
		if(player == player1):
			print("\n"+"It's Player 1's turn.")
			player = play_round(deck,score1,player)
		elif player == player2:
			print("\n"+"It's Player 2's turn.")
			player = play_round(deck,score2,player)
		if(check_game_over()):
			if(no_funds(player)):
				break
			if(no_funds(1-player)):
				player = 1-player # Changes reference of 'player', needed for what_next() implementation
				break
	what_next(player)

# Play one player's turn. Gets player moves, changes players, and adjusts money if necessary.
# Return the player whose turn is next. Return the winner if the game ends.
def play_round(deck, current_score, player,winner=-1):
	choice = prompt_user_move()
	if(choice == 1):
		print("\nCurrent Hand: " + str(get_list(player)) + "\t" + "Money: " + str(cash_available[player]))
	if(choice == 2):
		winner = update_score(player,deck)
		if(not check_game_over()):
			play_round(deck,current_score,player)
		if(winner > -1):
			adjust_money(winner)
			return winner
	if(choice == 3):
	 	return next_player(player)
	# if(choice == 4):
	# 	double_bet(player)
	# 	winner = update_score(player,deck)
	# 	adjust_money(winner)
	return player

def adjust_money(player):
	global bets
	global cash_available
	global Blackjack

	amt = bets[player]

	if(Blackjack):
		print("Winnings: " + str(amt*3/2))
		cash_available[player] += amt*5/2
	else:
		print("Winnings: " + str(amt))
		cash_available[player] += amt*2
	print("Player " + str(player+1) + ": " + str(cash_available[player]))
	print("Player " + str(2-player) + ": " + str(cash_available[1-player]))

def no_funds(player):
	return cash_available[player]==0

# Determines if player has funds and can play more.
# If the player has enough funds, then what_next will ask if players want to play another round.
# Otherwise, what_next will ask if players want to start a new game.
def what_next(player):
	global cash_available

	if(no_funds(player)):
		end_menu = eval(input("Player "+ str(player+1)+ " has no funds! Press 1 for a new game or 2 to quit. "))
		if(end_menu == 1):
			cash_available[0],cash_available[1] = starting_cash, starting_cash
			play()
		else:
			exit()
	else:
		end_menu = eval(input("Press 1 for another round or 2 to quit. "))
		if(end_menu == 1):
			play()
		elif end_menu == 2:
			exit()