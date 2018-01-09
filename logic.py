"""
Self-made game '2048'.

DISCLAIMER:
- Code below is my attempt to recreate game '2048'.
- Code below is not understandable and clean at all, someday, I hope, it will be :)
- It is not the correct way how to do it!

If you want to try this yourself, be aware that:
- if you are using macOS or linux: change self.clear from 'cls' to 'clear'.
- many 'features' are not implemented yet.
"""

import os
import time
from random import *


class Game:
    """Game class."""

    def __init__(self):
        """Game setup."""
        self.game_map = {0: '', 1: '', 2: '', 3: '',
                         4: '', 5: '', 6: '', 7: '',
                         8: '', 9: '', 10: '', 11: '',
                         12: '', 13: '', 14: '', 15: ''}

        self.clear_mode = 'cls'
        self.win = False
        self.add_four = False
        self.run_once = True
        self.score = 0

        for i in range(2):
            self.add_random_tile()

    def clear(self):
        """Clear console."""
        os.system(self.clear_mode)

    def run_game(self):
        """Main loop."""
        self.print_game_map()

        while True:
            ui = input().lower()

            # Ask for new input if it's not correct
            while not self.check_user_input(ui):
                self.print_game_map()
                ui = input().lower()

            # Quick-save
            if ui == 'qs':
                self.save_game()
                time.sleep(0.5)
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

            # Shift tiles
            self.shift(ui)

            # Check if the game is won
            if self.win is False and self.has_won():
                break

            # Add random tile
            self.print_game_map()
            time.sleep(0.2)
            if self.add_random_tile():
                print("\nGAME OVER!")
                self.save_game()
                for i in range(-3, 0):
                    print('Game will close in {} seconds.'.format(abs(i)))
                    time.sleep(1)
                break

            # Print game
            self.print_game_map()

    def shift(self, direction):
        """Main magic is done here."""
        w = {'w': ([4, 8, 12], -4, range(4)), 's': ([8, 4, 0], 4, range(4)),
             'a': ([1, 2, 3], -1, range(0, 13, 4)), 'd': ([2, 1, 0], 1, range(0, 13, 4))}

        for c in w[direction][2]:  # 'w': range(4)
            counter = 0
            shifts = self.possible_shifts(c, direction)
            for i in w[direction][0] * 3:  # 'w': [4, 8, 12]
                current = c + i
                # If next tile is empty
                if self.game_map[current + w[direction][1]] == '':
                    self.game_map[current + w[direction][1]] = self.game_map[current]
                    self.game_map[current] = ''
                # If next tile and current tile equal
                elif self.game_map[current + w[direction][1]] == self.game_map[current] and counter < shifts and \
                        self.game_map[current + w[direction][1]] == str(int(self.game_map[current])):
                    # Multiply next tile by 2
                    self.game_map[current + w[direction][1]] = str(int(self.game_map[current]) * 2)
                    # Update score
                    self.score += int(self.game_map[current]) * 2
                    # Remove number from current tile
                    self.game_map[current] = ''
                    counter += 1

    def possible_shifts(self, i, direction):
        """Get the amount of possible shifts for given direction at given column/row."""
        w = {'w': ([0, 4, 8, 12], -4), 's': ([12, 8, 4, 0], 4), 'a': ([0, 1, 2, 3], -1), 'd': ([3, 2, 1, 0], 1)}
        values_for_comparing = []

        for l in w[direction][0]:
            values_for_comparing.append(self.game_map[i + l])

        shifts = self.count_similar(sorted(values_for_comparing))
        if shifts > 2: shifts = 2

        return shifts

    @staticmethod
    def count_similar(n):
        """Get the amount of similar pairs. Recursion."""
        if len(n) < 2:
            return 0
        elif n[0] == n[1]:
            return 1 + Game.count_similar(n[2:])
        else:
            return 0 + Game.count_similar(n[1:])

    def add_random_tile(self):
        """Add new tile at the random place after shift is done."""
        if self.add_four is False:
            for i in range(16):
                if self.game_map[i] == '4':
                    self.add_four = True
                    break

        choices = ['2', '2', '2', '2']
        n = randint(0, 15)

        temp = []
        while len(self.game_map[n]) > 0:
            if len(temp) > 200: return True
            temp.append(True)
            n = randint(0, 15)

        if self.add_four:
            choices += ['4', '4']

        self.game_map[n] = choice(choices)

    def has_won(self):
        """Check for the winning position."""
        for i in range(16):
            if self.game_map[i] == '2048':
                self.win = True
                self.clear()
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
        self.clear()
        if self.run_once or 1:
            print('PLAY 2048 GAME v1.0\n'
                  'Join the numbers and get to the 2048 tile!\n\n'
                  'HOW TO PLAY:\n'
                  ' - Use your WASD keys to move the tiles.\n'
                  ' - When two tiles with the same number touch, they merge into one!\n'
                  ' - Press "l" to load lastly saved game.\n'
                  ' - Press "q" to save and quit game.\n'
                  ' - Press "qs" to quicksave and continue game.\n\n')
            self.run_once = False

        m = self.game_map
        print(' SCORE: {} '.format(self.score).center(24, '='))
        for i in range(0, 16):
            if i % 4 == 0 and i != 0: print('\n-----+-----+-----+------')
            if i % 4 == 3:
                print('{}'.format(m[i].center(5)), end='')
            else:
                print('{}|'.format(m[i].center(5)), end='')
        print("\n========================")

    def save_game(self):
        """Save game into txt file."""
        print('GAME IS SAVED WITH TOTAL SCORE OF {}'.format(self.score))
        f = open('save.txt', 'w')
        f.write('Score:\n' + str(self.score) + '\n\nSaved game:\n')
        for i in range(16):
            f.write(self.game_map[i] + '\n')
        f.close()

    def load_game(self):
        """Load saved game from txt file."""
        f = open('save.txt', 'r').readlines()
        self.score = int(f[1].strip('\n'))
        for i in range(16):
            self.game_map[i] = f[i + 4].strip('\n')


if __name__ == '__main__':
    Game().run_game()
