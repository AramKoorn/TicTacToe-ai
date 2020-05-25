import itertools
import numpy as np
from scripts.tictactoe import TicTacToe
from itertools import compress
import random

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

players = [0, 1, 2]


class TicTacToeBot:

    def __init__(self):
        self.all_states = [[list(i[0:3]), list(i[3:6]), list(i[6:10])] for i in itertools.product(players, repeat=9)]
        self.action_space = [x for x in range(9)]  # There are at maximum 9 possible actions
        self.player = 'x'  # bot is player x
        self.q_ref_table = dict(zip(list(range(len(self.all_states))), self.all_states))
        self.q_table = {}
        self.alpha = 0.8
        self.gamma = 0.6
        self.epsilon = 0.2

    def evaluate_possible_actions(self, current_board_state):
        return np.where(current_board_state.flatten() == 0)

    def get_qtable_state(self, current_board_state):
        key = {k for k, v in self.q_ref_table.items() if ((current_board_state == v).sum().sum() == 9)}
        if len(key) > 1:
            raise KeyError('We have duplicate states!')
        possible_actions = self.evaluate_possible_actions(current_board_state)[0]

        # Check if state already exists
        try:
            state = self.q_table[key]

        # Initialize state
        except:
            state = np.zeros(9)
            idx_set_na = list(set(self.action_space) - set(possible_actions))
            state[idx_set_na] = np.nan

        return state, key

    def get_reward(self, terminal_state, player):

        if (terminal_state == 'win') & (player == 'x'):
            reward = 1
        if terminal_state == 'draw':
            reward = 0.5
        if (terminal_state == 'win') & (player == 'o'):
            reward = -1
        return reward

    def check_finished(self, terminal_state):
        if terminal_state != 'notdone':
            return True
        else:
            return False

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

    def train_bot(self, iterations=1000):

        # For plotting metrics
        winner_list = []

        for i in range(iterations):

            done = False
            env = TicTacToe()
            q_table_history = {}

            while not done:

                current_board = env.board
                starting_player = env.player

                if env.player == 'x':

                    player_playing = env.player

                    # Explore
                    if random.random() < self.epsilon:
                        action = random.choice(self.evaluate_possible_actions(env.board)[0])

                    # Eploit
                    else:
                        q_state, key = self.get_qtable_state(current_board)
                        q_max = np.nanmax(q_state)
                        sel = q_state == q_max
                        action_list = list(compress(self.action_space, sel))
                        if len(action_list) > 1:
                            action = random.choice(action_list)  # Select randomly from all the max value actions
                        else:
                            action = action_list[0]

                    action_coded = {v: k for k, v in env.coordinates().items()}[action]
                    terminal_state = env.insert_board(action_coded)

                    # Save action
                    q_table_history[list(key)[0]] = action

                    done = self.check_finished(terminal_state)
                    if done:

                        winner_list.append(f'{starting_player}: {terminal_state}')

                        # Get reward
                        reward = self.get_reward(terminal_state, player_playing)
                        self.update_qtable(q_table_history, reward)
                        if reward == 1:
                            print('AI won!')
                        else:
                            print('draw')

                else:

                    # Player playing
                    player_playing = env.player

                    possible_actions = self.evaluate_possible_actions(current_board)[0]
                    action = random.choice(possible_actions)
                    action = {v: k for k, v in env.coordinates().items()}[action]
                    terminal_state = env.insert_board(action)
                    done = self.check_finished(terminal_state)
                    if done:

                        winner_list.append(f'{starting_player}: {terminal_state}')

                        reward = self.get_reward(terminal_state, player_playing)
                        self.update_qtable(q_table_history, reward)
                        if reward == 1:
                            print('Stupid won :(')
                        else:
                            print('draw')

        return winner_list, self.q_table

if __name__ == '__main__':
    winners, q_table = TicTacToeBot().train_bot()
