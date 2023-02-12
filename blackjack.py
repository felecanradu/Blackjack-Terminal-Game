import random
import os
import time
#from pytimedinput import timedInput
import getpass
import csv
from werkzeug.security import generate_password_hash, check_password_hash

class Database:

  def __init__(self):
    self.check_if_database_exists()

  def check_if_database_exists(self):
    if not os.path.exists(database_path):
        with open(database_path, "w", newline='') as database:
            fieldnames = ["first_name", "last_name", "username", "password", "budget"]
            db = csv.DictWriter(database, fieldnames=fieldnames)
            db.writeheader()

  def db_post(self, first_name, last_name, username, password, budget=0):
    with open(database_path, 'a', newline='') as database:
      fieldnames = ["first_name", "last_name", "username", "password", "budget"]
      db = csv.DictWriter(database, fieldnames=fieldnames)
      db.writerow({"first_name": first_name, "last_name": last_name, "username": username, "password": password, "budget": budget})

  def db_get(self, username, field_name):
    with open(database_path, newline='') as database:
        db = csv.DictReader(database)
        for row in db:
            if row['username'] == username:
                return row.get(field_name)

  def db_check_login(self, username, password):
    with open(database_path, newline='') as database:
        db = csv.DictReader(database)
        for row in db:
            if row['username'] == username:
                if check_password_hash(row["password"], password):
                  return True
        return False
  
  def db_update(self, username, budget):
    with open(database_path, newline='') as database:
      db = csv.DictReader(database)
      new_db = []
      for row in db:
        if row['username'] == username:
            row['budget'] = budget
        new_db.append(row)
    with open(database_path, "w", newline='') as database:
        fieldnames = ["first_name", "last_name", "username", "password", "budget"]
        db = csv.DictWriter(database, fieldnames=fieldnames)
        db.writeheader()
        for row in new_db:
            db.writerow(row)

class Layers:

  def intro_page(self):
    while True:
      global username
      os.system('cls')
      print("\n" + self.center_message("Blackjack V1.0") + "\n")
      print("\n" + self.center_message("--> Developed by Radu Felecan <--") + "\n")
      has_account = ""
      while not has_account in ("y", "n"):
        has_account = input("\n" + self.center_message("Do you already have an account? (y/n) "))
      if has_account == "y":
        username = input("\n Username: ")
        password = getpass.getpass("\n Password: ")
        if database.db_check_login(username, password):
          print("\n" + self.center_message("Login successful!"))
          print("\n" + self.center_message("Welcome back, " + database.db_get(username, "first_name") + "!"))
          time.sleep(2)
          break
        else:
          print("\n" + self.center_message("Incorrect username or password!"))
          input("\n" + self.center_message("Press ENTER to return..."))
      else:
        break
    
    if has_account == "n":
      first_name = input("\n First name: ")
      last_name = input("\n Last name: ")
      username = input("\n Username: ")
      password = getpass.getpass("\n Password: ")
      password1 = getpass.getpass("\n Confirm password: ")
      while not password == password1:
        print("\n" + self.center_message("The passwords you introduced do not match. Please retry!"))
        password1 = getpass.getpass("\n Retype password: ")
      pswd = generate_password_hash(password)
      database.db_post(first_name, last_name, username, pswd)
      print("\n" + self.center_message("Sign up successful!"))
      print("\n" + self.center_message("Welcome, " + database.db_get(username, "first_name") + "!"))
      time.sleep(2)

  def player_page(self):
    os.system('cls')
    print("\n" + self.center_message("Blackjack V1.0") + "\n")
    print("\n" + self.center_message("--> Developed by Radu Felecan <--") + "\n")
    print("\nFirst name: " + database.db_get(username, "first_name"))
    print("\nLast name: " + database.db_get(username, "last_name"))
    print("\nUsername: " + database.db_get(username, "username"))
    print("\nAvailable budget: " + str(database.db_get(username, "budget")) + "$")
    input(self.center_message("Press ENTER to continue..."))

  def loading_page(self, timestep):
    loading_line = ""
    while len(loading_line) <= 10:
      os.system('cls')
      print("\n\nLoading " + loading_line + "\n\n")
      loading_line += "■"
      time.sleep(timestep)
    time.sleep(0.5)

  def game_page(self, player_finished):
    os.system('cls')
    print("\n" + self.center_message("Blackjack V1.0") + "\n")
    print("\n" + self.center_message("--> Developed by Radu Felecan <--") + "\n")
    print("\n" + "-" * 80)
    print("\n" + self.center_message("Dealer") + "\n")
    if not player_finished:
      print(self.center_message(dealer.show(hidden=True)) + "\n\n")
    else:
      print(self.center_message(dealer.show(hidden=False)) + "\n")
      print(self.center_message(dealer.hand_status(dealer)))
    print("")
    print("-" * 80)
    print("\n" + self.center_message(player.name))
    print("\n" + self.center_message(player.show()))
    print("\n" + self.center_message(dealer.hand_status(player)))
    print("\n" + self.center_message("Budget: " + str(player.budget) + "$"))
    print("\n" + "-" * 80 + "\n")

  def center_message(self, message):
    return " " * ((80 - len(message)) // 2) + message

class Deck:
  def __init__(self):
    self.cards = []
    self.cards_value = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 10, "Q": 10, "K": 10}

  def build(self):
    names = ("2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A")
    suits = ("♦", "♣", "♥", "♠")
    self.cards = [(name + suit) for name in names for suit in suits]

  def show(self):
    print(self.cards)

  def shuffle(self):
    for card_id in range(len(self.cards)-1, 0, -1):
      random_card_id = random.randint(0, card_id)
      self.cards[card_id], self.cards[random_card_id] = self.cards[random_card_id], self.cards[card_id]

  def drawCard(self):
    return self.cards.pop()

  def count_hand(self, hand):
    hand_total = 0
    aces = 0
    for card in hand:
      if not card[0] == "A":
        hand_total += self.cards_value.get(card[:-1])
      else:
        aces += 1
    if aces > 0:
      for i in range(aces):
        if hand_total <= 10:
          hand_total += 11
        else:
          hand_total += 1
        i += 1
    return hand_total
            
