import itertools
import numpy as np
from scripts.tictactoe import TicTacToe
from itertools import compress
import random

players = [0, 1, 2]

class TicTacToeBot:
    """
    Reward winning = 10
    reward nothing = 1
    reward draw = 5
    penalty losing = -10
    """

    def __init__(self):
        self.all_states = [[list(i[0:3]), list(i[3:6]), list(i[6:10])] for i in itertools.product(players, repeat=9)]
        self.action_space = [x for x in range(9)]  # There are at maximum 9 possible actions
        self.player = 'x'  # bot is player x
        self.q_ref_table = dict(zip(list(range(len(self.all_states))), self.all_states))
        self.q_table = {}
        self.alpha = 0.1
        self.gamma = 0.6
        self.epsilon = 0.1

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

    def get_reward(self, terminal_state):
        if terminal_state == 'notdone':
            reward = 1
        if terminal_state == 'win':
            reward = 10
        if terminal_state == 'draw':
            reward = 4
        return reward

    def check_finished(self, terminal_state):
        if terminal_state != 'notdone':
            return True
        else:
            return False

    def train_bot(self):

        # For plotting metrics
        winner_list = []

        for i in range(100):

            done = False
            env = TicTacToe()

            while not done:

                current_board = env.board

                if env.player == 'x':

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
                    reward = self.get_reward(terminal_state)

                    # Get state of the board after applying action
                    new_board = env.board
                    q_state_new, _ = self.get_qtable_state(new_board)
                    new_q_max = np.nanmax(q_state_new)

                    # Update q value
                    new_value = (1 - self.alpha) * q_max + self.alpha * (reward + self.gamma * new_q_max)
                    q_state[action] = new_value
                    self.q_table[list(key)[0]] = q_state

                    done = self.check_finished(terminal_state)
                    if done:
                        winner_list.append(f'ai: {terminal_state}')
        #           q_state = self.ge

                # Play against random opponent
                else:
                    possible_actions = self.evaluate_possible_actions(current_board)[0]
                    action = random.choice(possible_actions)
                    action = {v: k for k, v in env.coordinates().items()}[action]
                    terminal_state = env.insert_board(action)
                    done = self.check_finished(terminal_state)
                    if done:
                        winner_list.append(f'stupid: {terminal_state}')

        return winner_list

if __name__ == '__main__':
    test = TicTacToeBot().train_bot()