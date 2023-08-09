#!/usr/bin/env python3
import random
"""This program plays a game of Rock, Paper, Scissors between two Players,
and reports both Player's scores each round."""

moves = ['rock', 'paper', 'scissors']

"""The Player class is the parent class for all of the Players
in this game"""


def valid_input(string, options, quiting):
    player_choice = input(string).lower()
    if player_choice in moves or player_choice in options:
        if player_choice == "rock" or player_choice == "r":
            return "rock"
        elif player_choice == "paper" or player_choice == "p":
            return "paper"
        elif player_choice == "scissors" or player_choice == "s":
            return "scissors"
        else:
            return player_choice
    else:
        if quiting and player_choice == "quit":
            return "quit"
        else:
            return valid_input(string, options, quiting)


def num_input(string):
    try:
        rounds_num = int(round(float(input(string))))
        if rounds_num < 1:
            rounds_num = 1
    except ValueError:
        print("Please enter a whole number.")
        return num_input(string)
    return rounds_num


class Player:
    def move(self):
        return 'rock'

    def learn(self, my_move, their_move):
        pass


class RandomPlayer(Player):
    def move(self):
        return random.choice(moves)


class HumanPlayer(Player):
    def move(self):
        return valid_input("Rock, Paper, Scissors? (r,p,s) --> ",
                           ["r", "p", "s"], True)


class ReflectPlayer(Player):
    def __init__(self):
        self.my_next_move = random.choice(moves)

    def move(self):
        return self.my_next_move

    def learn(self, my_move, their_move):
        self.my_next_move = their_move


class CyclePlayer(Player):
    def __init__(self):
        self.my_next_move = moves[random.randint(0, 2)]

    def move(self):
        return self.my_next_move

    def learn(self, my_move, their_move):
        self.my_next_move = moves[(moves.index(my_move) + 1) % 3]


def beats(one, two):
    return ((one == 'rock' and two == 'scissors') or
            (one == 'scissors' and two == 'paper') or
            (one == 'paper' and two == 'rock'))


class Game:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.win1 = 0
        self.win2 = 0

    def play_round(self):
        self.move1 = self.p1.move()
        self.move2 = self.p2.move()
        if self.move1 != "quit" and self.move2 != "quit":
            print(f"Player 1: {self.move1}  Player 2: {self.move2}")
            self.p1.learn(self.move1, self.move2)
            self.p2.learn(self.move2, self.move1)
            if beats(self.move1, self.move2):
                print("Player 1 Win!")
                self.win1 += 1
            elif self.move1 == self.move2:
                print("***TIES***")
            else:
                print("Player 2 Win!")
                self.win2 += 1
            print(f"Player 1 : {self.win1} win(s) | Player "
                  f"2 : {self.win2} win(s)\n")

    def wwr_mode(self):
        n = num_input("How many round(s) you would like to play?"
                      "(min. 1)--> ")
        print("\nGame start!")
        print("You are Palyer 1!\n")
        for round in range(n):
            print(f"Round {round + 1}:")
            self.play_round()
            if self.move1 == "quit" or self.move2 == "quit":
                break

    def fptp_mode(self):
        n = num_input("Number of win(s) to declare a winner? (min. 1)--> ")
        print("\nGame start!")
        print("You are Palyer 1!\n")
        self.round = 0
        while self.win1 < n and self.win2 < n:
            self.round += 1
            print(f"Round {self.round}:")
            self.play_round()
            if self.move1 == "quit" or self.move2 == "quit":
                break

    def gv_mode(self):
        n = num_input("Number of win(s) exceeding opponent to declare a "
                      "winner? (min. 1)--> ")
        print("\nGame start!")
        print("You are Palyer 1!\n")
        self.round = 0
        while abs(self.win1 - self.win2) < n:
            self.round += 1
            print(f"Round {self.round}:")
            self.play_round()
            if self.move1 == "quit" or self.move2 == "quit":
                break

    def winner(self, one, two):
        if one > two:
            print(f"\nThe winner is Player 1 with total {self.win1} win(s)!!!")
        elif one < two:
            print(f"\nThe winner is Player 2 with total {self.win2} win(s)!!!")
        else:
            print(f"\nThere is no Winner! Is a Ties at {self.win1} win(s)!!!")

    def play_game(self):
        print("""

        Game Mode:
        1. Win within rounds
        2. First past the post
        3. Great victory

        """)
        mode = valid_input("Please Select Game Mode.\n", ["1", "2", "3"],
                           False)
        if mode == "1":
            self.wwr_mode()
        elif mode == "2":
            self.fptp_mode()
        elif mode == "3":
            self.gv_mode()

        self.winner(self.win1, self.win2)
        print("Game over!\n")


if __name__ == '__main__':
    game = Game(HumanPlayer(), RandomPlayer())
    game.play_game()
