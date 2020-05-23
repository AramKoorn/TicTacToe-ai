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
            reward = 0
        if terminal_state == 'win':
            reward = 10
        if terminal_state == 'draw':
            reward = 4
        return reward

    def train_bot(self):

        # For plotting metrics
        all_epochs = []
        all_penalties = []

        for i in range(2):

            done = False
            env = TicTacToe()

            while not done:

                current_board = env.board
                q_state, key = self.get_qtable_state(current_board)
                q_max = np.max(q_state)
                sel = q_state == q_max
                action_list = list(compress(self.action_space, sel))
                if len(action_list) > 1:
                    action = random.choice(action_list)  # Select randomly from all the max value actions
                else:
                    action = action_list[0]

                action = {v: k for k, v in env.coordinates().items()}[action]
                terminal_state = env.insert_board(action)
                self.get_reward(terminal_state)
    #           q_state = self.ge







if __name__ == '__main__':
    TicTacToeBot().train_bot()