class Dealer:
  def __init__(self):
    self.name = "Dealer"
    self.hand = []
    self.hand_total = 0

  def show(self, hidden):
    cards = ""
    if hidden:
      cards = self.hand[0] + " ?"
    else:
      for card in self.hand:
        cards += card + " "
    return cards

  def draw(self):
    return deck.drawCard()

  def deal(self, players):
    for player in players:
      player.hand = []
    for i in range(2):
      for player in players:
        player.hand.append(self.draw())
  
  def hit(self, player):
    player.hand.append(self.draw())
  
  def hand_status(self, player):
    if self.check_status(player) == "blackjack":
      return "Blackjack!"
    elif self.check_status(player) == "bust":
      return "Bust!"
    else:
      return ""

  def check_status(self, player):
    player.hand_total = deck.count_hand(player.hand)
    if player.hand_total == 21:
      return "blackjack"
    elif player.hand_total < 17:
      return "hit"
    elif player.hand_total > 21:
      return "bust"
    else:
      return player.hand_total

class Player:
  def __init__(self, name, budget):
    self.name = name
    self.budget = budget
    self.hand = []
    self.hand_total = 0

  def show(self):
    cards = ""
    for card in self.hand:
      cards += card + " "
    return cards

# End of functions

database_path = "./blackjack.csv"

database = Database()
deck = Deck()
display = Layers()

display.intro_page()
display.loading_page(0.1)
display.player_page()
display.loading_page(0.1)

players = []

dealer = Dealer()
player = Player(database.db_get(username, "first_name"), int(database.db_get(username, "budget")))

players.append(player)
players.append(dealer)

while player.budget >= 5:

  deck.build()
  deck.shuffle()
  dealer.deal(players)

  player_finished = False
  dealers_turn = False
  
  while not player_finished:
    display.game_page(player_finished)
    if dealer.check_status(player) == "blackjack":
      print(display.center_message(player.name + " won!"))
      player.budget += 5
      break
    elif dealer.check_status(player) == "bust":
      print(display.center_message(player.name + " lost!"))
      player.budget -= 5
      break
    elif dealer.check_status(player) in (17, 18, 19, 20):
      action = ""
      while not action in ("h", "hit", "s", "stand"):
        action = input(display.center_message("Would you like another card (hit) or would you like to stand down (stand)? "))
      if action == "hit" or action == "h":
        dealer.hit(player)
      else:
        player_finished = True
        dealers_turn = True
    else:
      action = input(display.center_message("Press ENTER to request another card... "))
      dealer.hit(player)

  while dealers_turn:
    display.game_page(player_finished)
    if dealer.check_status(dealer) == "blackjack":
      print(display.center_message("Dealer won!"))
      player.budget -= 5
      break
    elif dealer.check_status(dealer) == "bust":
      print(display.center_message("Dealer lost!"))
      player.budget += 5
      break
    elif dealer.check_status(dealer) == "hit":
      print(display.center_message("The dealer draws another card..."))
      time.sleep(1)
      dealer.hit(dealer)
    elif dealer.check_status(dealer) in (17, 18, 19, 20):
      if dealer.check_status(dealer) == dealer.check_status(player):
        print(display.center_message("Equal score!"))
      elif dealer.check_status(dealer) < dealer.check_status(player):
        print(display.center_message(player.name + " won!"))
        player.budget += 5
      else:
        print(display.center_message("Dealer won!"))
        player.budget -= 5
      break
  database.db_update(username, player.budget)
  action = input(display.center_message("\nPress ENTER to continue the game... "))

print(display.center_message("You ran out of money :("))
    
