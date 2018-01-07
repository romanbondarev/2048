"""
Self-made game '2048'.

DISCLAIMER:
- Code below is my attempt to recreate game '2048'.
- Code below is not understandable and clean at all, someday, i hope, it will be :)
- It is not the correct way how to do it!

If you want to try this yourself, be aware that:
- if you are using macOS or linux: change os.system('cls') to os.system('clear').
- input is case sensitive!
- many 'features' are not implemented yet.
- gameplay is not 100% identical... yet.
"""

from random import *
import os


class Game:
    """Game."""

    def __init__(self):
        """Setup the map."""
        self.game_map = {0: '', 1: '', 2: '', 3: '',
                         4: '', 5: '', 6: '', 7: '',
                         8: '', 9: '', 10: '', 11: '',
                         12: '', 13: '', 14: '', 15: ''}

        self.add_four = False

        # Add to the map two 'two's'
        for i in range(2):
            self.add_new_number()

        self.score = 0

    def move(self, direction):
        """Main magic is done here."""
        if direction == 'w':
            for i in range(4, 16):
                i = abs(i)
                if len(self.game_map[i - 4]) <= 0:
                    self.game_map[i - 4] = self.game_map[i]
                    self.game_map[i] = ''

                elif self.game_map[i - 4] == self.game_map[i]:
                    self.game_map[i - 4] = str(int(self.game_map[i]) * 2)
                    self.score += (int(self.game_map[i]) * 2)
                    self.game_map[i] = ''

        elif direction == 's':
            for i in range(-11, 1):
                i = abs(i)
                if len(self.game_map[i + 4]) <= 0:
                    self.game_map[i + 4] = self.game_map[i]
                    self.game_map[i] = ''
                elif self.game_map[i + 4] == self.game_map[i]:
                    self.game_map[i + 4] = str(int(self.game_map[i]) * 2)
                    self.score += (int(self.game_map[i]) * 2)
                    self.game_map[i] = ''

        elif direction == 'd':
            for i in range(-15, 1):
                i = abs(i)
                if i in [3, 7, 11, 15]:
                    continue
                if len(self.game_map[i + 1]) <= 0:
                    self.game_map[i + 1] = self.game_map[i]
                    self.game_map[i] = ''
                elif self.game_map[i + 1] == self.game_map[i]:
                    self.game_map[i + 1] = str(int(self.game_map[i]) * 2)
                    self.score += (int(self.game_map[i]) * 2)
                    self.game_map[i] = ''

        elif direction == 'a':
            for i in range(0, 16):

                if i in [0, 4, 8, 12]:
                    continue
                if len(self.game_map[i - 1]) <= 0:
                    self.game_map[i - 1] = self.game_map[i]
                    self.game_map[i] = ''
                elif self.game_map[i - 1] == self.game_map[i]:
                    self.game_map[i - 1] = str(int(self.game_map[i]) * 2)
                    self.score += (int(self.game_map[i]) * 2)
                    self.game_map[i] = ''

    def run_game(self):
        """Takes user input and does something with it."""
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
        self.get_game_map()

        while True:
            ui = input()
            # Quick-save
            if ui == 'qs':
                self.save_game()
                self.get_game_map()
                continue
            # Quit game
            elif ui == 'q':
                self.save_game()
                break
            # Load saved game
            elif ui == 'l':
                self.load_game()
                self.get_game_map()
                continue

            self.move(ui)
            self.add_new_number()
            self.get_game_map()

    def add_new_number(self):
        """Adds new number after move is done."""
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

    def get_game_map(self):
        """Prints out map."""
        os.system('cls')
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
        """Loads saved game from txt file"""
        f = open('save.txt', 'r').readlines()
        self.score = int(f[1].strip('\n'))
        for i in range(16):
            self.game_map[i] = f[i + 4].strip('\n')


if __name__ == '__main__':
    Game().run_game()
