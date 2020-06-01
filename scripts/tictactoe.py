#!/usr/bin/env python3

import numpy as np
import random
from itertools import compress


class TicTacToe:

    def __init__(self):
        self.board = np.array([['', '', ''], ['', '', ''], ['', '', '']])
        self.number_moves = 0
        self.grid = self.coordinates()
        self.player = self.first_player()
        self.action_space = [x for x in range(9)]
        # print(f'Starting player: {self.player}')

    def sample(self):
        idx = list(self.board.flatten() == '')
        possible_actions = list(compress(self.action_space, idx))
        return random.choice(possible_actions)

    def first_player(self):
        x = random.random()
        if x < 0.5:
            player = 'X'
        else:
            player = 'O'
        return player

    def switch_player(self):
        if self.player == 'X':
            self.player = 'O'
        else:
            self.player = 'X'

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

        if self.board[element] != '':
            raise KeyError('Not a valid input!')

    def insert_board(self, coord):

        # Either X or O
        input_value = self.player

        self.board = self.board.flatten()
        element = self.grid[coord]

        # Check if valid input
        self.check_valid_input(element)

        # Insert value
        self.board[element] = input_value
        self.board = self.board.reshape(3, 3)

        # Check if there is a winner
        terminal_state = self.check_win(input_value)

        # Switch player if the game if not done yet
        if terminal_state == 'notdone':
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
            return 'win'

        if all(self.board.flatten() != ''):
            return 'draw'
        else:
            return 'notdone'


if __name__ == '__main__':

    TicTacToe().sample()
    TicTacToe().insert_board('AC')

