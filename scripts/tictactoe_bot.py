#!/usr/bin/env python3

import itertools
import numpy as np
from scripts.tictactoe import TicTacToe
from itertools import compress
import random
import pandas as pd

'''
Note we assign Qvalues after state is done
todo: 
- clean script
- see what happens when x (the bot) always starts
- parameter tuning
- Create script with metrics
- use proper notation and naming
- make nice layout


'''


class Qtable:
    """
    Qtable specifically designed for tic tac toe
    """

    def __init__(self, player_name):
        self.all_states = [[list(i[0:3]), list(i[3:6]), list(i[6:10])] for i in
                           itertools.product(['X', 'O', ''], repeat=9)]
        self.player_name = player_name
        self.action_space = [x for x in range(9)]  # There are at maximum 9 possible actions
        self.q_ref_table = dict(zip(list(range(len(self.all_states))), self.all_states))
        self.q_table = {}

    def get_qtable_state(self, current_board_state):
        key = {k for k, v in self.q_ref_table.items() if ((current_board_state == v).sum().sum() == 9)}
        if len(key) > 1:
            raise KeyError('We have duplicate states!')
        possible_actions = self.evaluate_possible_actions(current_board_state)[0]

        # Check if state already exists
        try:
            state = self.q_table[list(key)[0]]

        # Initialize state
        except:
            state = np.zeros(9)
            idx_set_na = list(set(self.action_space) - set(possible_actions))
            state[idx_set_na] = np.nan

        return state, key

    def update_qtable(self, q_table_path, reward):

        # Check if we already has seen this state before. Otherwise init with zeros
        for key in sorted(q_table_path.keys(), reverse=True):
            if key not in self.q_table.keys():
                self.q_table[key] = np.zeros(9)  # we init with zeros

        for i, key in enumerate(sorted(q_table_path.keys(), reverse=True)):
            if i == 0:
                action = q_table_path[key]
                old_value = self.q_table[key][action]
                new_q_max = (1 - self.alpha) * old_value + self.alpha * (reward)
                self.q_table[key][action] = new_q_max

            else:
                action = q_table_path[key]
                old_value = self.q_table[key][action]
                new_q_max = (1 - self.alpha) * old_value + self.alpha * (0 + self.gamma * new_q_max)  # reward r_{t} is always zero because it's not the last move
                self.q_table[key][action] = new_q_max

        pass


class QLearning:
    def __init__(self, bot_X, bot_O):
        self.bot_X = bot_X
        self.bot_O = bot_O
        self.check_different_players()
        self.q_ref_table = dict(zip(list(range(len(bot_X.all_states))), bot_X.all_states))

    def check_different_players(self):
        if self.bot_X.player_name == self.bot_O.player_name:
            raise ValueError('Should be different players')

    def evaluate_possible_actions(self, current_board_state):
        return np.where(current_board_state.flatten() == '')

    def get_qtable_state(self, env, player):

        key = {k for k, v in self.q_ref_table.items() if ((env.board == v).sum().sum() == 9)}
        if len(key) > 1:
            raise KeyError('We have duplicate states!')
        key = list(key)[0]
        possible_actions = self.evaluate_possible_actions(env.board)[0]

        if player == 'X':
            bot = self.bot_X
        else:
            bot = self.bot_O

        # Check if state already exists
        try:
            if player == 'X':
                state = self.bot_X.q_table[key]
                return state, key
            else:
                state = self.bot_O.q_table[key]
                return state, key

        # Initialize state
        except:
            state = np.zeros(9)
            idx_set_na = list(set(env.action_space) - set(possible_actions))
            state[idx_set_na] = np.nan

            # Init state in the Q Table
            if player == 'X':
                self.bot_X.q_table[key] = state
            else:
                self.bot_O.q_table[key] = state

        return state, key

    def update_qtable(self, path_x, path_o, env, reward_dict):

        alpha = 0.4
        gamma = 1

        # Update qtable O
        for i, key in enumerate(sorted(path_o.keys(), reverse=False)):
            action = path_o[key]

            if i == 0:
                old_value = bot_O.q_table[key][action]
                reward = reward_dict['O']
                next_max = 0
                new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
                bot_O.q_table[key][action] = new_value
            else:
                old_value = bot_O.q_table[key][action]
                new_value = (1 - alpha) * old_value + alpha * (gamma * new_value)
                bot_O.q_table[key][action] = new_value

        # Update qtable X
        for i, key in enumerate(sorted(path_x.keys(), reverse=False)):
            action = path_x[key]

            if i == 0:
                old_value = bot_X.q_table[key][action]
                reward = reward_dict['X']
                next_max = 0
                new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
                bot_X.q_table[key][action] = new_value
            else:
                old_value = bot_X.q_table[key][action]
                new_value = (1 - alpha) * old_value + alpha * (gamma * new_value)
                bot_X.q_table[key][action] = new_value

        pass

    def train(self, alpha=0.6, gamma=0.6, epsilon=0.1):

        for i in range(7000):

            done = False
            env = TicTacToe()
            # Init path inside the loop
            path_x = {}
            path_o = {}

            while not done:
                player_turn = env.player

                if player_turn == 'X':
                    player = self.bot_X.player_name
                else:
                    player = self.bot_O.player_name

                qstate, key = self.get_qtable_state(env, player)

                if random.uniform(0, 1) < epsilon:
                    action = env.sample()  # Explore action space
                else:
                    invalid = np.where(env.board.flatten() != '')
                    if len(invalid) > 0:
                        qstate[invalid] = np.nan

                    max_value = np.nanmax(qstate)  # Exploit learned values
                    idx = qstate == max_value
                    actions = list(compress(env.action_space, idx))
                    action = random.choice(actions)

                if player_turn == 'X':
                    path_x[key] = action
                if player_turn == 'O':
                    path_o[key] = action

                # Do action
                action_coded = {v: k for k, v in env.coordinates().items()}[action]
                game_state = env.insert_board(action_coded)

                if game_state != 'notdone':

                    if game_state == 'draw':
                        reward_dict = {'X': 0, 'O': 0}
                    if (env.player == 'O') & (game_state == 'win'):
                        reward_dict = {'X': -1, 'O': 1}
                    if (env.player == 'X') & (game_state == 'win'):
                        reward_dict = {'X': 1, 'O': -1}

                    # Update q table
                    self.update_qtable(path_x, path_o, env, reward_dict)
                    done = True
                    #print(f'{env.player}: {game_state}')
                    #print(env.board)


if __name__ == '__main__':
    bot_X = Qtable(player_name='X')
    bot_O = Qtable(player_name='O')

    QLearning(bot_X, bot_O).train()

    # Save data
    import os

    os.chdir('..')

    pd.to_pickle(bot_X, 'data/bot_x_7000.pkl')
    pd.to_pickle(bot_O, 'data/bot_o_7000.pkl')

