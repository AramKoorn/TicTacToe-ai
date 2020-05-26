import numpy as np
import random


class TicTacToe:

    def __init__(self):
        self.board = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
        self.number_moves = 0
        self.grid = self.coordinates()
        self.player = self.first_player()
        # print(f'Starting player: {self.player}')

    def first_player(self):
        x = random.random()
        if x < 0.5:
            player = 'x'
        else:
            player = 'o'
        return player

    def switch_player(self):
        if self.player == 'x':
            self.player = 'o'
        else:
            self.player = 'x'

    def coordinates(self):
        grid =  '''\
                AA AB AC
                BA BB BC
                CA CB CC
                '''
        grid = grid.split()
        mapping = list(range(len(grid)))
        return dict(zip(grid, mapping))

        return grid

    def check_valid_input(self, element):

        if element not in list(range(0, len(self.board))):
            raise ValueError('Not a valid input!')

        if self.board[element] != 0:
            raise KeyError('Not a valid input!')

    def insert_board(self, coord):

        # Determine input value
        if self.player == 'x':
            input_value = 1
        else:
            input_value = 2

        self.board = self.board.flatten()
        element = self.grid[coord]

        # Check if valid input
        self.check_valid_input(element)

        # Insert value
        self.board[element] = input_value
        self.board = self.board.reshape(3, 3)

        # Check if there is a winner
        terminal_state = self.check_win(input_value)
        #print(f'\n {self.board}')

        # Switch player
        self.switch_player()

        return terminal_state

    def check_win(self, input_value):
        for i in range(3):

            # Check horizontal
            if all(self.board[:, i] == input_value):
                return 'win'

            # Check vertical
            if all(self.board[i, :] == input_value):
                return 'win'

        # Check diagonal
        if all(self.board.diagonal() == input_value):
            return 'win'

        # Check other diagonal
        if all(np.fliplr(self.board).diagonal() == input_value):
            'win'

        if all(self.board.flatten() != 0):
            return 'draw'
        else:
            return 'notdone'


if __name__ == '__main__':

    TicTacToe().insert_board('AC')
