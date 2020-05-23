import itertools
import numpy as np
from scripts.tictactoe import TicTacToe

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

    def get_qtable_sate(self, current_board_state):
        key = {k for k, v in self.q_ref_table.items() if ((current_board_state == v).sum().sum() == 9)}
        if len(key) > 1:
            raise KeyError('We have duplicate states!')
        possible_actions = self.evaluate_possible_actions(current_board_state)

        # Check if state already exists
        try:
            state = self.q_table[key]

        # Initialize state
        except:
            state = np.zeros(9)
            state[key][possible_actions] = np.nan

        return state

    # For plotting metrics
    all_epochs = []
    all_penalties = []

    #






if __name__ == '__main__':
    1 + 1