import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scripts.tictactoe import TicTacToe
from scripts.tictactoe_bot import Qtable


def play_against_random(iterations):

    bot = pd.read_pickle('data/qtable_o.pkl')
    test = Qtable('X')

    ai_won = 0
    random_moves = 0

    for i in range(iterations):

        env = TicTacToe()

        done = False
        while not done:


            # Random play
            if env.player == 'X':
                action = env.sample()
                move = {v: k for k, v in env.coordinates().items()}[action]
                game_state = env.insert_board(move)

            # AI PLay
            else:
                key = list({k for k, v in test.q_ref_table.items() if (env.board == v).sum().sum() == 9})[0]
                try:
                    state = bot[key]
                    action = np.nanargmax(state)
                    action_coded = {v: k for k, v in env.coordinates().items()}[action]
                    game_state = env.insert_board(action_coded)
                # In case the AI never was in this state before
                except:
                    action = env.sample()
                    move = {v: k for k, v in env.coordinates().items()}[action]
                    game_state = env.insert_board(move)
                    random_moves += 1

            if (game_state == 'win') & (env.player == 'O'):
                ai_won += 1

            if game_state != 'notdone':
                done = True

    return ai_won, random_moves


# PLay thousand games against random player
def run():

    iterations = 1000
    ai_won, random_moves = play_against_random(iterations=iterations)

    print(f'AI won {ai_won/iterations}% of {iterations} games')
    print(f'Total random moves: {random_moves} in {iterations} games')

    pass


if __name__ == '__main__':

    import os
    os.chdir('..')

    run()