import os
import time
from random import *


class Game:
    """2048 game."""

    def __init__(self):
        """Gamemap and variable initialization."""
        self.game_map = {0: '', 1: '', 2: '', 3: '',
                         4: '', 5: '', 6: '', 7: '',
                         8: '', 9: '', 10: '', 11: '',
                         12: '', 13: '', 14: '', 15: ''}

        self.clear_mode = 'cls'
        self.win = False
        self.add_four = False
        self.score = 0
        self.load_game()

    def clear(self):
        """Clears the console."""
        os.system(self.clear_mode)

    def run_game(self):
        """Main game loop."""
        self.print_game_map()

        while True:
            user_input = input().lower()
            while not self.check_user_input(user_input):
                self.print_game_map()
                user_input = input().lower()

            # Start the new game
            if user_input == 'n':
                self.clear()
                reset = input('Reset Progress & Start New Game? y/n: ').lower()
                if reset == 'y':
                    self.start_new_game()
                self.save_game()
                self.print_game_map()
                continue

            # Quit game
            elif user_input == 'q':
                self.clear()
                self.save_game()
                print('Quiting game...')
                time.sleep(3)
                break

            # Load saved game
            elif user_input == 'l':
                self.load_game()
                self.print_game_map()
                continue

            # Shift tiles
            self.shift(user_input)

            self.print_game_map()
            time.sleep(0.2)
            # Check for the winning position and try to add a new tile
            if self.win is False and self.has_won() or self.add_random_tile():
                self.clear()
                self.save_game()
                print('Quiting game...')
                time.sleep(3)
                break

            # Save game
            self.save_game()

            # Print game
            self.print_game_map()

    def shift(self, direction):
        """Tile shifting."""
        moves = {'w': ([4, 8, 12], -4, range(4)), 's': ([8, 4, 0], 4, range(4)),
                 'a': ([1, 2, 3], -1, range(0, 13, 4)), 'd': ([2, 1, 0], 1, range(0, 13, 4))}

        for c in moves[direction][2]:  # 'w': range(4)
            counter = 0
            shifts = self.possible_shifts(c, direction)
            for i in moves[direction][0] * 3:  # 'w': [4, 8, 12]
                current = c + i
                # If next tile is empty
                if self.game_map[current + moves[direction][1]] == '':
                    self.game_map[current + moves[direction][1]] = self.game_map[current]
                    self.game_map[current] = ''
                # If next tile and current tile are the same
                elif self.game_map[current + moves[direction][1]] == self.game_map[current] and counter < shifts and \
                        self.game_map[current + moves[direction][1]] == str(int(self.game_map[current])):
                    # Multiply next tile by 2
                    self.game_map[current + moves[direction][1]] = str(int(self.game_map[current]) * 2)
                    # Update score
                    self.score += int(self.game_map[current]) * 2
                    # Remove number from current tile
                    self.game_map[current] = ''
                    counter += 1

    def possible_shifts(self, row, direction):
        """Gets the amount of possible shifts for given direction at given column/row."""
        moves = {'w': ([0, 4, 8, 12], -4), 's': ([12, 8, 4, 0], 4), 'a': ([0, 1, 2, 3], -1), 'd': ([3, 2, 1, 0], 1)}
        values_to_compare = []

        for l in moves[direction][0]:
            values_to_compare.append(self.game_map[row + l])

        shifts = self.count_similar(sorted(values_to_compare))
        if shifts > 2: shifts = 2

        return shifts

    @staticmethod
    def count_similar(n):
        """Gets the amount of similar pairs."""
        if len(n) < 2:
            return 0
        elif n[0] == n[1]:
            return 1 + Game.count_similar(n[2:])
        else:
            return 0 + Game.count_similar(n[1:])

    def add_random_tile(self):
        """Adds a new tile at the random place."""
        if self.add_four is False:
            for i in range(16):
                if self.game_map[i] == '4':
                    self.add_four = True
                    break

        choices = ['2', '2', '2', '2']
        n = randint(0, 15)

        counter = 0
        # If tile is not empty at random value place, generate a new random value
        # Timeout after 200 tries
        while len(self.game_map[n]) > 0:
            if counter > 200: return True
            counter += 1
            n = randint(0, 15)

        if self.add_four: choices += ['4', '4']
        self.game_map[n] = choice(choices)
        return False

    def has_won(self):
        """Checks for the winning position."""
        for i in range(16):
            if self.game_map[i] == '2048':
                self.win = True
                self.clear()
                print(" __   __         __      __          _ \n"
                      " \ \ / /__ _  _  \ \    / /__ _ _   | |\n"
                      "  \ V / _ \ || |  \ \/\/ / _ \ ' \  |_|\n"
                      "   |_|\___/\_,_|   \_/\_/\___/_||_| (_)\n")
                ui = input("Do you want to continue? y/n: ").lower()
                if ui == 'n':
                    return True
        return False

    @staticmethod
    def check_user_input(user_input):
        """Checks if user's input is correct."""
        return user_input in ['w', 'a', 's', 'd', 'q', 'l', 'n']

    def print_game_map(self):
        """Prints out map."""
        self.clear()
        print('PLAY 2048 GAME v1.0\n'
              'Join the numbers and get to the 2048 tile!\n\n'
              'HOW TO PLAY:\n'
              ' - Use your WASD keys to move the tiles.\n'
              ' - When two tiles with the same number touch, they merge into one!\n'
              ' - Press "q" to quit game.\n'
              ' - Press "n" to start a new game.\n')

        m = self.game_map
        print(' SCORE: {} '.format(self.score).center(24, '='))
        for i in range(0, 16):
            if i % 4 == 0 and i != 0: print('\n-----+-----+-----+------')
            if i % 4 == 3:
                print('{}'.format(m[i].center(5)), end='')
            else:
                print('{}|'.format(m[i].center(5)), end='')
        print("\n========================")

    def start_new_game(self):
        """Starts a new game."""
        self.win, self.add_four, self.score = False, False, 0
        for c in range(16): self.game_map[c] = ''
        for i in range(2): self.add_random_tile()

    def save_game(self):
        """Saves game into txt file."""
        f = open('save.txt', 'w')
        f.write('Score:\n' + str(self.score) + '\n\nSaved game:\n')
        for i in range(16):
            f.write(self.game_map[i] + '\n')
        f.write('\n' + str(self.win))
        f.close()

    def load_game(self):
        """Loads saved game from txt file."""
        try:
            file = open('save.txt', 'r').readlines()
        except FileNotFoundError:
            self.start_new_game()
        else:
            self.score = int(file[1].strip('\n'))
            self.win = file[21]
            for i in range(16):
                self.game_map[i] = file[i + 4].strip('\n')


if __name__ == '__main__':
    Game().run_game()
