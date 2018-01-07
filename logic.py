"""
Self-made game '2048'.

DISCLAIMER:
- Code below is my attempt to recreate game '2048'.
- Code below is not understandable and clean at all, someday, I hope, it will be :)
- It is not the correct way how to do it!

If you want to try this yourself, be aware that:
- if you are using macOS or linux: change self.clear from 'cls' to 'clear'.
- input is case sensitive!
- many 'features' are not implemented yet.
- gameplay is not 100% identical... yet.
"""

import os
from random import *


class Game:
    """Game."""

    def __init__(self):
        """Setup the map."""
        self.game_map = {0: '', 1: '', 2: '', 3: '',
                         4: '', 5: '', 6: '', 7: '',
                         8: '', 9: '', 10: '', 11: '',
                         12: '', 13: '', 14: '', 15: ''}

        self.clear = 'cls'
        self.win = False
        self.add_four = False
        self.score = 0

        # Add to the map two 'two' tiles
        for i in range(2):
            self.add_random_tile()

    def shift(self, direction):
        """Main magic is done here."""
        w = {'w': ([4, 12, 8, 4, 12, 8], -4, range(4)),
             's': ([8, 0, 4, 8, 0, 4], 4, range(4)),
             'a': ([1, 2, 3, 1, 2, 3], -1, [0, 4, 8, 12]),
             'd': ([2, 1, 0, 2, 1, 0], 1, [0, 4, 8, 12])}

        for c in w[direction][2]:
            counter = 0
            cntr = self.coun(c, direction)
            for i in w[direction][0]:
                # for i in [4, 8, 12, 4, 8, 4]:
                if len(self.game_map[c + i + w[direction][1]]) <= 0:
                    self.game_map[c + i + w[direction][1]] = self.game_map[c + i]
                    self.game_map[c + i] = ''
                elif self.game_map[c + i + w[direction][1]] == self.game_map[c + i] and counter < cntr:
                    counter += 1
                    a = str(int(self.game_map[c + i]))
                    if self.game_map[c + i + w[direction][1]] == a:
                        self.game_map[c + i + w[direction][1]] = str(int(self.game_map[c + i]) * 2)
                        self.score += int(self.game_map[c + i]) * 2
                        self.game_map[c + i] = ''

    def coun(self, i, direction):
        counter = 0
        w = {'w': ([4, 8, 12], -4), 's': ([8, 4, 0], 4), 'a': ([1, 2, 3], -1), 'd': ([2, 1, 0], 1)}
        for s in w[direction][0]:
            if self.game_map[i + s] == self.game_map[i + s + w[direction][1]]:
                counter += 1
        if counter > 2:
            counter = 2
        return counter

    def run_game(self):
        """Takes user input and does something with it."""
        os.system(self.clear)
        print('WELCOME TO GAME 2048 v0.1\n'
              'Your goal is to to get 2048!\n\n'
              'HOW TO PLAY:\n'
              'l - load lastly saved game.\n'
              'q - save and quit game.\n'
              'qs - quicksave, continue game.\n'
              'wasd - to navigate.\n\n'
              'Press ENTER to begin playing game'
              )

        # Wait until player presses ENTER, can/should be removed
        wait = input()
        self.print_game_map()

        while True:
            ui = input().lower()
            while not self.check_user_input(ui):
                self.print_game_map()
                ui = input().lower()
            # Quick-save
            if ui == 'qs':
                self.save_game()
                self.print_game_map()
                continue
            # Quit game
            elif ui == 'q':
                self.save_game()
                break
            # Load saved game
            elif ui == 'l':
                self.load_game()
                self.print_game_map()
                continue

            self.shift(ui)
            if self.win is False and self.has_won():
                break
            self.add_random_tile()
            self.print_game_map()

    def add_random_tile(self):
        """Adds new number after shift is done."""
        if self.add_four is False:
            for i in range(16):
                if self.game_map[i] == '4':
                    self.add_four = True
                    break

        choices = ['2', '2', '2']
        n = randint(0, 15)

        while len(self.game_map[n]) > 0:
            print('New rand')
            n = randint(0, 15)

        if self.add_four:
            choices += ['4', '4']

        self.game_map[n] = choice(choices)

    def has_won(self):
        """Check for the winning position."""
        for i in range(16):
            if self.game_map[i] == '2048':
                self.win = True
                os.system(self.clear)
                print(" __   __         __      __          _ \n"
                      " \ \ / /__ _  _  \ \    / /__ _ _   | |\n"
                      "  \ V / _ \ || |  \ \/\/ / _ \ ' \  |_|\n"
                      "   |_|\___/\_,_|   \_/\_/\___/_||_| (_)\n")

                ui = input("Do you want to continue? y/n\n").lower()
                if ui == 'y':
                    self.save_game()
                    return False
                elif ui == 'n':
                    self.save_game()
                    return True

    @staticmethod
    def check_user_input(ui):
        """Check if user input is correct."""
        return ui in ['w', 'a', 's', 'd', 'q', 'qs', 'l']

    def print_game_map(self):
        """Prints out map."""
        os.system(self.clear)
        m = self.game_map
        print((f' SCORE: {self.score} ').center(24, '='))
        for i in range(0, 16):
            if i % 4 == 0 and i != 0:
                print('\n-----+-----+-----+------')
            if i in [0, 1, 2, 4, 5, 6, 8, 9, 10, 12, 13, 14]:
                print(f'{m[i].center(5)}|', end='')
            else:
                print(f'{m[i].center(5)}', end='')
        print("\n========================")

    def save_game(self):
        """Saves game into txt file."""
        print(f'YOU SAVED GAME WITH TOTAL SCORE OF {self.score}')
        f = open('save.txt', 'w')
        f.write('Score:\n')
        f.write(str(self.score))
        f.write('\n\nSaved game:\n')
        for i in range(16):
            f.write(self.game_map[i] + '\n')
        f.close()

    def load_game(self):
        """Loads saved game from txt file."""
        f = open('save.txt', 'r').readlines()
        self.score = int(f[1].strip('\n'))
        for i in range(16):
            self.game_map[i] = f[i + 4].strip('\n')


if __name__ == '__main__':
    Game().run_game()
